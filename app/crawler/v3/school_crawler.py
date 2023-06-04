import json
from datetime import datetime

import aiohttp
import edgedb
from bs4 import BeautifulSoup
import re


async def school_parser(board: str, m_code: str, page: int):
    client = edgedb.create_client()
    now = datetime.now()

    url = f"https://www.koreatech.ac.kr/kor/CMS/NoticeMgr/{board}.do?mCode={m_code}&page={page}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                html = await resp.text()
                soup = BeautifulSoup(html, 'html.parser')

                posts = soup.select("#board-wrap > div.board-list-wrap > table > tbody > tr")
                for post in posts:
                    try:
                        num_parsed = post.select_one("td.num:nth-child(1)").get_text().strip()
                        writer_parsed = post.select_one("td.writer").get_text().strip()
                        write_date_parsed = post.select_one("td.date").get_text().strip()
                        write_date_parsed = datetime.strptime(write_date_parsed, '%Y.%m.%d')
                        read_count_parsed = int(post.select_one("td.cnt").get_text().strip())
                        article_url_parsed = post.select_one("td.subject > a").get('href')
                        article_url_parsed = f"https://koreatech.ac.kr{article_url_parsed}"

                        try:
                            importance_img = post.select_one("td.subject > img")
                            if importance_img.get("src") == "/resources/_Img/Board/default/ico_notice.gif":
                                is_importance = True
                            else:
                                is_importance = False
                        except AttributeError:
                            is_importance = False

                        async with session.get(article_url_parsed) as article_resp:
                            if article_resp.status == 200:
                                html = await article_resp.text()
                                soup = BeautifulSoup(html, 'html.parser')
                                try:
                                    title_parsed = soup.select_one(
                                        "#board-wrap > div.board-view-head > div.board-view-title > h4 > span").get_text().strip()
                                    text_parsed = soup.select_one(
                                        "#boardContents").decode_contents()
                                    text_parsed = text_parsed.replace("<img", "<br><img")

                                except AttributeError:
                                    continue

                                files = soup.select("#board-wrap > div.board-view-head > div.board-view-winfo > div > ul > li")

                                file_list = []
                                for file in files:
                                    file_url = file.select_one("a")["href"]
                                    file_name = file.select_one("a").get_text()
                                    file_name = re.sub("\[.*]", "", file_name).strip()

                                    file_dic = {
                                        "file_url": f'https://cms3.koreatech.ac.kr{file_url}',
                                        "file_name": file_name
                                    }

                                    file_list.append(file_dic)

                                try:
                                    client.query("""
                                        insert school {
                                            board := <str>$board,
                                            num := <str>$num,
                                            is_importance := <bool>$is_importance,
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
                                                 file_data=json.dumps(file_list), is_importance=is_importance)

                                except edgedb.errors.ConstraintViolationError:
                                    client.query("""
                                        update school
                                        filter .article_url = <str>$article_url
                                        set {
                                            title := <str>$title,
                                            is_importance := <bool>$is_importance,
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
                                                 article_url=article_url_parsed, file_data=json.dumps(file_list),
                                                 is_importance=is_importance)

                            else:
                                continue

                    except AttributeError:
                        continue
            else:
                pass

    client.close()

