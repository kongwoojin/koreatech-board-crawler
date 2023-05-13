from fastapi import APIRouter, Depends
from api.crawler.v2.department_common_crawler import *

router = APIRouter(
    prefix="/v2/arch",
    tags=["arch"],
    responses={404: {"description": "Not found"}},
)


@router.get("/notice/")
async def get_arch_notice(params: dict = Depends(arch_notice)):
    return params


@router.get("/free/")
async def get_arch_free_board(params: dict = Depends(arch_free_board)):
    return params


@router.get("/article/")
async def get_arch_article(params: dict = Depends(department_common_article_parser)):
    return params
