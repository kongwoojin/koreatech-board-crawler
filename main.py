from fastapi import Depends, FastAPI
from cse_crawler import *
from school_crawler import *
from dorm_crawler import *
from department_common_crawler import *

app = FastAPI()


@app.get("/cse/notice/")
async def get_cse_notice(params: dict = Depends(cse_notice)):
    return params


@app.get("/cse/job/")
async def get_cse_job_board(params: dict = Depends(cse_job_board)):
    return params


@app.get("/cse/free/")
async def get_cse_free_board(params: dict = Depends(cse_free_board)):
    return params


@app.get("/cse/article/")
async def get_cse_article(params: dict = Depends(cse_article_parser)):
    return params


@app.get("/mechanical/notice/")
async def get_mechanical_notice(params: dict = Depends(mechanical_notice)):
    return params


@app.get("/mechanical/lecture/")
async def get_mechanical_lecture_notice(params: dict = Depends(mechanical_lecture_notice)):
    return params


@app.get("/mechanical/free/")
async def get_mechanical_free_board(params: dict = Depends(mechanical_free_board)):
    return params


@app.get("/mechanical/article/")
async def get_mechanical_article(params: dict = Depends(department_common_article_parser)):
    return params


@app.get("/mechatronics/notice/")
async def get_mechanical_notice(params: dict = Depends(mechatronics_notice)):
    return params


@app.get("/mechatronics/lecture/")
async def get_mechanical_lecture_notice(params: dict = Depends(mechatronics_lecture_notice)):
    return params


@app.get("/mechatronics/bachelor/")
async def get_mechanical_bachelor_notice(params: dict = Depends(mechatronics_bachelor_notice)):
    return params


@app.get("/mechatronics/job/")
async def get_mechanical_job_notice(params: dict = Depends(mechatronics_job_notice)):
    return params


@app.get("/mechatronics/free/")
async def get_mechanical_free_board(params: dict = Depends(mechatronics_free_board)):
    return params


@app.get("/mechatronics/article/")
async def get_mechanical_article(params: dict = Depends(department_common_article_parser)):
    return params


@app.get("/ite/notice/")
async def get_ite_notice(params: dict = Depends(ite_notice)):
    return params


@app.get("/ite/article/")
async def get_ite_article(params: dict = Depends(department_common_article_parser)):
    return params


@app.get("/ide/notice/")
async def get_ide_notice(params: dict = Depends(ide_notice)):
    return params


@app.get("/ide/free/")
async def get_ide_free_board(params: dict = Depends(ide_free_board)):
    return params


@app.get("/ide/article/")
async def get_ide_article(params: dict = Depends(department_common_article_parser)):
    return params


@app.get("/arch/notice/")
async def get_arch_notice(params: dict = Depends(arch_notice)):
    return params


@app.get("/arch/free/")
async def get_arch_free_board(params: dict = Depends(arch_free_board)):
    return params


@app.get("/arch/article/")
async def get_arch_article(params: dict = Depends(department_common_article_parser)):
    return params


@app.get("/emc/notice/")
async def get_emc_notice(params: dict = Depends(emc_notice)):
    return params


@app.get("/emc/article/")
async def get_emc_article(params: dict = Depends(department_common_article_parser)):
    return params


@app.get("/sim/notice/")
async def get_sim_notice(params: dict = Depends(sim_notice)):
    return params


@app.get("/sim/article/")
async def get_sim_article(params: dict = Depends(department_common_article_parser)):
    return params


@app.get("/school/notice/")
async def get_school_general_notice(params: dict = Depends(school_general_notice)):
    return params


@app.get("/school/scholar/")
async def get_school_scholar_notice(params: dict = Depends(school_scholar_notice)):
    return params


@app.get("/school/bachelor/")
async def get_school_bachelor_notice(params: dict = Depends(school_bachelor_notice)):
    return params


@app.get("/school/covid19/")
async def get_school_covid19_notice(params: dict = Depends(school_covid19_notice)):
    return params


@app.get("/school/article/")
async def get_school_article(params: dict = Depends(school_article_parser)):
    return params


@app.get("/dorm/notice/")
async def get_dorm_notice(params: dict = Depends(dorm_notice)):
    return params


@app.get("/dorm/free/")
async def get_dorm_free_board(params: dict = Depends(dorm_free_board)):
    return params


@app.get("/dorm/article/")
async def get_dorm_article(params: dict = Depends(dorm_article_parser)):
    return params
