"""Strava username checker."""
from navarro.core.base import PlatformChecker
from navarro.core.enums import CheckResult
from .mixins import SingleURLMixin


class StravaChecker(SingleURLMixin, PlatformChecker):
    """Strava username checker."""
    
    platform_name = "Strava"
    platform_key = "strava"
    URL_PATTERN = "https://www.strava.com/athletes/{username}"
    
    def detect_found(self, response) -> bool:
        if response.status_code != 200:
            return False
        text = response.text
        return "Athlete" in text or self._current_username in text
    
    def detect_not_found(self, response) -> bool:
        return response.status_code == 404
    
    def check(self, username: str) -> CheckResult:
        self._current_username = username
        return super().check(username)
