from fastapi import APIRouter, Depends
from app.db.v3.sim import *

router = APIRouter(
    prefix="/v3/sim",
    tags=["sim"],
    responses={404: {"description": "Not found"}},
)


@router.get("/notice/")
async def get_sim_notice(params: dict = Depends(sim_notice)):
    return params


@router.get("/article/")
async def get_sim_article(params: dict = Depends(get_article)):
    return params
