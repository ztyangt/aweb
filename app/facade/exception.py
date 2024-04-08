import traceback
from app.facade import log
from app.facade import RES
from functools import wraps
from fastapi import status
from fastapi.requests import Request
from starlette.exceptions import HTTPException


async def validation_exception_handler(request, exc):
    errors = []
    for error in exc.errors():
        errors.append({
            'loc': error.get('loc'),
            'msg': error.get('msg'),
            'type': error.get('type')
        })
        log.error(f"参数错误: {str(errors)}")
    return RES.res_400(errors, "参数错误")


def handle_api_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            log.error(f"接口异常: {e}")
            return RES.res_400(str(e))
    return wrapper


async def http_exception_handler(request, exc: HTTPException):
    """自定义处理HTTPException"""

    log.error(exc.detail)
    return RES.res_200(code=exc.status_code, msg=exc.detail)


async def app_exception_handler(request: Request, exc: Exception):
    """自定义全局系统错误"""
    log.error(f"系统异常: {traceback.format_exc()}")
    return RES.res_200(code=500, msg="系统异常,请稍后重试~")
