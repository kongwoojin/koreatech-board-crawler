import requests
from bs4 import BeautifulSoup
from fastapi.encoders import jsonable_encoder
import re
from expiringdict import ExpiringDict

cache = ExpiringDict(max_len=10, max_age_seconds=300)  # Caching data for 5min and caching <= 10 pages per department


async def cse_article_parser(url: str):
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        data_list = []
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        try:
            title = soup.select_one(
                "#main-content > div > div > div.board_read > div.read_header > h1 > a").get_text().strip()
            writer = soup.select_one(
                "#main-content > div > div > div.board_read > div.read_header > p.meta > a").get_text().strip()
            text = soup.select_one(
                "#main-content > div > div > div.board_read > div.read_body > div:nth-child(1)").decode_contents()
            date = soup.select_one(
                "#main-content > div > div > div.board_read > div.read_header > p.time").get_text().strip()

        except AttributeError as e:
            return jsonable_encoder([{"status": "END"}])

        text = text.replace("<img", "<br><img")

        files = soup.select("#main-content > div > div > div.board_read > div.read_footer > div.fileList > ul > li")

        file_list = []
        for file in files:
            file_uri = file.select_one("a")["href"]
            file_name = file.select_one("a").get_text()
            file_name = re.sub("\[File.*]", "", file_name).strip()

            file_dic = {
                "file_uri": file_uri,
                "file_name": file_name
            }

            file_list.append(file_dic)

        data_dic = {
            'title': title,
            'writer': writer,
            'text': text,
            'date': date,
            'files': file_list
        }
        data_list.append(data_dic)

        return jsonable_encoder(data_list)
    else:
        return jsonable_encoder({'status_code': response.status_code})


async def cse_parser(board: str, page: int):

    if cache.get(f'{board}_{page}') is None:
        url = f"https://cse.koreatech.ac.kr/index.php?mid={board}&page={page}"
        response = requests.get(url, verify=False)

        if response.status_code == 200:
            data_list = []
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            posts = soup.select("#board_list > table > tbody > tr")
            for post in posts:
                try:
                    num = post.select_one("td:nth-child(1)").get_text().strip()
                    title = post.select_one("td.title > a").get_text().strip()
                    writer = post.select_one("td.author").get_text().strip()
                    write_date = post.select_one("td.time").get_text().strip()
                    read = post.select_one("td.readNum").get_text().strip()
                    article_url = post.select_one("td.title > a").get('href')
                except AttributeError as e:
                    return jsonable_encoder([{"status": "END"}])

                data_dic = {
                    'num': num,
                    'title': title,
                    'writer': writer,
                    'write_date': write_date,
                    'read': read,
                    'article_url': article_url
                }
                data_list.append(data_dic)

            cache[f'{board}_{page}'] = data_list
            return jsonable_encoder(data_list)
        else:
            return jsonable_encoder({'status_code': response.status_code})
    else:
        return jsonable_encoder(cache[f'{board}_{page}'])


async def cse_notice(page: int = 1):
    return await cse_parser("notice", page)


async def cse_job_board(page: int = 1):
    return await cse_parser("jobboard", page)


async def cse_free_board(page: int = 1):
    return await cse_parser("freeboard", page)


async def cse_pds(page: int = 1):
    return await cse_parser("pds", page)
