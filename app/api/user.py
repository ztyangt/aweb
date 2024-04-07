import utils
import math
from typing import List
from fastapi import APIRouter, Query
from app.validator.user import UserVal
from app.facade import RES
from app.model.user import UserModel, User_Pydantic
from app.facade.exception import handle_api_exceptions


user = APIRouter()


@user.get("/one", summary="获取指定")
@handle_api_exceptions
async def one(
    id: int = Query(description="数据id"),
    fields: List[str] = Query(default=None, description="查询字段"),
):
    res = await UserModel.get_or_none(id=id)
    if res is None:
        return RES.res_200(code=204, msg='无数据')
    return RES.res_200(User_Pydantic.model_validate(res).model_dump(mode="json", include=fields))


@user.get("/all", summary="获取全部")
@handle_api_exceptions
async def one(
    page: int = Query(example=1, description="页码", gt=0),
    limit: int = Query(example=5, description="每页条数"),
    fields: List[str] = Query(default=None, description="查询字段"),
):
    res = await User_Pydantic.from_queryset(UserModel.all().offset(limit * (page - 1)).limit(limit))
    count = await UserModel.all().count()
    return RES.res_200({
        "total": count,
        "data": [item.model_dump(mode="json", include=fields) for item in res],
        "page": math.ceil(count / limit),
    }) if len(res) else RES.res_200(code=204, msg='无数据')


@user.get("/count", summary="查询数量")
@handle_api_exceptions
async def count():
    res = await UserModel.all().count()
    return RES.res_200(res, msg="查询成功！")


@user.get("/column", summary="查询列")
@handle_api_exceptions
async def column(
    fields: List[str] = Query(default=None, description="查询字段"),
):
    res = await User_Pydantic.from_queryset(UserModel.all())
    return RES.res_200([item.model_dump(mode="json", include=fields) for item in res]) if len(res) else RES.res_200(code=204, msg='无数据')


@user.post("/create", summary="创建用户")
@handle_api_exceptions
async def create(data: UserVal):
    existing_account = await UserModel.get_or_none(account=data.account)

    if existing_account:
        return RES.res_200(code=400, msg='账号已存在')
    existing_email = await UserModel.get_or_none(email=data.email)

    if existing_email:
        return RES.res_200(code=400, msg='邮箱已存在')

    data.password = utils.password.create(data.password)

    res = await UserModel.create(**data.model_dump())
    return RES.res_200({"id": res.id}, 200, '创建成功')
