import requests
from bs4 import BeautifulSoup
from fastapi.encoders import jsonable_encoder


async def cse_parser(url: str):
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
            except AttributeError as e:
                return jsonable_encoder([{"status": "END"}])

            data_dic = {
                'num': num,
                'title': title,
                'writer': writer,
                'write_date': write_date,
                'read': read,
                'url': url
            }
            data_list.append(data_dic)

        return jsonable_encoder(data_list)
    else:
        return jsonable_encoder({'status_code': response.status_code})


async def cse_notice(page: int = 1):
    url = f"https://cse.koreatech.ac.kr/index.php?mid=notice&page={page}"
    return await cse_parser(url)


async def cse_job_board(page: int = 1):
    url = f"https://cse.koreatech.ac.kr/index.php?mid=jobboard&page={page}"
    return await cse_parser(url)


async def cse_free_board(page: int = 1):
    url = f"https://cse.koreatech.ac.kr/index.php?mid=freeboard&page={page}"
    return await cse_parser(url)
