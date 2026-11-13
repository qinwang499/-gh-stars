"""核心逻辑：校验输入、执行查询。"""

import logging
import sys

from gh_stars.cli import parse_args
from gh_stars.config import GITHUB_API, TIMEOUT
from gh_stars.errors import GhStarsError, UserNotFoundError

logger = logging.getLogger("gh_stars.core")


def hello(name: str = "git") -> str:
    """第一版 hello 脚本，改造成函数。"""
    return f"hello, {name}"


def validate_username(name: str) -> str:
    """校验用户名，不合法就抛 UserNotFoundError。"""
    name = name.strip()

    if not name:
        logger.warning("用户名为空")
        raise UserNotFoundError("用户名不能为空")

    if len(name) > 39:
        logger.warning("用户名过长：%s", name)
        raise UserNotFoundError(f"用户名长度不合法：{name}")

    for ch in name:
        if not (ch.isalnum() or ch == "-"):
            logger.warning("用户名含非法字符：%r", ch)
            raise UserNotFoundError(f"用户名含非法字符：{ch}")

    logger.debug("用户名校验通过：%s", name)
    return name


def run(user: str) -> None:
    """真正干活的函数，出错就往上抛。"""
    logger.info("开始处理用户：%s", user)
    user = validate_username(user)
    print(f"查询用户：{user}")
    print(f"API 地址：{GITHUB_API}")
    print(f"超时时间：{TIMEOUT} 秒")
    logger.info("处理完成：%s", user)


def main() -> None:
    """入口：解析参数，接住异常，给出人话。"""
    args = parse_args()
    logger.debug("收到参数：%r", args)

    try:
        run(args.user)
    except GhStarsError as e:
        logger.error("业务异常：%s", e)
        print(f"错误：{e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("用户取消")
        print("\n已取消")
        sys.exit(130)
    finally:
        logger.info("程序结束")
        print("程序结束")
