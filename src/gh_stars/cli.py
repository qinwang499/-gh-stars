"""命令行参数解析。"""

import argparse


def build_parser() -> argparse.ArgumentParser:
    """构建参数解析器。"""
    parser = argparse.ArgumentParser(
        prog="gh-stars",
        description="查询 GitHub 用户的仓库 star 排行榜",
    )

    parser.add_argument(
        "--user",
        "-u",
        required=True,
        help="GitHub 用户名",
    )
    parser.add_argument(
        "--top",
        "-t",
        type=int,
        default=10,
        help="只显示前 N 个仓库（默认 10）",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="stars.csv",
        help="CSV 输出路径（默认 stars.csv）",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="显示调试日志",
    )

    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """解析命令行参数。"""
    parser = build_parser()
    return parser.parse_args(argv)
