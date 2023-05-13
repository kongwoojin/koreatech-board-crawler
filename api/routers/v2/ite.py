from fastapi import APIRouter, Depends
from api.crawler.v2.department_common_crawler import *

router = APIRouter(
    prefix="/v2/ite",
    tags=["ite"],
    responses={404: {"description": "Not found"}},
)


@router.get("/notice/")
async def get_ite_notice(params: dict = Depends(ite_notice)):
    return params


@router.get("/article/")
async def get_ite_article(params: dict = Depends(department_common_article_parser)):
    return params
