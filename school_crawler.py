import requests
from bs4 import BeautifulSoup
from fastapi.encoders import jsonable_encoder
import re


async def school_article_parser(url: str):
    url = f"https://koreatech.ac.kr/{url}"
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        data_list = []
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        try:
            title = soup.select_one(
                "#board-wrap > div.board-view-head > div.board-view-title > h4 > span").get_text().strip()
            writer = soup.select_one(
                "#board-wrap > div.board-view-head > div.board-view-title > div > span.txt.name").get_text().strip()
            text = soup.select_one(
                "#boardContents").decode_contents()
            date = soup.select_one(
                "#board-wrap > div.board-view-head > div.board-view-title > div > span:nth-child(2)").get_text().strip()

        except AttributeError as e:
            return jsonable_encoder([{"status": "END"}])

        text = text.replace("<img", "<br><img")

        files = soup.select("#board-wrap > div.board-view-head > div.board-view-winfo > div > ul > li")

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
        data_list.append(data_dic)

        return jsonable_encoder(data_list)
    else:
        return jsonable_encoder({'status_code': response.status_code})


async def school_parser(board: str, m_code: str, page: int):
    url = f"https://www.koreatech.ac.kr/kor/CMS/NoticeMgr/{board}.do?mCode={m_code}&page={page}"
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        data_list = []
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        posts = soup.select("#board-wrap > div.board-list-wrap > table > tbody > tr")
        for post in posts:
            try:
                num = post.select_one("td.num:nth-child(1)").get_text().strip()
                if board == "list" and m_code == "MN230":
                    notice_type = post.select_one("td:nth-child(2)").get_text().strip()
                title = post.select_one("td.subject").get_text().strip()
                writer = post.select_one("td.writer").get_text().strip()
                write_date = post.select_one("td.date").get_text().strip()
                read = post.select_one("td.cnt").get_text().strip()
                article_url = post.select_one("td.subject > a").get('href')
            except AttributeError as e:
                return jsonable_encoder([{"status": "END"}])

            if board == "list" and m_code == "MN230":
                data_dic = {
                    'num': num,
                    'notice_type': notice_type,
                    'title': title,
                    'writer': writer,
                    'write_date': write_date,
                    'read': read,
                    'article_url': article_url
                }
            else:
                data_dic = {
                    'num': num,
                    'title': title,
                    'writer': writer,
                    'write_date': write_date,
                    'read': read,
                    'article_url': article_url
                }

            data_list.append(data_dic)

        return jsonable_encoder(data_list)
    else:
        return jsonable_encoder({'status_code': response.status_code})


async def school_general_notice(page: int = 1):
    return await school_parser("list", "MN230", page)


async def school_scholar_notice(page: int = 1):
    return await school_parser("scholarList", "MN231", page)


async def school_bachelor_notice(page: int = 1):
    return await school_parser("bachelorList", "MN233", page)


async def school_covid19_notice(page: int = 1):
    return await school_parser("boardList8", "MN427", page)
