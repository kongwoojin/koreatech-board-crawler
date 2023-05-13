from fastapi import APIRouter, Depends
from api.crawler.v2.department_common_crawler import *

router = APIRouter(
    prefix="/v2/mechanical",
    tags=["mechanical"],
    responses={404: {"description": "Not found"}},
)

@router.get("/notice/")
async def get_mechanical_notice(params: dict = Depends(mechanical_notice)):
    return params


@router.get("/lecture/")
async def get_mechanical_lecture_notice(params: dict = Depends(mechanical_lecture_notice)):
    return params


@router.get("/free/")
async def get_mechanical_free_board(params: dict = Depends(mechanical_free_board)):
    return params


@router.get("/article/")
async def get_mechanical_article(params: dict = Depends(department_common_article_parser)):
    return params
