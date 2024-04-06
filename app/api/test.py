from fastapi import APIRouter, Query
from typing import Optional
from app.validator.test import TestVal

test = APIRouter()


@test.get("/get", summary="测试GET请求")
async def get(
    a: str = Query(example=20, description="参数描述"),
    b: int = Query(example=20, description="参数描述"),
    c: Optional[int] = Query(None, example=99, description="参数描述")
):
    return {"code": 200, "msg": "success", "data": {"name": "test", "a": a, "b": b}}


@test.post("/post", summary="测试POST请求")
async def post(data: TestVal):
    return {"code": 200, "msg": "success", "data": data}
