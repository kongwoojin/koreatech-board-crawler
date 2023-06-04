from fastapi import APIRouter, Depends
from app.db.v3.ite import *

router = APIRouter(
    prefix="/v3/ite",
    tags=["ite"],
    responses={404: {"description": "Not found"}},
)


@router.get("/notice/")
async def get_ite_notice(params: dict = Depends(ite_notice)):
    return params


@router.get("/article/")
async def get_ite_article(params: dict = Depends(get_article)):
    return params
