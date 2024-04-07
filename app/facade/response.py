import json
from fastapi import status
from fastapi.responses import JSONResponse
from typing import Union


http_status_codes = {
    200: '成功！',
    204: '无数据！',
    400: '请求错误！',
    403: '无权限！',
    404: '未找到资源！',
}


class Response:
    @staticmethod
    def res_200(data: Union[list, dict, str] = None, code: int = 200, msg: str = None) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'code': code,
                'data': data,
                'msg': msg if msg is not None else (http_status_codes[code] if code in http_status_codes else "ok"),
            }
        )

    @staticmethod
    def res_400(data: Union[list, dict, str] = None, msg: str = 'error') -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'code': 400,
                'data': data,
                'msg': msg,
            }
        )
