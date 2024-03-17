import asyncio

from app.crawler.v3 import dorm_crawler, school_crawler, common_crawler
from app.dataclass.enums.department import Department


async def main_common_crawler():
    # Remove Department.ACE because not logged-in user can't access the board
    departmentList = [Department.ARCH, Department.CSE, Department.MSE, Department.IDE, Department.ITE,
                      Department.MECHANICAL, Department.MECHATRONICS, Department.SIM]
    for department in departmentList:
        for index in range(0, department.board_len()):
            await common_crawler.sched_board_crawler(department, index)


async def main_school_crawler():
    department = Department.SCHOOL
    for index in range(0, department.board_len()):
        await school_crawler.sched_board_crawler(department, index)


async def main_dorm_crawler():
    department = Department.DORM
    for index in range(0, department.board_len()):
        await dorm_crawler.sched_board_crawler(department, index)


async def main_crawler():
    await asyncio.gather(
        main_school_crawler(),
        main_dorm_crawler(),
        main_common_crawler()
    )

