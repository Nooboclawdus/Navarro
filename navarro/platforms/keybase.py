"""Keybase username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class KeybaseChecker(SingleURLMixin, PlatformChecker):
    """Keybase username checker."""
    
    platform_name = "Keybase"
    platform_key = "keybase"
    URL_PATTERN = "https://keybase.io/{username}"
    
    FOUND_MARKERS = [
        '"proofs_summary"',
        '"stellar"',
        '"bitcoin"',
    ]
    
    NOT_FOUND_MARKERS = [
        "User not found",
        "No such user",
        "404",
    ]
    
    def detect_found(self, response) -> bool:
        if response.status_code != 200:
            return False
        text = response.text
        if any(marker in text for marker in self.NOT_FOUND_MARKERS):
            return False
        return any(marker in text for marker in self.FOUND_MARKERS)
    
    def detect_not_found(self, response) -> bool:
        if response.status_code != 200:
            return True
        return any(marker in response.text for marker in self.NOT_FOUND_MARKERS)
