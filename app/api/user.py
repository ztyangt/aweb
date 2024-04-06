from fastapi import APIRouter
from app.validator.user import UserVal
from app.facade import RES


user = APIRouter()


@user.post("/create", summary="创建用户")
async def create(data: UserVal):
    return RES.res_200(data.model_dump())
