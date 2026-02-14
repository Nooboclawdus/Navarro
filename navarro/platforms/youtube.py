"""YouTube username checker."""
from navarro.core.base import PlatformChecker
from .mixins import MultiURLMixin


class YouTubeChecker(MultiURLMixin, PlatformChecker):
    """YouTube username checker - tries multiple URL patterns."""
    
    platform_name = "YouTube"
    platform_key = "youtube"
    URL_PATTERNS = [
        "https://www.youtube.com/@{username}",
        "https://www.youtube.com/c/{username}",
        "https://www.youtube.com/user/{username}",
    ]
    
    FOUND_MARKERS = [
        '"channelId":"',
        '"subscriberCountText"',
        '"viewCountText"',
        '"videoCount"',
        '"@type":"Person"',
        '"externalId":"UC',
    ]
    
    NOT_FOUND_MARKERS = [
        "This page isn't available",
        "404 Not Found",
    ]
    
    def detect_found(self, response) -> bool:
        if response.status_code != 200:
            return False
        text = response.text
        if any(marker in text for marker in self.NOT_FOUND_MARKERS):
            return False
        return any(marker in text for marker in self.FOUND_MARKERS)
    
    def detect_not_found(self, response) -> bool:
        if response.status_code == 404:
            return True
        return any(marker in response.text for marker in self.NOT_FOUND_MARKERS)
