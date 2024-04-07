import toml
import uvicorn
from fastapi import FastAPI
from app.facade.config import initConfig
from app.facade.routes import add_routers
from app.facade import Loggers
from app.facade.database import config
from tortoise.contrib.fastapi import register_tortoise
from fastapi.exceptions import RequestValidationError
from app.facade.exception import validation_exception_handler

app = FastAPI()

register_tortoise(app=app, config=config)

# 参数异常处理
app.add_exception_handler(RequestValidationError,
                          validation_exception_handler)

# 配置路由
add_routers(app)

if __name__ == "__main__":
    initConfig()
    Loggers.init_config()
    config = toml.load('config/app.toml')
    port = config.get('app').get('port', 3030)
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
