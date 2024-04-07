import toml
import uvicorn
from fastapi import FastAPI
from app.facade import Loggers
from app.facade.database import config
from app.facade.config import initConfig
from app.facade.routes import add_routers
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.usetime import UseTimeMiddleware
from fastapi.exceptions import RequestValidationError
from tortoise.contrib.fastapi import register_tortoise
from app.facade.exception import validation_exception_handler


app = FastAPI(title="Aweb")

# 注册全局中间件
app.add_middleware(UseTimeMiddleware)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   expose_headers=["*"],
                   max_age=600,
                   )


# 参数异常处理
app.add_exception_handler(RequestValidationError,
                          validation_exception_handler)
# 配置路由
add_routers(app)


@app.on_event("startup")
async def startup_event():
    Loggers.init_config()
    register_tortoise(app=app, config=config)


if __name__ == "__main__":
    initConfig()
    config = toml.load('config/app.toml')
    port = config.get('app').get('port', 3030)
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
