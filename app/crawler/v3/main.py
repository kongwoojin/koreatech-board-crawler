from app.crawler.v3 import arch_crawler, cse_crawler, dorm_crawler, emc_crawler, ide_crawler, ite_crawler, \
    mechanical_crawler, mechatronics_crawler, school_crawler, sim_crawler


def main_arch_crawler():
    for board in [340, 341]:
        for page in range(1, 3):
            arch_crawler.arch_parser(board, page)


def main_cse_crawler():
    for board in ["notice", "jobboard", "freeboard", "pds"]:
        for page in range(1, 3):
            cse_crawler.cse_parser(board, page)


def main_dorm_crawler():
    for board in ["notice", "bulletin"]:
        for page in range(1, 3):
            dorm_crawler.dorm_parser(board, page)


def main_emc_crawler():
    for board in [541]:
        for page in range(1, 3):
            emc_crawler.emc_parser(board, page)


def main_ide_crawler():
    for board in [330, 332]:
        for page in range(1, 3):
            ide_crawler.ide_parser(board, page)


def main_ite_crawler():
    for board in [247]:
        for page in range(1, 3):
            ite_crawler.ite_parser(board, page)


def main_mechanical_crawler():
    for board in [229, 230, 232]:
        for page in range(1, 3):
            mechanical_crawler.mechanical_parser(board, page)


def main_mechatronics_crawler():
    for board in [235, 236, 237, 238, 244]:
        for page in range(1, 3):
            mechatronics_crawler.mechatronics_parser(board, page)


def main_school_crawler():
    for board, m_code in [("list", "MN230"), "scholarList", "MN231", "bachelorList", "MN233", "boardList8", "MN427"]:
        for page in range(1, 3):
            school_crawler.school_parser(board, m_code, page)


def main_sim_crawler():
    for board in [373]:
        for page in range(1, 3):
            sim_crawler.sim_parser(board, page)


def main_crawler_one():
    main_cse_crawler()  # 4
    main_school_crawler()  # 4
    main_dorm_crawler()  # 2
    main_arch_crawler()  # 2


def main_crawler_two():
    main_mechatronics_crawler()  # 5
    main_mechanical_crawler()  # 3
    main_ide_crawler()  # 2
    main_emc_crawler()  # 1
    main_ite_crawler()  # 1
    main_sim_crawler()  # 1
