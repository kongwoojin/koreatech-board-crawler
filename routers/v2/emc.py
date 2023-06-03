from fastapi import APIRouter, Depends
from crawler.v2.department_common_crawler import *

router = APIRouter(
    prefix="/v2/emc",
    tags=["emc"],
    responses={404: {"description": "Not found"}},
)


@router.get("/notice/")
async def get_emc_notice(params: dict = Depends(emc_notice)):
    return params


@router.get("/article/")
async def get_emc_article(params: dict = Depends(department_common_article_parser)):
    return params
