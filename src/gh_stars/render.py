"""终端表格输出与 CSV 导出。"""

import csv
import unicodedata

from gh_stars.errors import GhStarsError


def _width(text: str) -> int:
    """计算显示宽度：中文占 2 列，英文占 1 列。"""
    total = 0
    for ch in text:
        total += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
    return total


def _pad(text: str, width: int, align: str = "left") -> str:
    """按显示宽度补齐空格。"""
    space = " " * max(0, width - _width(text))
    return text + space if align == "left" else space + text


def sort_by_stars(repos: list[dict], top: int) -> list[dict]:
    """按 star 降序，取前 top 个。"""
    return sorted(repos, key=lambda r: r["stars"], reverse=True)[:top]


def print_table(repos: list[dict]) -> None:
    """打印对齐表格。"""
    if not repos:
        print("（没有仓库）")
        return

    widths = (5, 26, 8, 12, 12)
    titles = ("排名", "仓库名", "STARS", "语言", "更新")

    def line(cells: tuple[str, ...]) -> str:
        parts = [
            _pad(c, w, "right" if i == 2 else "left")
            for i, (c, w) in enumerate(zip(cells, widths))
        ]
        return "  ".join(parts).rstrip()

    header = line(titles)
    print(header)
    print("-" * _width(header))

    for i, r in enumerate(repos, 1):
        print(
            line(
                (
                    str(i),
                    r["name"][:24],
                    str(r["stars"]),
                    r["language"][:13],
                    r["updated"],
                )
            )
        )


def save_csv(repos: list[dict], path: str) -> None:
    """保存为 CSV（utf-8-sig 让 Excel 正常显示中文）。"""
    try:
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["name", "stars", "language", "updated"],
            )
            writer.writeheader()
            writer.writerows(repos)
    except OSError as e:
        raise GhStarsError(f"无法写入文件 {path}：{e}")
