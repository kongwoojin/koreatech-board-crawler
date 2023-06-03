from fastapi import APIRouter, Depends
from crawler.v2.department_common_crawler import *

router = APIRouter(
    prefix="/v2/mechatronics",
    tags=["mechatronics"],
    responses={404: {"description": "Not found"}},
)


@router.get("/notice/")
async def get_mechanical_notice(params: dict = Depends(mechatronics_notice)):
    return params


@router.get("/lecture/")
async def get_mechanical_lecture_notice(params: dict = Depends(mechatronics_lecture_notice)):
    return params


@router.get("/bachelor/")
async def get_mechanical_bachelor_notice(params: dict = Depends(mechatronics_bachelor_notice)):
    return params


@router.get("/job/")
async def get_mechanical_job_notice(params: dict = Depends(mechatronics_job_notice)):
    return params


@router.get("/free/")
async def get_mechanical_free_board(params: dict = Depends(mechatronics_free_board)):
    return params


@router.get("/article/")
async def get_mechanical_article(params: dict = Depends(department_common_article_parser)):
    return params
