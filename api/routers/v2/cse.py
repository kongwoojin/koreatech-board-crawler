from fastapi import APIRouter, Depends
from api.crawler.v2.cse_crawler import *

router = APIRouter(
    prefix="/v2/cse",
    tags=["cse"],
    responses={404: {"description": "Not found"}},
)


@router.get("/notice/")
async def get_cse_notice(params: dict = Depends(cse_notice)):
    return params


@router.get("/job/")
async def get_cse_job_board(params: dict = Depends(cse_job_board)):
    return params


@router.get("/free/")
async def get_cse_free_board(params: dict = Depends(cse_free_board)):
    return params


@router.get("/pds/")
async def get_cse_pds(params: dict = Depends(cse_pds)):
    return params


@router.get("/article/")
async def get_cse_article(params: dict = Depends(cse_article_parser)):
    return params
