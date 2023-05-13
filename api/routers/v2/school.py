from fastapi import APIRouter, Depends
from api.crawler.v2.school_crawler import *

router = APIRouter(
    prefix="/v2/school",
    tags=["school"],
    responses={404: {"description": "Not found"}},
)


@router.get("/notice/")
async def get_school_general_notice(params: dict = Depends(school_general_notice)):
    return params


@router.get("/scholar/")
async def get_school_scholar_notice(params: dict = Depends(school_scholar_notice)):
    return params


@router.get("/bachelor/")
async def get_school_bachelor_notice(params: dict = Depends(school_bachelor_notice)):
    return params


@router.get("/covid19/")
async def get_school_covid19_notice(params: dict = Depends(school_covid19_notice)):
    return params


@router.get("/article/")
async def get_school_article(params: dict = Depends(school_article_parser)):
    return params
