from fastapi import APIRouter, Depends
from app.db.v3.emc import *

router = APIRouter(
    prefix="/v3/emc",
    tags=["emc"],
    responses={404: {"description": "Not found"}},
)


@router.get("/notice/")
async def get_emc_notice(params: dict = Depends(emc_notice)):
    return params


@router.get("/article/")
async def get_emc_article(params: dict = Depends(get_article)):
    return params
