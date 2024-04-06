# error_handlers.py
from app.facade import RES


async def validation_exception_handler(request, exc):
    errors = []
    for error in exc.errors():
        errors.append({
            'loc': error.get('loc'),
            'msg': error.get('msg'),
            'type': error.get('type')
        })
    return RES.res_400(errors, "请求参数错误")
