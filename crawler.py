import requests
from bs4 import BeautifulSoup
from fastapi.encoders import jsonable_encoder
import re


async def cse_article_parser(board: str, article: int):
    url = f"https://cse.koreatech.ac.kr/index.php?mid={board}&document_srl={article}"
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        data_list = []
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        posts = soup.select("#main-content > div > div > div.board_read")
        for post in posts:
            try:
                title = post.select_one("div.read_header > h1 > a").get_text().strip()
                writer = post.select_one("div.read_header > p.meta > a").get_text().strip()
                text = post.select_one("div.read_body > div:nth-child(1)").decode_contents()

            except AttributeError as e:
                return jsonable_encoder([{"status": "END"}])

            data_dic = {
                'title': title,
                'writer': writer,
                'text': text
            }
            data_list.append(data_dic)

        return jsonable_encoder(data_list)
    else:
        return jsonable_encoder({'status_code': response.status_code})


async def cse_parser(board: str, page: int):
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
                url = post.select_one("td.title > a").get('href')
                article_num = re.findall('(?<=document_srl=)\d+', url)[0]
            except AttributeError as e:
                return jsonable_encoder([{"status": "END"}])

            data_dic = {
                'num': num,
                'title': title,
                'writer': writer,
                'write_date': write_date,
                'read': read,
                'article_num': article_num
            }
            data_list.append(data_dic)

        return jsonable_encoder(data_list)
    else:
        return jsonable_encoder({'status_code': response.status_code})


async def cse_notice(page: int = 1):
    return await cse_parser("notice", page)


async def cse_job_board(page: int = 1):
    return await cse_parser("jobboard", page)


async def cse_free_board(page: int = 1):
    return await cse_parser("freeboard", page)
