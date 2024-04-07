from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .usetime import UseTimeMiddleware
from .jwt import JwtMiddleware


def registerMiddlewareHandle(server: FastAPI):
    """ 注册中间件 """
    server.add_middleware(UseTimeMiddleware)
    server.add_middleware(JwtMiddleware)
    server.add_middleware(CORSMiddleware,
                          allow_origins=["*"],
                          allow_credentials=True,
                          allow_methods=["*"],
                          allow_headers=["*"],
                          expose_headers=["*"],
                          max_age=600,
                          )
