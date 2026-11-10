"""核心逻辑：校验输入、执行查询。"""

import sys

from gh_stars.config import GITHUB_API, TIMEOUT
from gh_stars.errors import GhStarsError, UserNotFoundError


def hello(name: str = "git") -> str:
    """第一版 hello 脚本，改造成函数。"""
    return f"hello, {name}"


def validate_username(name: str) -> str:
    """校验用户名，不合法就抛 UserNotFoundError。"""
    name = name.strip()

    if not name:
        raise UserNotFoundError("用户名不能为空")

    if len(name) < 1 or len(name) > 39:
        raise UserNotFoundError(f"用户名长度不合法：{name}")

    for ch in name:
        if not (ch.isalnum() or ch == "-"):
            raise UserNotFoundError(f"用户名含非法字符：{ch}")

    return name


def run(user: str) -> None:
    """真正干活的函数，出错就往上抛。"""
    user = validate_username(user)
    print(f"查询用户：{user}")
    print(f"API 地址：{GITHUB_API}")
    print(f"超时时间：{TIMEOUT} 秒")


def main() -> None:
    """入口：负责接住所有业务异常，给出人话。"""
    try:
        if len(sys.argv) > 1:
            user = sys.argv[1]
        else:
            user = input("请输入 GitHub 用户名：")
        run(user)
    except GhStarsError as e:
        print(f"错误：{e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n已取消")
        sys.exit(130)
    except EOFError:
        print("错误：没有读到输入，已退出")
        sys.exit(1)
    finally:
        print("程序结束")