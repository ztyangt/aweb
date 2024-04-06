import os
from app.facade.template import *


class initConfig:

    def __init__(self):
        if not os.path.exists('config'):
            os.mkdir('config')
        self.initAppConfig()
        self.initDbConfig()

    def initAppConfig(self):
        # 初始化配置文件，如果存在则跳过
        config_file = 'config/app.toml'
        if not os.path.exists(config_file):
            with open(config_file, 'w') as f:
                f.write(TempApp)

    def initDbConfig(self):
        # 初始化配置文件，如果存在则跳过
        config_file = 'config/database.toml'

        if not os.path.exists(config_file):
            with open(config_file, 'w') as f:
                f.write(TempDatabase)
