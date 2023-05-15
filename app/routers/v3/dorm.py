from fastapi import APIRouter, Depends
from app.db.v3.dorm import *

router = APIRouter(
    prefix="/v3/dorm",
    tags=["dorm"],
    responses={404: {"description": "Not found"}},
)


@router.get("/notice/")
async def get_dorm_notice(params: dict = Depends(dorm_notice)):
    return params


@router.get("/free/")
async def get_dorm_free_board(params: dict = Depends(dorm_free_board)):
    return params


@router.get("/article/")
async def get_dorm_article(params: dict = Depends(get_article)):
    return params
