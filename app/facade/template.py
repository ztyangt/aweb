
TempApp = """# 应用配置
[app]
# 项目运行端口
port = 3030
"""


TempDatabase = """# 数据库引擎
engine = "mysql"

# Mysql配置
[mysql]
hostname = \"localhost\"
# 数据库端口
hostport = 3306
# 数据库用户
username = \"\"
# 数据库名称
database = \"\"
# 数据库密码
password = \"\"
# 数据库编码
charset = \"utf8mb4\""""


TempJwt = """# JWT配置
[jwt]
# 密钥
key      = \"Aweb-7dfa9589ccf3b93336fd22af3c77061e\"
# 过期时间(秒)
expire   = \"7 * 24 * 60 * 60\"
# 签发者
issuer   = \"ztyang\"
# 主题
subject  = \"Aweb\""""
