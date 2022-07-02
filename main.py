from fastapi import Depends, FastAPI
from cse_crawler import *
from school_crawler import *

app = FastAPI()


@app.get("/cse/notice/")
async def get_cse_notice(params: dict = Depends(cse_notice)):
    return params


@app.get("/cse/job/")
async def get_cse_job(params: dict = Depends(cse_job_board)):
    return params


@app.get("/cse/free/")
async def get_cse_free(params: dict = Depends(cse_free_board)):
    return params


@app.get("/cse/article/")
async def get_cse_article(params: dict = Depends(cse_article_parser)):
    return params


@app.get("/school/notice/")
async def get_school_notice(params: dict = Depends(school_general_notice)):
    return params


@app.get("/school/scholar/")
async def get_school_notice(params: dict = Depends(school_scholar_notice)):
    return params


@app.get("/school/bachelor/")
async def get_school_notice(params: dict = Depends(school_bachelor_notice)):
    return params


@app.get("/school/covid19/")
async def get_school_notice(params: dict = Depends(school_covid19_notice)):
    return params


@app.get("/school/article/")
async def get_school_notice(params: dict = Depends(school_article_parser)):
    return params
