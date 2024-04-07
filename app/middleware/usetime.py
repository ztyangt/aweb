import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class UseTimeMiddleware(BaseHTTPMiddleware):
    """ 计算耗时中间件"""

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        """ 请求耗时 """
        start_time = time.time()
        # 调用下一个中间件或路由处理函数
        result = await call_next(request)
        process_time = time.time() - start_time
        process_time_ms = round(process_time * 1000, 2)
        # 将处理时间添加到响应头中
        result.headers["X-Process-Time"] = f"{process_time_ms}ms"
        return result
