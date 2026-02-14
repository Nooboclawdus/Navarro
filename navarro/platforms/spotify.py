"""Spotify username checker."""
from navarro.core.base import PlatformChecker
from navarro.core.enums import CheckResult
from .mixins import SingleURLMixin


class SpotifyChecker(SingleURLMixin, PlatformChecker):
    """Spotify username checker."""
    
    platform_name = "Spotify"
    platform_key = "spotify"
    URL_PATTERN = "https://open.spotify.com/user/{username}"
    
    def detect_found(self, response) -> bool:
        if response.status_code != 200:
            return False
        return self._current_username.lower() in response.text.lower()
    
    def detect_not_found(self, response) -> bool:
        return response.status_code == 404
    
    def check(self, username: str) -> CheckResult:
        self._current_username = username
        return super().check(username)
