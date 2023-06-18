import json
import re

import asyncio

import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import edgedb

from app.crawler.v3 import headers
from app.dataclass.board import Board
from app.logs import crawling_log


async def article_parser(session, data: Board):
    client = edgedb.create_client()
    now = datetime.now()

    num_parsed = data.num
    board = data.board
    article_url_parsed = data.article_url
    writer_parsed = data.writer

    crawling_log.article_crawling_log(data)

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

            try:
                client.query("""
                            insert mechanical {
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
                        """, board=str(board), num=num_parsed, title=title_parsed, writer=writer_parsed,
                             write_date=write_date_parsed, read_count=read_count_parsed,
                             article_url=article_url_parsed, content=text_parsed, crawled_time=now,
                             file_data=json.dumps(file_list))

            except edgedb.errors.ConstraintViolationError:
                client.query("""
                            update mechanical
                            filter .article_url = <str>$article_url
                            set {
                                title := <str>$title,
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
                             read_count=read_count_parsed,
                             content=text_parsed, crawled_time=now,
                             article_url=article_url_parsed, file_data=json.dumps(file_list))

        else:
            crawling_log.http_response_error(resp.status, article_url_parsed)

    client.close()


async def board_page_crawler(session, board_num: int, page: int, ignore_date=False):
    board_list = []

    crawling_log.board_crawling_log(board_num, page)

    url = f"https://cms3.koreatech.ac.kr/bbs/me/{board_num}/artclList.do?page={page}"

    date_of_last_article = 0

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

    if ignore_date:
        return board_list
    else:
        if datetime.today() - timedelta(days=7) > date_of_last_article:
            return board_list
        else:
            board_list.extend(await board_page_crawler(session, board_num + 1, page))
            return board_list


async def board_crawler(board_num: int, start_page: int, last_page: int):
    board_list = []

    # limit TCPConnector to 10 for avoid ServerDisconnectedError
    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        pages = [asyncio.ensure_future(board_page_crawler(session, board_num, page)) for page in
                 range(start_page, last_page + 1)]
        datas = await asyncio.gather(*pages)
        for data in datas:
            board_list.extend(data)

        tasks = [asyncio.ensure_future(article_parser(session, data)) for data in board_list]
        await asyncio.gather(*tasks)


async def board_crawler(board_num: int, start_page: int, last_page: int):
    board_list = []

    # limit TCPConnector to 10 for avoid ServerDisconnectedError
    # Enable force_close to disable HTTP Keep-Alive
    connector = aiohttp.TCPConnector(limit=10, force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        pages = [asyncio.ensure_future(board_page_crawler(session, board_num, page, True)) for page in
                 range(start_page, last_page + 1)]
        datas = await asyncio.gather(*pages)
        for data in datas:
            board_list.extend(data)

        tasks = [asyncio.ensure_future(article_parser(session, data)) for data in board_list]
        await asyncio.gather(*tasks)


async def sched_board_crawler(board_num: int):
    # limit TCPConnector to 10 for avoid ServerDisconnectedError
    # Enable force_close to disable HTTP Keep-Alive
    connector = aiohttp.TCPConnector(limit=10, force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        board_list = await board_page_crawler(session, board_num, 1)

        tasks = [asyncio.ensure_future(article_parser(session, data)) for data in board_list]
        await asyncio.gather(*tasks)
