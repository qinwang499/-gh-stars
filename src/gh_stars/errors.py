"""项目自定义异常。

所有业务异常都继承 GhStarsError，方便统一捕获。
"""


class GhStarsError(Exception):
    """所有 gh-stars 异常的基类。"""
    pass


class UserNotFoundError(GhStarsError):
    """用户名不合法或不存在。"""
    pass


class RateLimitError(GhStarsError):
    """请求被 GitHub 限流。"""

    def __init__(self, retry_after: int = 60):
        super().__init__(f"请求太频繁，请 {retry_after} 秒后重试")
        self.retry_after = retry_after