import toml
from app.model.base.config import ConfigModel
from app.model.base.user import UserModel
from app.facade.encry import handleAuth


db_config = toml.load("config/database.toml")
engine = db_config.get("engine", "sqlite")

config = {
    "connections": {
        "default": {
            "engine": f"tortoise.backends.{db_config.get('engine', 'sqlite')}",
            "credentials": {
                "host": db_config.get(engine).get("hostname", "127.0.0.1"),
                "port": db_config.get(engine).get("hostport", 3306),
                "user": db_config.get(engine).get("username", "root"),
                "database": db_config.get(engine).get("database"),
                "password": db_config.get(engine).get("password"),
                "charset": db_config.get(engine).get("charset", "utf8mb4"),
                "echo": True,
            },
        }
    },
    "apps": {
        "models": {
            "models": ["app.model.base.user", "app.model.base.config", "aerich.models"],
            "default_connection": "default",
        }
    },
    "use_tz": True,
    "timezone": "Asia/Shanghai",
}


class InsertUtil:

    @staticmethod
    async def init_data():
        await InsertUtil.insert_admin_user()

    @staticmethod
    async def insert_admin_user():
        count = await UserModel.filter(admin=True).count()
        if not count:
            password = handleAuth.get_password_hash("123456")
            await UserModel.create(
                account="admin", password=password, nickname="管理员", admin=True
            )
