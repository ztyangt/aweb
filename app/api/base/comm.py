from fastapi import APIRouter, Body
from app.facade import RES
from app.model.base.user import User_Pydantic
from app.facade.encry import handleAuth, JwtUtil


comm = APIRouter()


@comm.post("/login", summary="用户登录")
async def login(
    account: str = Body(description="账号"), password: str = Body(description="密码")
):
    user = await handleAuth.authenticate_user(account, password)
    if not user:
        return RES.res_200(code=401, msg="账号或密码错误！")
    admin = user.admin
    payload = (
        {"uid": user.id, "admin": admin, "account": user.account}
        if admin
        else {"uid": user.id, "account": user.account}
    )
    del user.admin
    return RES.res_200(
        {
            "token": JwtUtil.generate(payload),
            "user": User_Pydantic.model_validate(user).model_dump(mode="json"),
        },
        msg=f"登录成功！",
    )
