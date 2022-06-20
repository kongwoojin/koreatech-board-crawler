from fastapi import Depends, FastAPI
from crawler import *

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
