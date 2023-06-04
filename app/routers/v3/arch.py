from fastapi import APIRouter, Depends
from app.db.v3.arch import *

router = APIRouter(
    prefix="/v3/arch",
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
async def get_arch_article(params: dict = Depends(get_article)):
    return params
