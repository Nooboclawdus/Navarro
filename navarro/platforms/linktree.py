"""Linktree username checker."""
from navarro.core.base import PlatformChecker
from navarro.core.enums import CheckResult
from .mixins import SingleURLMixin


class LinktreeChecker(SingleURLMixin, PlatformChecker):
    """Linktree username checker."""
    
    platform_name = "Linktree"
    platform_key = "linktree"
    URL_PATTERN = "https://linktr.ee/{username}"
    
    NOT_FOUND_MARKERS = [
        "Sorry, this page isn't available",
        "404",
    ]
    
    def detect_found(self, response) -> bool:
        if response.status_code != 200:
            return False
        text = response.text
        if any(marker in text for marker in self.NOT_FOUND_MARKERS):
            return False
        return self._current_username.lower() in text.lower() or "linktr.ee" in text.lower()
    
    def detect_not_found(self, response) -> bool:
        if response.status_code != 200:
            return True
        return any(marker in response.text for marker in self.NOT_FOUND_MARKERS)
    
    def check(self, username: str) -> CheckResult:
        self._current_username = username
        return super().check(username)
