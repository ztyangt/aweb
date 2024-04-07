from fastapi import FastAPI
from .response import Response as RES
from .logger import Loggers
from .logger import log
from .exception import validation_exception_handler, http_exception_handler, app_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


def registerCustomErrorHandle(server: FastAPI):
    """ 统一注册自定义错误处理器 """
    server.add_exception_handler(
        RequestValidationError, validation_exception_handler)
    # 错误处理StarletteHTTPException
    server.add_exception_handler(
        StarletteHTTPException, http_exception_handler)
    # 自定义全局系统错误
    server.add_exception_handler(Exception, app_exception_handler)
