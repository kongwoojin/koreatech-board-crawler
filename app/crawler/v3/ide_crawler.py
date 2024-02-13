import json
import re

import asyncio

import aiohttp
from aiohttp import ClientConnectorError
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import edgedb

from app.crawler.v3 import headers, gather_with_concurrency, ServerRefusedError
from app.dataclass.board import Board
from app.db.v3 import edgedb_client
from app.logs import crawling_log


async def article_parser(session, data: Board):
    now = datetime.now()

    num_parsed = data.num
    board = data.board
    article_url_parsed = data.article_url
    writer_parsed = data.writer

    crawling_log.article_crawling_log(data)

    try:
        async with session.get(data.article_url, headers=headers) as resp:
            # add small delay for avoid ServerDisconnectedError
            await asyncio.sleep(0.01)
            if resp.status == 200:
                html = await resp.text()
                soup = BeautifulSoup(html, 'html.parser')

                file_list = []

                try:
                    title_parsed = soup.select_one("div.artclViewTitleWrap > h2").text.strip().replace("\n", "") \
                        .replace("\t", "").replace("［", "[").replace("］", "]")
                    write_date_parsed = soup.select_one(
                        "div.right > dl:nth-child(1) > dd").text
                    write_date_parsed = datetime.strptime(write_date_parsed, '%Y.%m.%d')
                    text_parsed = soup.select_one(
                        "div.artclView").decode_contents()
                    text_parsed = text_parsed.replace("<img", "<br><img")
                    text_parsed = text_parsed.replace("/dext5editordata",
                                                      "https://cms3.koreatech.ac.kr/dext5editordata")
                    read_count_parsed = int(soup.select_one("div.right > dl:nth-child(4) > dd").text.strip())

                    files = soup.select("div.artclItem.viewForm > dl > dd > ul > li")

                    for file in files:
                        file_url = file.select_one("a")["href"]
                        file_name = file.select_one("a").text
                        file_name = re.sub("\[.*]", "", file_name).strip()

                        file_dic = {
                            "file_url": f'https://cms3.koreatech.ac.kr{file_url}',
                            "file_name": file_name
                        }

                        file_list.append(file_dic)
                except AttributeError as e:
                    crawling_log.attribute_exception_error(article_url_parsed, e)

            else:
                crawling_log.http_response_error(resp.status, article_url_parsed)
    except (Exception, ClientConnectorError):
        raise ServerRefusedError(data)


async def board_page_crawler(session, board_num: int, page: int, ignore_date=False):
    board_list = []

    crawling_log.board_crawling_log(board_num, page)

    url = f"https://cms3.koreatech.ac.kr/bbs/ide/{board_num}/artclList.do?page={page}"

    date_of_last_article = 0

    try:
        async with session.get(url, headers=headers) as resp:
            # add small delay for avoid ServerDisconnectedError
            await asyncio.sleep(0.01)
            if resp.status == 200:
                html = await resp.text()
                soup = BeautifulSoup(html, 'html.parser')

                posts = soup.select("table.artclTable > tbody > tr")

                for post in posts:
                    try:
                        num_parsed = post.select_one("td._artclTdNum").text.strip()
                        writer_parsed = post.select_one("td._artclTdWriter").text.strip()
                        article_url_parsed = post.select_one("td._artclTdTitle > a").get('href')
                        article_url_parsed = f"https://cms3.koreatech.ac.kr{article_url_parsed}"
                        write_date_parsed = post.select_one("td._artclTdRdate").text.strip()
                        write_date_parsed = datetime.strptime(write_date_parsed, '%Y.%m.%d')

                        date_of_last_article = write_date_parsed

                        # If article older than 7 days, pass it
                        if not ignore_date and (datetime.today() - timedelta(days=7) > write_date_parsed):
                            continue

                        board_list.append(
                            Board(
                                board=board_num,
                                num=num_parsed,
                                article_url=article_url_parsed,
                                writer=writer_parsed
                            ))
                    except Exception as e:
                        crawling_log.unknown_exception_error(e)
    except (Exception, ClientConnectorError):
        raise ServerRefusedError(page)

    if ignore_date:
        return board_list
    else:
        if datetime.today() - timedelta(days=7) > date_of_last_article:
            return board_list
        else:
            board_list.extend(await board_page_crawler(session, board_num + 1, page))
            return board_list


async def board_crawler(board_num: int, start_page: int, last_page: int):
    # limit TCPConnector to 10 for avoid ServerDisconnectedError
    # Enable force_close to disable HTTP Keep-Alive
    connector = aiohttp.TCPConnector(limit=10, force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        board_list = await board_list_crawler(session, board_num, start_page, last_page)

        await board_crawler_task(session, board_list)


async def board_list_crawler(session, board_num: int, start_page: int, last_page: int):
    board_list = []
    failed_page = []

    pages = [asyncio.ensure_future(board_page_crawler(session, board_num, page, True)) for page in
             range(start_page, last_page + 1)]
    datas = await gather_with_concurrency(100, *pages)
    for data in datas:
        try:
            board_list.extend(data)
        except TypeError:
            failed_page.append(int(data.data))

    failed_page.sort()

    if failed_page:
        board_list.extend(await board_list_crawler(session, board_num, failed_page[0], failed_page[-1]))

    return board_list


async def board_crawler_task(session, board_list):
    tasks = [asyncio.ensure_future(article_parser(session, data)) for data in board_list]
    result = await gather_with_concurrency(100, *tasks)

    failed_data = [i for i in result if i is not None]
    failed_data = [i.data for i in failed_data]

    if failed_data:
        await board_crawler_task(session, failed_data)


async def sched_board_crawler(board_num: int):
    # limit TCPConnector to 10 for avoid ServerDisconnectedError
    # Enable force_close to disable HTTP Keep-Alive
    connector = aiohttp.TCPConnector(limit=10, force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        board_list = await board_page_crawler(session, board_num, 1)

        await board_crawler_task(session, board_list)
