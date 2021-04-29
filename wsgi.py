import os
from dotenv import load_dotenv

# 指定.env文件路径
# 使用python类来组织配置。包含敏感信息的配置会从环境变量获取，这些配置值存储在.env文件中。
# 当安装了python-dotenv并使用Flask内置的run命令启动程序时，.env文件的环境变量会被自动设置。
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
# 从当前目录的.env文件加载环境变量(如果存在该文件)
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from Xtime2 import create_app

app = create_app('development')
