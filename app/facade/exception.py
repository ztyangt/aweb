from app.facade import RES
from functools import wraps
from app.facade import log


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
