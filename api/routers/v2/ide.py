from fastapi import APIRouter, Depends
from api.crawler.v2.department_common_crawler import *

router = APIRouter(
    prefix="/v2/ide",
    tags=["ide"],
    responses={404: {"description": "Not found"}},
)


@router.get("/notice/")
async def get_ide_notice(params: dict = Depends(ide_notice)):
    return params


@router.get("/free/")
async def get_ide_free_board(params: dict = Depends(ide_free_board)):
    return params


@router.get("/article/")
async def get_ide_article(params: dict = Depends(department_common_article_parser)):
    return params
