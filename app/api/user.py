from fastapi import APIRouter, Query
from app.validator.user import UserVal
from app.facade import RES
from app.model.user import UserModel, User_Pydantic
from app.facade.exception import handle_api_exceptions
from tortoise.contrib.pydantic import pydantic_queryset_creator


user = APIRouter()


@user.get("/one", summary="获取指定")
@handle_api_exceptions
async def one(id: int = Query(description="数据id")):
    res = await UserModel.get_or_none(id=id)
    return RES.res_200(User_Pydantic.model_validate(res).model_dump(mode='json')) if res else RES.res_200(code=204, msg='无数据')


@user.post("/create", summary="创建用户")
@handle_api_exceptions
async def create(data: UserVal):
    existing_account = await UserModel.get_or_none(account=data.account)
    if existing_account:
        return RES.res_200(code=400, msg='账号已存在')
    res = await UserModel.create(**data.model_dump())
    return RES.res_200({"id": res.id}, 200, '创建成功')
