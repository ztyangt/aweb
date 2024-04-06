from fastapi import status
from fastapi.responses import JSONResponse
from typing import Union


class Response:
    @staticmethod
    def res_200(data: Union[list, dict, str], msg: str = 'success') -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'code': 200,
                'data': data,
                'msg': msg,
            }
        )

    @staticmethod
    def res_400(data: Union[list, dict, str], msg: str = 'error') -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'code': 400,
                'data': data,
                'msg': msg,
            }
        )
