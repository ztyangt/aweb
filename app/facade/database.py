import toml
import os
import shutil
import subprocess
from tortoise.contrib.fastapi import register_tortoise


db_config = toml.load('config/database.toml')
engine = db_config.get('engine', 'sqlite')

config = {
    "connections": {
        "default": {
            "engine": f"tortoise.backends.{db_config.get('engine', 'sqlite')}",
            "credentials": {
                "host": db_config.get(engine).get('hostname', '127.0.0.1'),
                "port": db_config.get(engine).get('hostport', 3306),
                "user": db_config.get(engine).get('username', 'root'),
                "database": db_config.get(engine).get('database'),
                "password": db_config.get(engine).get('password'),
                "charset": db_config.get(engine).get('charset', 'utf8mb4'),
                "echo": True
            },
        }
    },

    "apps": {
        "models": {
            "models": ["app.model.user", "aerich.models"],
            "default_connection": "default",
        }
    },

    "use_tz": False,
    "timezone": "Asia/Shanghai",
}


def init_tortoise_orm(app):

    # 注册Tortoise ORM到FastAPI应用
    register_tortoise(
        app=app,
        config=config,
        # generate_schemas=False,  # 自动生成数据库表结构
        # add_exception_handlers=True,  # 添加异常处理,生产环境建议关闭，会泄露调试信息
    )


def autoMigrate():
    runtime_path = 'runtime/migrations'
    if os.path.exists(runtime_path):
        shutil.rmtree(runtime_path)
    subprocess.run(['aerich', 'init', '-t',
                   'app.facade.database.config', '--location', f'{runtime_path}'])

    subprocess.run(['aerich', 'init-db'])
    subprocess.run(['aerich', 'migrate'])
    subprocess.run(['aerich', 'upgrade'])
