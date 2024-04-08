from fastapi import APIRouter, Depends
from app.facade import RES
from fastapi.security import OAuth2PasswordRequestForm
from app.model.user import User_Pydantic
from app.facade.encry import handleAuth, JwtUtil


comm = APIRouter()


@comm.post("/login", summary="用户登录")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await handleAuth.authenticate_user(form_data.username, form_data.password)
    if not user:
        return RES.res_200(code=401, msg='用户名或密码错误！')
    return RES.res_200({
        'token': JwtUtil.generate({"uid": user.id, "username": user.username}),
        'user': User_Pydantic.model_validate(user).model_dump(mode="json")
    }, msg=f'登录成功！')
