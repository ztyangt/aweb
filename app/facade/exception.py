from app.facade import RES
from functools import wraps


async def validation_exception_handler(request, exc):
    errors = []
    for error in exc.errors():
        errors.append({
            'loc': error.get('loc'),
            'msg': error.get('msg'),
            'type': error.get('type')
        })
    return RES.res_400(errors, "参数错误")


def handle_api_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            return RES.res_400(str(e))

    return wrapper
