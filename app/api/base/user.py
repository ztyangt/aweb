import math
import time
from typing import List
from fastapi import APIRouter, Query, Depends, Body
from app.types.common.jwt import JwtData
from app.validator.base.user import UserVal, UserUpdateVal
from app.facade import RES
from app.model.base.user import UserModel, User_Pydantic
from app.facade.exception import handle_api_exceptions
from app.facade.encry import handleAuth, JwtUtil


user = APIRouter()


@user.get("/one", summary="获取指定")
@handle_api_exceptions
async def one(
    id: int = Query(description="数据id"),
    fields: List[str] = Query(None, description="查询字段"),
    onlyTrashed: bool = Query(
        default=None, description="仅查询回收站", example="false"
    ),
):

    fields = None if fields == [""] else fields
    where = {}

    if onlyTrashed:
        where["delete_time__isnull"] = False
    res = await UserModel.get_or_none(id=id, **where)
    if res is None:
        return RES.res_200(code=204, msg="无数据")
    return RES.res_200(
        User_Pydantic.model_validate(res).model_dump(mode="json", include=fields)
    )


@user.get("/all", summary="获取全部")
@handle_api_exceptions
async def all(
    page: int = Query(1, example=1, description="页码", gt=0),
    limit: int = Query(15, example=5, description="每页条数"),
    fields: List[str] = Query(default=None, description="查询字段"),
    order: str = Query(default=None, description="排序", example="id"),
    withTrashed: bool = Query(default=None, description="包含回收站", example="false"),
    onlyTrashed: bool = Query(
        default=None, description="仅查询回收站", example="false"
    ),
):
    fields = None if fields == [""] else fields
    order = "id" if not order else order

    where = {}
    if not withTrashed:
        where["delete_time__isnull"] = True

    if onlyTrashed:
        where["delete_time__isnull"] = False

    res = await User_Pydantic.from_queryset(
        UserModel.filter(**where)
        .order_by(order)
        .offset(limit * (page - 1))
        .limit(limit)
    )
    count = await UserModel.filter(**where).count()
    return (
        RES.res_200(
            {
                "total": count,
                "data": [item.model_dump(mode="json", include=fields) for item in res],
                "page": math.ceil(count / limit),
            }
        )
        if len(res)
        else RES.res_200(code=204, msg="无数据")
    )


@user.get("/count", summary="查询数量")
@handle_api_exceptions
async def count(
    withTrashed: bool = Query(default=None, description="包含回收站", example="false"),
):
    where = {}
    if not withTrashed:
        where["delete_time__isnull"] = True
    res = await UserModel.filter(**where).count()
    return RES.res_200(res, msg="查询成功！")


@user.get("/column", summary="查询列")
@handle_api_exceptions
async def column(
    fields: List[str] = Query(default=None, description="查询字段"),
    withTrashed: bool = Query(default=None, description="包含回收站", example="false"),
    onlyTrashed: bool = Query(
        default=None, description="仅查询回收站", example="false"
    ),
):

    where = {}
    if not withTrashed:
        where["delete_time__isnull"] = True

    if onlyTrashed:
        where["delete_time__isnull"] = False

    fields = None if fields == [""] else fields
    res = await User_Pydantic.from_queryset(UserModel.filter(**where))
    return (
        RES.res_200([item.model_dump(mode="json", include=fields) for item in res])
        if len(res)
        else RES.res_200(code=204, msg="无数据")
    )


@user.post("/save", summary="保存用户", dependencies=[Depends(JwtUtil.check_login)])
@handle_api_exceptions
async def save(data: UserUpdateVal):
    if data.id:
        return await update(data)
    else:
        del data.id
        return await create(data)


@user.post("/create", summary="创建用户", dependencies=[Depends(JwtUtil.check_admin)])
@handle_api_exceptions
async def create(data: UserVal):
    existing_account = await UserModel.exists(account=data.account)

    if existing_account:
        return RES.res_200(code=400, msg="账号已存在")
    existing_email = (
        None if data.email == None else await UserModel.exists(email=data.email)
    )
    if existing_email:
        return RES.res_200(code=400, msg="邮箱已存在")

    data.password = handleAuth.get_password_hash(data.password)

    res = await UserModel.create(**data.model_dump())
    return RES.res_200({"id": res.id}, 200, "创建成功")


@user.put("/update", summary="更新用户")
@handle_api_exceptions
async def update(data: UserUpdateVal, cur_user: JwtData = Depends(JwtUtil.check_login)):
    if not (cur_user["uid"] == data.id or cur_user.get("admin", False)):
        return RES.res_200(code=403, msg="无权限")
    print(cur_user)
    exist = await UserModel.exists(id=data.id)
    if not exist:
        return RES.res_200(code=400, msg="用户不存在")
    if data.password != None:
        data.password = handleAuth.get_password_hash(data.password)
    id = data.id
    del data.id
    await UserModel.filter(id=id).update(
        **data.model_dump(), update_time=int(time.time() * 1000)
    )
    return RES.res_200({"id": id}, code=200, msg="更新成功")


@user.put("/restore", summary="恢复数据", dependencies=[Depends(JwtUtil.check_admin)])
@handle_api_exceptions
async def restore(ids: List[int] = Body(description="主键列表")):
    records_to_restore = await UserModel.filter(
        id__in=ids, delete_time__not_isnull=True
    )

    if not records_to_restore:
        return RES.res_200(code=204, msg="无可操作数据")

    restore_ids = [record.id for record in records_to_restore]

    await UserModel.filter(id__in=restore_ids).update(delete_time=None)

    return RES.res_200({"ids": restore_ids}, code=200, msg="操作成功")


@user.delete("/remove", summary="软删除")
@handle_api_exceptions
async def remove(
    ids: List[int] = Body(description="主键列表"),
    cur_user: JwtData = Depends(JwtUtil.check_admin),
):
    if cur_user["uid"] in ids:
        return RES.res_200({"id": cur_user["uid"]}, code=400, msg="不能自己删除自己！")

    # 获取要更新的记录的完整列表（包括ID）
    records_to_update = await UserModel.filter(id__in=ids, delete_time__isnull=True)

    if not records_to_update:
        return RES.res_200(code=204, msg="无可操作数据")

    updated_ids = [record.id for record in records_to_update]

    await UserModel.filter(id__in=updated_ids).update(
        delete_time=int(time.time() * 1000)
    )
    return RES.res_200({"ids": updated_ids}, code=200, msg="操作成功")


@user.delete("/delete", summary="彻底删除")
@handle_api_exceptions
async def delete(
    ids: List[int] = Body(description="主键列表"),
    cur_user: JwtData = Depends(JwtUtil.check_admin),
):
    if cur_user["uid"] in ids:
        return RES.res_200({"id": cur_user["uid"]}, code=400, msg="不能自己删除自己！")

    records_to_delete = await UserModel.filter(id__in=ids, delete_time__not_isnull=True)

    if not records_to_delete:
        return RES.res_200(code=204, msg="无可操作数据")

    delete_ids = [record.id for record in records_to_delete]
    await UserModel.filter(id__in=delete_ids).delete()
    return RES.res_200({"ids": delete_ids}, code=200, msg="操作成功")


@user.delete(
    "/clear", summary="清空回收站", dependencies=[Depends(JwtUtil.check_login)]
)
@handle_api_exceptions
async def clear():
    await UserModel.filter(delete_time__not_isnull=True).delete()
    return RES.res_200(code=200, msg="操作成功")
