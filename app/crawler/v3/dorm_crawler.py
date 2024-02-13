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
    client = edgedb_client()
    now = datetime.now()

    num_parsed = data.num
    board = data.board
    article_url_parsed = data.article_url

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
                    title_parsed = soup.select_one("#board > div.boardViewer > h4").text.strip()
                    text_parsed = soup.select_one(
                        "#board > div.boardViewer > table.viewer div.story").decode_contents()
                    text_parsed = text_parsed.replace("<img", "<br><img")
                    writer_parsed = soup.select_one(
                        "#board > div.boardViewer > table.viewer > tr > td:nth-child(2)").text.strip()
                    write_date_parsed = soup.select_one(
                        "#board > div.boardViewer > table.viewer > tr > td:nth-child(4)").text.strip()
                    write_date_parsed = datetime.strptime(write_date_parsed, '%Y-%m-%d')
                    read_count_parsed = int(soup.select_one(
                        "#board > div.boardViewer > table.viewer > tr > td:nth-child(6)").text.strip())

                    files = soup.select("#board > div.boardViewer > table.viewer tr:nth-child(3) > td > a")

                    for file in files:
                        file_url = file["href"]
                        file_name = file.text
                        file_name = re.sub("\[.*]", "", file_name).strip()

                        file_dic = {
                            "file_url": f"https://dorm.koreatech.ac.kr{file_url}",
                            "file_name": file_name
                        }

                        file_list.append(file_dic)

                except AttributeError as e:
                    crawling_log.attribute_exception_error(article_url_parsed, e)

                try:
                    client.query("""
                            insert dorm {
                                board := <str>$board,
                                num := <str>$num,
                                title := <str>$title,
                                writer := <str>$writer,
                                write_date := <cal::local_date>$write_date,
                                read_count := <int64>$read_count,
                                article_url := <str>$article_url,
                                content := <str>$content,
                                crawled_time := <cal::local_datetime>$crawled_time,
                                files := (with
                                          raw_data := <json>$file_data,
                                          for item in json_array_unpack(raw_data) union (
                                            insert Files {
                                                file_name := <str>item['file_name'],
                                                file_url := <str>item['file_url']            
                                            } unless conflict on .file_url else (
                                            update Files
                                            set {
                                                file_name := <str>item['file_name'],
                                                file_url := <str>item['file_url']            
                                            }
                                            )
                                          )
                                          )
                            }
                        """, board=board, num=num_parsed, title=title_parsed, writer=writer_parsed,
                                 write_date=write_date_parsed, read_count=read_count_parsed,
                                 article_url=article_url_parsed, content=text_parsed, crawled_time=now,
                                 file_data=json.dumps(file_list))

                except edgedb.errors.ConstraintViolationError:
                    client.query("""
                            update dorm
                            filter .article_url = <str>$article_url
                            set {
                                title := <str>$title,
                                writer := <str>$writer,
                                write_date := <cal::local_date>$write_date,
                                read_count := <int64>$read_count,
                                content := <str>$content,
                                crawled_time := <cal::local_datetime>$crawled_time,
                                files := (with
                                          raw_data := <json>$file_data,
                                          for item in json_array_unpack(raw_data) union (
                                            insert Files {
                                                file_name := <str>item['file_name'],
                                                file_url := <str>item['file_url']            
                                            } unless conflict on .file_url else (
                                            update Files
                                            set {
                                                file_name := <str>item['file_name'],
                                                file_url := <str>item['file_url']            
                                            }
                                            )
                                          )
                                          )
                            }
                            """, title=title_parsed, write_date=write_date_parsed,
                                 writer=writer_parsed, read_count=read_count_parsed,
                                 content=text_parsed, crawled_time=now,
                                 article_url=article_url_parsed, file_data=json.dumps(file_list))

            else:
                crawling_log.http_response_error(resp.status, article_url_parsed)
    except (Exception, ClientConnectorError):
        raise ServerRefusedError(data)

    client.close()


async def board_page_crawler(session, board: str, page: int, ignore_date=False):
    board_list = []

    crawling_log.board_crawling_log(board, page)

    url = f"https://dorm.koreatech.ac.kr/content/board/list.php?now_page={page}&GUBN=&SEARCH=&BOARDID={board}"

    date_of_last_article = 0

    try:
        async with session.get(url, headers=headers) as resp:
            # add small delay for avoid ServerDisconnectedError
            await asyncio.sleep(0.01)
            if resp.status == 200:
                html = await resp.text()
                soup = BeautifulSoup(html, 'html.parser')

                posts = soup.select("#board > table > tbody > tr")

                for post in posts:
                    try:
                        num_parsed = post.select_one("td:nth-child(1)").text.strip()
                        article_url_parsed = post.select_one("td:nth-child(2) > a").get('href')
                        article_url_parsed = re.sub("&now_page=\d*", "", article_url_parsed)
                        article_url_parsed = f"https://dorm.koreatech.ac.kr/content/board/{article_url_parsed}"
                        write_date_parsed = post.select_one("td:nth-child(4)").text.strip()
                        write_date_parsed = datetime.strptime(write_date_parsed, '%Y-%m-%d')

                        date_of_last_article = write_date_parsed

                        # If article older than 7 days, pass it
                        if not ignore_date and (datetime.today() - timedelta(days=7) > write_date_parsed):
                            continue

                        board_list.append(Board(
                            board=board,
                            num=num_parsed,
                            article_url=article_url_parsed
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
            board_list.extend(await board_page_crawler(session, board, page + 1))
            return board_list


async def board_crawler(board: str, start_page: int, last_page: int):
    # limit TCPConnector to 10 for avoid ServerDisconnectedError
    # Enable force_close to disable HTTP Keep-Alive
    connector = aiohttp.TCPConnector(limit=10, force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        board_list = await board_list_crawler(session, board, start_page, last_page)

        await board_crawler_task(session, board_list)


async def board_list_crawler(session, board: str, start_page: int, last_page: int):
    board_list = []
    failed_page = []

    pages = [asyncio.ensure_future(board_page_crawler(session, board, page, True)) for page in
             range(start_page, last_page + 1)]
    datas = await gather_with_concurrency(100, *pages)
    for data in datas:
        board_list.extend([i for i in data if isinstance(i, Board)])
        failed_page.extend([int(i.data) for i in data if isinstance(i, ServerRefusedError)])

    failed_page.sort()

    if failed_page:
        board_list.extend(await board_list_crawler(session, board, failed_page[0], failed_page[-1]))

    return board_list


async def board_crawler_task(session, board_list):
    tasks = [asyncio.ensure_future(article_parser(session, data)) for data in board_list]
    result = await gather_with_concurrency(100, *tasks)

    failed_data = [i for i in result if i is not None]
    failed_data = [i.data for i in failed_data]

    if failed_data:
        await board_crawler_task(session, failed_data)


async def sched_board_crawler(board: str):
    # limit TCPConnector to 10 for avoid ServerDisconnectedError
    # Enable force_close to disable HTTP Keep-Alive
    connector = aiohttp.TCPConnector(limit=10, force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        board_list = await board_page_crawler(session, board, 1)

        await board_crawler_task(session, board_list)
