from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.facade import RES
from app.types.common.jwt import JwtData
from utils import JWTUtil


noCheckTokenPathList = []


class JwtMiddleware(BaseHTTPMiddleware):
    """ jwt验证中间件 """

    def __init__(self, app):
        super().__init__(app)
        self.jwtUtil = JWTUtil()

    async def dispatch(self, request: Request, call_next):
        # 判断路由是否需要验证
        path = request.url.path
        if path in noCheckTokenPathList:
            return await call_next(request)
        # 获取token
        token = request.headers.get('Authorization', '')
        if token == "":
            return RES.res_200(code=401, msg="无权限")

        # 验证token
        tokenInfo = self.jwtUtil.decode(token, JwtData)
        if not isinstance(tokenInfo, JwtData):
            return RES.res_200(code=401, msg="登录已过期，请重新登录！")

        result = await call_next(request)
        print("token解析成功", tokenInfo)
        return result
