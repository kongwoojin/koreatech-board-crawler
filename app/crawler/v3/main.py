import asyncio

from app.crawler.v3 import arch_crawler, cse_crawler, dorm_crawler, emc_crawler, ide_crawler, ite_crawler, \
    mechanical_crawler, mechatronics_crawler, school_crawler, sim_crawler


async def main_arch_crawler():
    for board in [340, 341]:
        await arch_crawler.sched_board_crawler(board)


async def main_cse_crawler():
    for board in ["notice", "jobboard", "freeboard", "pds"]:
        await cse_crawler.sched_board_crawler(board)


async def main_dorm_crawler():
    for board in ["notice", "bulletin"]:
        await dorm_crawler.sched_board_crawler(board)


async def main_emc_crawler():
    for board in [541]:
        await emc_crawler.sched_board_crawler(board)


async def main_ide_crawler():
    for board in [330, 332]:
        await ide_crawler.sched_board_crawler(board)


async def main_ite_crawler():
    for board in [247]:
        await ite_crawler.sched_board_crawler(board)


async def main_mechanical_crawler():
    for board in [229, 232]:
        await mechanical_crawler.sched_board_crawler(board)


async def main_mechatronics_crawler():
    for board in [235, 236, 237, 238, 244]:
        await mechatronics_crawler.sched_board_crawler(board)


async def main_school_crawler():
    for board, m_code in [("list", "MN230"), ("scholarList", "MN231"), ("bachelorList", "MN233"),
                          ("boardList8", "MN427")]:
        await school_crawler.sched_board_crawler(board, m_code)


async def main_sim_crawler():
    for board in [373]:
        await sim_crawler.sched_board_crawler(board)


async def main_crawler():
    await asyncio.gather(
        main_cse_crawler(),  # 4
        main_school_crawler(),  # 4
        main_dorm_crawler(),  # 2
        main_arch_crawler(),  # 2
        main_mechatronics_crawler(),  # 5
        main_mechanical_crawler(),  # 3
        main_ide_crawler(),  # 2
        main_emc_crawler(),  # 1
        main_ite_crawler(),  # 1
        main_sim_crawler(),  # 1
    )

