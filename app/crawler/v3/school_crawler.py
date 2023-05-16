import json
from datetime import datetime

import edgedb
import requests
from bs4 import BeautifulSoup
import re


def school_parser(board: str, m_code: str, page: int):
    client = edgedb.create_client()
    now = datetime.now()

    url = f"https://www.koreatech.ac.kr/kor/CMS/NoticeMgr/{board}.do?mCode={m_code}&page={page}"
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        html = response.text
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

                article_response = requests.get(article_url_parsed, verify=False)

                if article_response.status_code == 200:
                    html = article_response.text
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
                        file_uri = file.select_one("a")["href"]
                        file_name = file.select_one("a").get_text()
                        file_name = re.sub("\[.*]", "", file_name).strip()

                        file_tuple = (file_name, file_uri)
                        file_list.append(file_tuple)

                    try:
                        client.query("""
                            insert school {
                                board := <str>$board,
                                num := <str>$num,
                                title := <str>$title,
                                writer := <str>$writer,
                                write_date := <cal::local_date>$write_date,
                                read_count := <int64>$read_count,
                                article_url := <str>$article_url,
                                content := <str>$content,
                                crawled_time := <cal::local_datetime>$crawled_time,
                                files := <array<tuple<str, str>>><json>$files
                            }
                        """, board=board, num=num_parsed, title=title_parsed, writer=writer_parsed,
                                     write_date=write_date_parsed, read_count=read_count_parsed,
                                     article_url=article_url_parsed, content=text_parsed, crawled_time=now,
                                     files=json.dumps(file_list))
                    except edgedb.errors.ConstraintViolationError:
                        client.query("""
                            update school
                            filter .article_url = <str>$article_url
                            set {
                                title := <str>$title,
                                write_date := <cal::local_date>$write_date,
                                read_count := <int64>$read_count,
                                content := <str>$content,
                                crawled_time := <cal::local_datetime>$crawled_time,
                                files := <array<tuple<str, str>>><json>$files
                            }
                        """, title=title_parsed, write_date=write_date_parsed, read_count=read_count_parsed,
                                     content=text_parsed, crawled_time=now,
                                     article_url=article_url_parsed, files=json.dumps(file_list))

                else:
                    continue

            except AttributeError:
                continue
    else:
        pass

    client.close()

