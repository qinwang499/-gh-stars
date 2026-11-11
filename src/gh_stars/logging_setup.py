"""日志配置：控制台 + 文件双输出。"""

import logging


def setup_logging(level: int = logging.INFO) -> None:
    """初始化日志：控制台显示 INFO 以上，文件记录 DEBUG 以上。"""

    logger = logging.getLogger("gh_stars")

    # 防止重复添加 handler（多次调用会产生重复日志）
    if logger.handlers:
        return

    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ① 控制台：只显示 level 及以上
    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(fmt)
    logger.addHandler(console)

    # ② 文件：记录所有 DEBUG 及以上
    file_handler = logging.FileHandler("gh-stars.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)