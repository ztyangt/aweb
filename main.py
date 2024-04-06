import toml
import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from app.facade.config import initConfig
from app.facade.exception import validation_exception_handler
from app.facade.routes import add_routers
from app.facade import Loggers


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.facade.database import init_tortoise_orm, autoMigrate
    # 初始化Tortoise ORM
    init_tortoise_orm(app)
    # 接管默认日志
    Loggers.init_config()
    # 自动迁移
    autoMigrate()
    yield


app = FastAPI(lifespan=lifespan)


# 参数异常处理
app.add_exception_handler(RequestValidationError,
                          validation_exception_handler)

# 配置路由
add_routers(app)

if __name__ == "__main__":
    initConfig()
    config = toml.load('config/app.toml')
    port = config.get('app').get('port', 3030)
    uvicorn.run("main:app", host="0.0.0.0", port=port,
                reload=True)
