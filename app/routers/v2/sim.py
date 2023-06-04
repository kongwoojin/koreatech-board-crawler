from fastapi import APIRouter, Depends
from app.crawler.v2.department_common_crawler import *

router = APIRouter(
    prefix="/v2/sim",
    tags=["sim"],
    responses={404: {"description": "Not found"}},
)


@router.get("/notice/")
async def get_sim_notice(params: dict = Depends(sim_notice)):
    return params


@router.get("/article/")
async def get_sim_article(params: dict = Depends(department_common_article_parser)):
    return params
