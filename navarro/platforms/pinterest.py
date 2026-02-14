"""Pinterest username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class PinterestChecker(SingleURLMixin, PlatformChecker):
    """Pinterest username checker."""
    
    platform_name = "Pinterest"
    platform_key = "pinterest"
    URL_PATTERN = "https://www.pinterest.com/{username}/"
    
    FOUND_MARKERS = [
        '"@type":"Person"',
        '"profileOwner":',
        '"pinterestapp:followers"',
    ]
    
    NOT_FOUND_MARKERS = [
        "User not found",
        "Sorry! We couldn't find",
        "Oops! We couldn't find",
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
