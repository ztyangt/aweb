from fastapi import APIRouter
from app.api import TestApi, FileApi, UserApi, CommApi


def add_routers(app: APIRouter):
    app.include_router(TestApi, prefix="/api/test", tags=["测试接口"])
    app.include_router(CommApi, prefix="/api/comm", tags=["公共接口"])
    app.include_router(UserApi, prefix="/api/user", tags=["用户接口"])
    app.include_router(FileApi, prefix="/api/file", tags=["文件接口"])
