from typing import Any, Optional


class KnownError(Exception):
    def __init__(self, message: str, inner: Optional[Any] = None):
        super().__init__(message)
        self.inner = inner

    def get_pretty(self) -> str:
        if self.inner:
            return f"""{self}
... {self.inner}
"""
        return str(self)


class BadConfigurationError(KnownError):
    def __init__(self, message: str):
        super().__init__(f"bad configuration: {message}")


class UsageError(KnownError):
    def __init__(self, message: str):
        super().__init__(f"bad usage: {message}")


class TransientError(KnownError):
    def __init__(self, message: str, inner: Optional[Any] = None):
        super().__init__(f"transient error: {message}", inner)
