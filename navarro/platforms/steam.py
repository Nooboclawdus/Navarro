"""Steam username checker."""
from navarro.core.base import PlatformChecker
from navarro.core.enums import CheckResult
from .mixins import SingleURLMixin


class SteamChecker(SingleURLMixin, PlatformChecker):
    """Steam Community username checker."""
    
    platform_name = "Steam"
    platform_key = "steam"
    URL_PATTERN = "https://steamcommunity.com/id/{username}"
    
    def detect_found(self, response) -> bool:
        if response.status_code == 404:
            return False
        text = response.text
        if "The specified profile could not be found" in text:
            return False
        if 'class="profile_header_bg"' in text:
            return True
        return self._current_username.lower() in text.lower()
    
    def detect_not_found(self, response) -> bool:
        if response.status_code == 404:
            return True
        return "The specified profile could not be found" in response.text
    
    def check(self, username: str) -> CheckResult:
        self._current_username = username
        return super().check(username)
