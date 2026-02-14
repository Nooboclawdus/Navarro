"""DeviantArt username checker."""
from navarro.core.base import PlatformChecker
from navarro.core.enums import CheckResult
from .mixins import SingleURLMixin


class DeviantArtChecker(SingleURLMixin, PlatformChecker):
    """DeviantArt username checker."""
    
    platform_name = "DeviantArt"
    platform_key = "deviantart"
    URL_PATTERN = "https://www.deviantart.com/{username}"
    
    NOT_FOUND_MARKERS = [
        "doesn't exist",
        "The page you're looking for",
    ]
    
    def detect_found(self, response) -> bool:
        if response.status_code == 404:
            return False
        text = response.text
        if any(marker in text for marker in self.NOT_FOUND_MARKERS):
            return False
        return self._current_username.lower() in text.lower() or 'deviantart.com' in text
    
    def detect_not_found(self, response) -> bool:
        if response.status_code == 404:
            return True
        return any(marker in response.text for marker in self.NOT_FOUND_MARKERS)
    
    def check(self, username: str) -> CheckResult:
        self._current_username = username
        return super().check(username)
