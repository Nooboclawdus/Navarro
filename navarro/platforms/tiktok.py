"""TikTok username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class TikTokChecker(SingleURLMixin, PlatformChecker):
    """TikTok username checker."""
    
    platform_name = "TikTok"
    platform_key = "tiktok"
    URL_PATTERN = "https://www.tiktok.com/@{username}"
    
    FOUND_PATTERNS = [
        '"uniqueId":"',
        '"__typename":"User"',
        '"followerCount":',
        '"videoCount":',
    ]
    
    NOT_FOUND_MARKERS = [
        "Couldn't find this account",
        "Impossible de trouver ce compte",
        '<h1>404</h1>',
        '"statusCode":10202',
    ]
    
    def detect_found(self, response) -> bool:
        if response.status_code != 200:
            return False
        text = response.text
        # Check not-found first
        if any(marker in text for marker in self.NOT_FOUND_MARKERS):
            return False
        return any(pattern in text for pattern in self.FOUND_PATTERNS)
    
    def detect_not_found(self, response) -> bool:
        if response.status_code == 404:
            return True
        return any(marker in response.text for marker in self.NOT_FOUND_MARKERS)
