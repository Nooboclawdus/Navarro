"""Chess.com username checker."""
from navarro.core.base import PlatformChecker
from navarro.core.enums import CheckResult
from .mixins import SingleURLMixin


class ChessDotComChecker(SingleURLMixin, PlatformChecker):
    """Chess.com username checker."""
    
    platform_name = "Chess.com"
    platform_key = "chessdotcom"
    URL_PATTERN = "https://www.chess.com/member/{username}"
    
    def detect_found(self, response) -> bool:
        if response.status_code != 200:
            return False
        text = response.text.lower()
        return self._current_username.lower() in text and "chess.com" in text
    
    def detect_not_found(self, response) -> bool:
        return response.status_code == 404
    
    def check(self, username: str) -> CheckResult:
        self._current_username = username
        return super().check(username)
