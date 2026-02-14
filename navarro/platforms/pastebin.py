"""Pastebin username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class PastebinChecker(SingleURLMixin, PlatformChecker):
    """Pastebin username checker."""
    
    platform_name = "Pastebin"
    platform_key = "pastebin"
    URL_PATTERN = "https://pastebin.com/u/{username}"
    
    def detect_found(self, response) -> bool:
        if response.status_code != 200:
            return False
        return "pastebin.com" in response.text.lower()
    
    def detect_not_found(self, response) -> bool:
        return response.status_code == 404
