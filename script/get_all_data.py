import asyncio

from app.crawler.v3 import arch_crawler, cse_crawler, dorm_crawler, emc_crawler, ide_crawler, ite_crawler, \
    mechanical_crawler, mechatronics_crawler, school_crawler, sim_crawler
from script.last_page import get_common_last_page, get_cse_last_page, get_dorm_last_page, get_school_last_page


async def main_arch_crawler():
    for board in [340, 341]:
        for i in range(1, await get_common_last_page("arch", board)):
            await arch_crawler.board_crawler(board, i, i)


async def main_cse_crawler():
    for board in ["notice", "jobboard", "freeboard", "pds"]:
        for i in range(1, await get_cse_last_page(board)):
            await cse_crawler.board_crawler(board, i, i)


async def main_dorm_crawler():
    for board in ["notice", "bulletin"]:
        for i in range(1, await get_dorm_last_page(board)):
            await dorm_crawler.board_crawler(board, i, i)


async def main_emc_crawler():
    for board in [541]:
        for i in range(1, await get_common_last_page("emc", board)):
            await emc_crawler.board_crawler(board, i, i)


async def main_ide_crawler():
    for board in [330, 332]:
        for i in range(1, await get_common_last_page("ide", board)):
            await ide_crawler.board_crawler(board, i, i)


async def main_ite_crawler():
    for board in [247]:
        for i in range(1, await get_common_last_page("ite", board)):
            await ite_crawler.board_crawler(board, i, i)


async def main_mechanical_crawler():
    for board in [229]:
        for i in range(1, await get_common_last_page("me", board)):
            await mechanical_crawler.board_crawler(board, i, i)


async def main_mechatronics_crawler():
    for board in [235, 236, 237, 238, 244]:
        for i in range(1, await get_common_last_page("mechatronics", board)):
            await mechatronics_crawler.board_crawler(board, i, i)


async def main_school_crawler():
    for board, m_code in [("list", "MN230"), ("scholarList", "MN231"), ("bachelorList", "MN233"), ("boardList8", "MN427")]:
        for i in range(1, await get_school_last_page(board, m_code)):
            await school_crawler.board_crawler(board, m_code, i, i)


async def main_sim_crawler():
    for board in [373]:
        for i in range(1, await get_common_last_page("sim", board)):
            await sim_crawler.board_crawler(board, i, i)


async def start_crawler():
    await main_arch_crawler()
    await main_cse_crawler()
    await main_dorm_crawler()
    await main_mechatronics_crawler()
    await main_mechanical_crawler()
    await main_ide_crawler()
    await main_emc_crawler()
    await main_ite_crawler()
    await main_sim_crawler()
    await main_school_crawler()


asyncio.run(start_crawler())
