import toml


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

    "use_tz": True,
    "timezone": "Asia/Shanghai",
}
