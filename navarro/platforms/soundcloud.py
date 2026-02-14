"""SoundCloud username checker."""
from navarro.core.base import PlatformChecker
from navarro.core.enums import CheckResult
from .mixins import SingleURLMixin


class SoundCloudChecker(SingleURLMixin, PlatformChecker):
    """SoundCloud username checker."""
    
    platform_name = "SoundCloud"
    platform_key = "soundcloud"
    URL_PATTERN = "https://soundcloud.com/{username}"
    
    def detect_found(self, response) -> bool:
        if response.status_code != 200:
            return False
        text = response.text.lower()
        return 'soundcloud' in text or self._current_username.lower() in text
    
    def detect_not_found(self, response) -> bool:
        return response.status_code == 404
    
    def check(self, username: str) -> CheckResult:
        self._current_username = username
        return super().check(username)
