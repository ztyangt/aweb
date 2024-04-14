import toml
import uvicorn
from fastapi import FastAPI
from app.facade import Loggers, registerCustomErrorHandle
from app.facade.database import config, InsertUtil
from app.facade.config import initConfig
from app.facade.routes import add_routers
from tortoise.contrib.fastapi import register_tortoise
from app.middleware import registerMiddlewareHandle


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     Loggers.init_config()
#     await InsertUtil.init_data()
#     yield
#     print("关闭应用")

app = FastAPI(title="Poetry-API", version="0.1")

# 初始化配置
initConfig()

# 注册全局中间件
registerMiddlewareHandle(app)

# 注册全局异常处理
registerCustomErrorHandle(app)

# 注册路由
add_routers(app)

# 注册tortoise-orm
register_tortoise(app=app, config=config)


@app.on_event("startup")
async def startup_event():
    Loggers.init_config()
    await InsertUtil.init_data()


if __name__ == "__main__":
    config = toml.load('config/app.toml')
    port = config.get('app').get('port', 3030)
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
