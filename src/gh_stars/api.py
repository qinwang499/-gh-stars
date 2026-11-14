"""GitHub API 封装。"""

import logging

import requests

from gh_stars.config import GITHUB_API, GITHUB_TOKEN, TIMEOUT
from gh_stars.errors import GhStarsError, RateLimitError, UserNotFoundError

logger = logging.getLogger("gh_stars.api")


def _headers() -> dict:
    """构造请求头，有 token 就带上。"""
    if GITHUB_TOKEN:
        return {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    return {}


def fetch_repos(user: str, per_page: int = 100) -> list[dict]:
    """拉取用户的全部公开仓库（处理分页）。"""
    url = f"{GITHUB_API}/users/{user}/repos"
    repos: list[dict] = []
    page = 1

    while True:
        logger.debug("请求第 %d 页：%s", page, url)
        try:
            resp = requests.get(
                url,
                headers=_headers(),
                params={"per_page": per_page, "page": page, "sort": "updated"},
                timeout=TIMEOUT,
            )
        except requests.Timeout:
            logger.error("请求超时：%s", url)
            raise GhStarsError("网络超时，请稍后重试")
        except requests.RequestException as e:
            logger.error("请求失败：%s", e)
            raise GhStarsError(f"网络错误：{e}")

        if resp.status_code == 404:
            logger.warning("用户不存在：%s", user)
            raise UserNotFoundError(f"找不到用户 {user}")

        if resp.status_code == 403:
            retry = resp.headers.get("Retry-After", "60")
            logger.warning("被限流，retry-after=%s", retry)
            raise RateLimitError(int(retry) if retry.isdigit() else 60)

        if resp.status_code != 200:
            logger.error("意外的状态码 %s", resp.status_code)
            raise GhStarsError(f"GitHub 返回异常状态码：{resp.status_code}")

        batch = resp.json()
        if not batch:
            break

        repos.extend(batch)
        logger.info("已拉取 %d 个仓库（第 %d 页）", len(repos), page)

        if len(batch) < per_page:
            break

        page += 1

    logger.info("共拉取 %d 个仓库", len(repos))
    return repos
def parse_repos(repos: list[dict]) -> list[dict]:
    """只保留需要的四个字段。"""
    result = []
    for r in repos:
        result.append({
            "name": r.get("name", ""),
            "stars": r.get("stargazers_count", 0),
            "language": r.get("language") or "-",
            "updated": (r.get("updated_at") or "")[:10],
        })
    return result