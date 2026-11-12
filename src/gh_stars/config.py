"""项目配置：常量与密钥读取。"""

import os

from dotenv import load_dotenv

load_dotenv()

GITHUB_API = "https://api.github.com"
TIMEOUT = 10
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
