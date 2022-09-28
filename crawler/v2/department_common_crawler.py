import requests
from bs4 import BeautifulSoup
from fastapi.encoders import jsonable_encoder
import re
import math


async def department_common_article_parser(url: str):
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        try:
            title = soup.select_one(
                "h2.artclViewTitle").get_text().strip().replace("［", "[").replace("］", "]")
            writer = soup.select_one(
                "body > div > div.artclViewHead > div.right > dl:nth-child(3) > dd").get_text().strip()
            text = soup.select_one(
                "div.artclView").decode_contents()
            date = soup.select_one(
                "body > div > div.artclViewHead > div.right > dl:nth-child(1) > dd").get_text().strip()

        except AttributeError as e:
            return jsonable_encoder([{"status": "END"}])

        text = text.replace("<img", "<br><img")

        files = soup.select("div.artclItem.viewForm > dl > dd > ul > li")

        file_list = []
        for file in files:
            file_uri = file.select_one("a")["href"]
            file_name = file.select_one("a").get_text()
            file_name = re.sub("\[.*]", "", file_name).strip()

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

        return jsonable_encoder(data_dic)
    else:
        return jsonable_encoder({'status_code': response.status_code})


async def department_common_parser(department: str, board_num: int, page: int, is_second_page: bool = False):
    if not is_second_page:
        page = page * 2 - 1

    url = f"https://cms3.koreatech.ac.kr/bbs/{department}/{board_num}/artclList.do?page={page}"

    response = requests.get(url, verify=False)

    if response.status_code == 200:
        data_list = []
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        if not is_second_page:
            try:
                last_page = soup.select_one("a._last").get('href')
                last_page = re.search("(?<=javascript:page_link\(')\d*", last_page).group(0)
                last_page = int(last_page)
                last_page = math.ceil(last_page / 2)
            except AttributeError:
                return jsonable_encoder({'last_page': -1, 'posts': []})

        posts = soup.select("table.artclTable > tbody > tr")
        for post in posts:
            try:
                if is_second_page and post.has_attr('class') and 'headline' in post['class']:
                    continue

                num = post.select_one("td._artclTdNum").get_text().strip()
                title = post.select_one("td._artclTdTitle > a").get_text().strip().replace("\n", "") \
                    .replace("\t", "").replace("［", "[").replace("］", "]")
                writer = post.select_one("td._artclTdWriter").get_text().strip()
                write_date = post.select_one("td._artclTdRdate").get_text().strip()
                read = post.select_one("td._artclTdAccess").get_text().strip()
                article_url = post.select_one("td._artclTdTitle > a").get('href')

                data_dic = {
                    'num': num,
                    'title': title,
                    'writer': writer,
                    'write_date': write_date,
                    'read': read,
                    'article_url': f"https://cms3.koreatech.ac.kr{article_url}"
                }
                data_list.append(data_dic)
            except AttributeError:
                return jsonable_encoder({'last_page': -1, 'posts': []})

        if page % 2 == 1:
            page += 1
            data_list.extend(await department_common_parser(department, board_num, page, True))

        if is_second_page:
            return data_list
        else:
            return jsonable_encoder({'last_page': last_page, 'posts': data_list})
    else:
        return jsonable_encoder({'status_code': response.status_code})


async def mechanical_notice(page: int = 1):
    return await department_common_parser("me", 229, page)


async def mechanical_lecture_notice(page: int = 1):
    return await department_common_parser("me", 230, page)


async def mechanical_free_board(page: int = 1):
    return await department_common_parser("me", 232, page)


async def mechatronics_notice(page: int = 1):
    return await department_common_parser("mechatronics", 235, page)


async def mechatronics_lecture_notice(page: int = 1):
    return await department_common_parser("mechatronics", 236, page)


async def mechatronics_bachelor_notice(page: int = 1):
    return await department_common_parser("mechatronics", 237, page)


async def mechatronics_job_notice(page: int = 1):
    return await department_common_parser("mechatronics", 238, page)


async def mechatronics_free_board(page: int = 1):
    return await department_common_parser("mechatronics", 244, page)


async def ite_notice(page: int = 1):
    return await department_common_parser("ite", 247, page)


async def ide_notice(page: int = 1):
    return await department_common_parser("ide", 330, page)


async def ide_free_board(page: int = 1):
    return await department_common_parser("ide", 332, page)


async def arch_notice(page: int = 1):
    return await department_common_parser("arch", 340, page)


async def arch_free_board(page: int = 1):
    return await department_common_parser("arch", 341, page)


async def emc_notice(page: int = 1):
    return await department_common_parser("emc", 541, page)


async def sim_notice(page: int = 1):
    return await department_common_parser("sim", 373, page)
