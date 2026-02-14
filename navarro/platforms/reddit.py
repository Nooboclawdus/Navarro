"""Reddit username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class RedditChecker(SingleURLMixin, PlatformChecker):
    """Reddit username checker."""
    
    platform_name = "Reddit"
    platform_key = "reddit"
    URL_PATTERN = "https://www.reddit.com/user/{username}"
    
    FOUND_MARKERS = [
        '"id":"t2_',
        '"isLoggedInUser"',
        'data-user-id',
        '"karma":',
    ]
    
    NOT_FOUND_MARKERS = [
        "u/",
        "page not found",
        "Sorry, nobody on Reddit goes by that name",
        "This account has been suspended",
    ]
    
    def detect_found(self, response) -> bool:
        if response.status_code != 200:
            return False
        text = response.text
        # Check for found markers but not not-found markers
        has_found = any(marker in text for marker in self.FOUND_MARKERS)
        has_not_found = any(marker in text for marker in self.NOT_FOUND_MARKERS)
        return has_found and not has_not_found
    
    def detect_not_found(self, response) -> bool:
        if response.status_code == 404:
            return True
        text = response.text.lower()
        return any(marker.lower() in text for marker in self.NOT_FOUND_MARKERS)
