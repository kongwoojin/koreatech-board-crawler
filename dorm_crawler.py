import requests
from bs4 import BeautifulSoup
from fastapi.encoders import jsonable_encoder
import re
from expiringdict import ExpiringDict

cache = ExpiringDict(max_len=10, max_age_seconds=1800)  # Caching data for 30min and caching <= 10 pages per department


async def dorm_article_parser(url: str):
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        data_list = []
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        try:
            title = soup.select_one(
                "#board > div.boardViewer > h4").get_text().strip()
            writer = soup.select_one(
                "#board > div.boardViewer > table.viewer tr:nth-child(2) > td:nth-child(2)").get_text().strip()
            text = soup.select_one(
                "#board > div.boardViewer > table.viewer div.story").decode_contents()
            date = soup.select_one(
                "#board > div.boardViewer > table.viewer tr:nth-child(2) > td:nth-child(4)").get_text().strip()

        except AttributeError as e:
            return jsonable_encoder([{"status": "END"}])

        text = text.replace("<img", "<br><img")

        files = soup.select("#board > div.boardViewer > table.viewer tr:nth-child(3) > td > a")

        file_list = []
        for file in files:
            file_uri = file["href"]
            file_name = file.get_text()
            file_name = re.sub("\[.*]", "", file_name).strip()

            file_dic = {
                "file_uri": f"https://dorm.koreatech.ac.kr{file_uri}",
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


async def dorm_parser(board: str, page: int, is_second_page: bool = False):
    if not is_second_page:
        page = page * 2 - 1

    if cache.get(f'{board}_{page}') is None:

        url = f"https://dorm.koreatech.ac.kr/content/board/list.php?now_page={page}&GUBN=&SEARCH=&BOARDID={board}"
        response = requests.get(url, verify=False)

        if response.status_code == 200:
            data_list = []
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            posts = soup.select("#board > table > tbody > tr")
            for post in posts:
                try:
                    num = post.select_one("td:nth-child(1)").get_text().strip()
                    title = post.select_one("td:nth-child(2)").get_text().strip()
                    writer = post.select_one("td:nth-child(3)").get_text().strip()
                    write_date = post.select_one("td:nth-child(4)").get_text().strip()
                    if board == "notice":
                        read = post.select_one("td:nth-child(6)").get_text().strip()
                    else:
                        read = post.select_one("td:nth-child(5)").get_text().strip()
                    article_url = post.select_one("td:nth-child(2) > a").get('href')
                except AttributeError as e:
                    return jsonable_encoder([{"status": "END"}])

                data_dic = {
                    'num': num,
                    'title': title,
                    'writer': writer,
                    'write_date': write_date,
                    'read': read,
                    'article_url': f"https://dorm.koreatech.ac.kr/content/board/{article_url}"
                }

                data_list.append(data_dic)

            if page % 2 == 1:
                page += 1
                data_list.extend(await dorm_parser(board, page, True))

            if is_second_page:
                return data_list
            else:
                cache[f'{board}_{page}'] = data_list
                return jsonable_encoder(data_list)
        else:
            return jsonable_encoder({'status_code': response.status_code})
    else:
        return jsonable_encoder(cache[f'{board}_{page}'])


async def dorm_notice(page: int = 1):
    return await dorm_parser("notice", page)


async def dorm_free_board(page: int = 1):
    return await dorm_parser("bulletin", page)
