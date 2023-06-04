import json

import aiohttp
from bs4 import BeautifulSoup
import re
from datetime import datetime
import edgedb


async def dorm_parser(board: str, page: int):
    client = edgedb.create_client()
    now = datetime.now()

    url = f"https://dorm.koreatech.ac.kr/content/board/list.php?now_page={page}&GUBN=&SEARCH=&BOARDID={board}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                html = await resp.text()
                soup = BeautifulSoup(html, 'html.parser')

                posts = soup.select("#board > table > tbody > tr")
                for post in posts:
                    try:
                        num_parsed = post.select_one("td:nth-child(1)").get_text().strip()
                        writer_parsed = post.select_one("td:nth-child(3)").get_text().strip()
                        write_date_parsed = post.select_one("td:nth-child(4)").get_text().strip()
                        write_date_parsed = datetime.strptime(write_date_parsed, '%Y-%m-%d')
                        if board == "notice":
                            read_count_parsed = post.select_one("td:nth-child(6)").get_text().strip()
                        else:
                            read_count_parsed = post.select_one("td:nth-child(5)").get_text().strip()
                        read_count_parsed = int(read_count_parsed)
                        article_url_parsed = post.select_one("td:nth-child(2) > a").get('href')
                        article_url_parsed = re.sub("&now_page=\d*", "", article_url_parsed)
                        article_url_parsed = f"https://dorm.koreatech.ac.kr/content/board/{article_url_parsed}"

                    except AttributeError:
                        continue

                    async with session.get(article_url_parsed) as article_resp:
                        if article_resp.status == 200:
                            html = article_resp.text
                            soup = BeautifulSoup(html, 'html.parser')
                            try:
                                title_parsed = soup.select_one(
                                    "#board > div.boardViewer > h4").get_text().strip()
                                text_parsed = soup.select_one(
                                    "#board > div.boardViewer > table.viewer div.story").decode_contents()
                                text_parsed = text_parsed.replace("<img", "<br><img")

                            except AttributeError:
                                continue

                            files = soup.select("#board > div.boardViewer > table.viewer tr:nth-child(3) > td > a")

                            file_list = []
                            for file in files:
                                file_url = file["href"]
                                file_name = file.get_text()
                                file_name = re.sub("\[.*]", "", file_name).strip()

                                file_dic = {
                                    "file_url": f'https://dorm.koreatech.ac.kr{file_url}',
                                    "file_name": file_name
                                }

                                file_list.append(file_dic)

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
                                                        }
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
                                """, title=title_parsed, write_date=write_date_parsed, read_count=read_count_parsed,
                                             content=text_parsed, crawled_time=now,
                                             article_url=article_url_parsed, file_data=json.dumps(file_list))
            else:
                pass

    client.close()
