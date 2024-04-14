from fastapi import APIRouter, Depends
from app.facade import RES
from app.model.base.user import User_Pydantic
from app.facade.encry import handleAuth, JwtUtil


comm = APIRouter()


@comm.post("/login", summary="用户登录")
async def login(ussername: str, password: str):
    user = await handleAuth.authenticate_user(ussername, password)
    if not user:
        return RES.res_200(code=401, msg='用户名或密码错误！')
    return RES.res_200({
        'token': JwtUtil.generate({"uid": user.id, "account": user.account}),
        'user': User_Pydantic.model_validate(user).model_dump(mode="json")
    }, msg=f'登录成功！')
