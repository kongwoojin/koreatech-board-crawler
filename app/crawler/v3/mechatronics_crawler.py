import json

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import edgedb


def mechatronics_parser(board_num: int, page: int):
    client = edgedb.create_client()
    now = datetime.now()

    requests.packages.urllib3.disable_warnings()
    url = f"https://cms3.koreatech.ac.kr/bbs/mechatronics/{board_num}/artclList.do?page={page}"

    response = requests.get(url, verify=False)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        posts = soup.select("table.artclTable > tbody > tr")
        for post in posts:
            try:
                num_parsed = post.select_one("td._artclTdNum").get_text().strip()
                writer_parsed = post.select_one("td._artclTdWriter").get_text().strip()
                write_date_parsed = post.select_one("td._artclTdRdate").get_text().strip()
                write_date_parsed = datetime.strptime(write_date_parsed, '%Y.%m.%d')
                article_url_parsed = post.select_one("td._artclTdTitle > a").get('href')
                article_url_parsed = f"https://cms3.koreatech.ac.kr{article_url_parsed}"
                read_count_parsed = int(post.select_one("td._artclTdAccess").get_text().strip())

                article_response = requests.get(article_url_parsed, verify=False)

                if article_response.status_code == 200:
                    html = article_response.text
                    soup = BeautifulSoup(html, 'html.parser')
                    try:
                        title_parsed = post.select_one("td._artclTdTitle > a").get_text().strip().replace("\n", "") \
                            .replace("\t", "").replace("［", "[").replace("］", "]")
                        text_parsed = soup.select_one(
                            "div.artclView").decode_contents()
                        text_parsed = text_parsed.replace("<img", "<br><img")

                    except AttributeError:
                        continue

                    files = soup.select("div.artclItem.viewForm > dl > dd > ul > li")

                    file_list = []
                    for file in files:
                        try:
                            file_uri = file.select_one("a")["href"]
                            file_name = file.select_one("a").get_text()
                            file_name = re.sub("\[.*]", "", file_name).strip()
                        except AttributeError:
                            continue

                        file_dic = {
                            "file_uri": file_uri,
                            "file_name": file_name
                        }

                        file_list.append(file_dic)

                    board = str(board_num)

                    try:
                        client.query("""
                            insert mechatronics {
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
                                              file_uri := <str>item['file_uri']            
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
                            update mechatronics
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
                                                file_uri := <str>item['file_uri']            
                                            } unless conflict on .file_uri else (
                                            update Files
                                            set {
                                                file_name := <str>item['file_name'],
                                                file_uri := <str>item['file_uri']            
                                            }
                                            )
                                          )
                                          )
                            }
                        """, title=title_parsed, write_date=write_date_parsed, read_count=read_count_parsed,
                                     content=text_parsed, crawled_time=now,
                                     article_url=article_url_parsed, file_data=json.dumps(file_list))

            except AttributeError:
                # If attribute error faced, It means the article is blinded.
                # So, Just get next one.
                continue

    else:
        pass

    client.close()
