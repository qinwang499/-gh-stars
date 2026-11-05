from gh_stars.config import GITHUB_API, TIMEOUT


def main() -> None:
    print(f"API 地址：{GITHUB_API}")
    print(f"超时时间：{TIMEOUT} 秒")