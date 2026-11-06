from gh_stars.config import GITHUB_API, TIMEOUT


def hello(name: str = "git") -> str:
    """第一版 hello 脚本，改造成函数。"""
    return f"hello, {name}"


def main() -> None:
    print(hello())
    print(f"API 地址：{GITHUB_API}")
    print(f"超时时间：{TIMEOUT} 秒")