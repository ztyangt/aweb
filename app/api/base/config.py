import math
from typing import List, Optional
from fastapi import APIRouter, Query, Depends, Body, Header
from app.validator.base.config import ConfigVal
from app.facade import RES
from app.model.base.config import ConfigModel, Config_Pydantic
from app.facade.exception import handle_api_exceptions
from app.facade.encry import JwtUtil
from tortoise import timezone


config = APIRouter()


@config.get("/one", summary="获取指定配置", dependencies=[Depends(JwtUtil.check_token)])
@handle_api_exceptions
async def one(
    name: str = Query(description="配置名"),
    fields: Optional[List[str]] = Query(default=None, description="查询字段"),
):
    res = await ConfigModel.get_or_none(name=name)
    if res is None:
        return RES.res_200(code=204, msg='无数据')
    return RES.res_200(Config_Pydantic.model_validate(res).model_dump(mode="json", include=fields))


@config.get("/all", summary="获取全部配置", dependencies=[Depends(JwtUtil.check_token)])
@handle_api_exceptions
async def one(
    page: int = Query(example=1, description="页码", gt=0),
    limit: int = Query(example=5, description="每页条数"),
    fields: Optional[List[str]] = Query(default=None, description="查询字段"),
):
    res = await Config_Pydantic.from_queryset(ConfigModel.all().offset(limit * (page - 1)).limit(limit))
    count = await ConfigModel.all().count()
    return RES.res_200({
        "total": count,
        "data": [item.model_dump(mode="json", include=fields) for item in res],
        "page": math.ceil(count / limit),
    }) if len(res) else RES.res_200(code=204, msg='无数据')


@config.get("/count", summary="查询数量")
@handle_api_exceptions
async def count():
    res = await ConfigModel.all().count()
    return RES.res_200(res, msg="查询成功！")


@config.get("/column", summary="查询列", dependencies=[Depends(JwtUtil.check_token)])
@handle_api_exceptions
async def column(fields: Optional[List[str]] = Query(default=None, description="查询字段")):
    res = await Config_Pydantic.from_queryset(ConfigModel.all())
    return RES.res_200([item.model_dump(mode="json", include=fields) for item in res]) if len(res) else RES.res_200(code=204, msg='无数据')


@config.put("/update", summary="更新配置", dependencies=[Depends(JwtUtil.check_token)])
@handle_api_exceptions
async def update(data: ConfigVal):
    res = await ConfigModel.filter(name=data.name).update(value=data.value, update_time=int(timezone.now().timestamp() * 1000))
    return RES.res_200(res, code=200, msg='更新成功')
