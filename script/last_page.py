import re

import aiohttp
from bs4 import BeautifulSoup

from app.logs import crawling_log


async def get_cse_last_page(board):
    async with (aiohttp.ClientSession() as session):
        async with session.get(f"https://cse.koreatech.ac.kr/index.php?mid={board}") as resp:
            if resp.status == 200:
                html = await resp.text()
                soup = BeautifulSoup(html, 'html.parser')

                try:
                    page = soup.select_one("a.direction:nth-child(12)").get("href").replace(
                        "https://cse.koreatech.ac.kr/index.php?mid=notice&page=", "")

                    return int(page) + 1

                except AttributeError:
                    crawling_log.unknown_last_page_error(board)
                    return 1
            else:
                crawling_log.http_response_error(resp.status, board)
                return 1


async def get_common_last_page(department, board_num):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://cms3.koreatech.ac.kr/bbs/{department}/{board_num}/artclList.do") as resp:
            if resp.status == 200:
                html = await resp.text()
                soup = BeautifulSoup(html, 'html.parser')

                try:
                    page = soup.select_one("a._last").get("href")

                    pattern = r"javascript:page_link\('(\d+)'\)"

                    match = re.search(pattern, page)

                    return int(match.group(1)) + 1

                except AttributeError:
                    crawling_log.unknown_last_page_error(board_num)
                    return 1
            else:
                crawling_log.http_response_error(resp.status, board_num)
                return 1


async def get_school_last_page(board, m_code):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.koreatech.ac.kr/kor/CMS/NoticeMgr/{board}.do?mCode={m_code}") as resp:
            if resp.status == 200:
                html = await resp.text()
                soup = BeautifulSoup(html, 'html.parser')

                try:
                    page = soup.select_one(".lastpage").get("href").replace("?robot=Y&mCode=MN230&page=", "")

                    return int(page) + 1

                except AttributeError:
                    crawling_log.unknown_last_page_error(board)
                    return 1
            else:
                crawling_log.http_response_error(resp.status, board)
                return 1


async def get_dorm_last_page(board):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"https://dorm.koreatech.ac.kr/content/board/list.php?now_page=&GUBN=&SEARCH=&BOARDID={board}") as resp:
            if resp.status == 200:
                html = await resp.text()
                soup = BeautifulSoup(html, 'html.parser')

                try:
                    page = soup.select_one(".paging > li:nth-child(6) > a:nth-child(1)").get("href")

                    pattern = r"now_page=(\d+)"

                    match = re.search(pattern, page)

                    return int(match.group(1)) + 1

                except AttributeError:
                    crawling_log.unknown_last_page_error(board)
                    return 1
            else:
                crawling_log.http_response_error(resp.status, board)
                return 1
