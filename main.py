from fastapi import Depends, FastAPI
from cse_crawler import *
from school_crawler import *
from dorm_crawler import *

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
