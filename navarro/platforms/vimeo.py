"""Vimeo username checker."""
from navarro.core.base import PlatformChecker
from navarro.core.enums import CheckResult
from .mixins import SingleURLMixin


class VimeoChecker(SingleURLMixin, PlatformChecker):
    """Vimeo username checker."""
    
    platform_name = "Vimeo"
    platform_key = "vimeo"
    URL_PATTERN = "https://vimeo.com/{username}"
    
    NOT_FOUND_MARKERS = [
        "Sorry, we couldn't find that page",
        "Page not found",
    ]
    
    def detect_found(self, response) -> bool:
        if response.status_code == 404:
            return False
        text = response.text
        if any(marker in text for marker in self.NOT_FOUND_MARKERS):
            return False
        return self._current_username.lower() in text.lower()
    
    def detect_not_found(self, response) -> bool:
        if response.status_code == 404:
            return True
        return any(marker in response.text for marker in self.NOT_FOUND_MARKERS)
    
    def check(self, username: str) -> CheckResult:
        self._current_username = username
        return super().check(username)
