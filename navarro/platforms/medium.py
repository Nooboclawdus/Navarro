"""Medium username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class MediumChecker(SingleURLMixin, PlatformChecker):
    """Medium username checker."""
    
    platform_name = "Medium"
    platform_key = "medium"
    URL_PATTERN = "https://medium.com/@{username}"
    
    FOUND_MARKERS = [
        '"@type":"Person"',
        '"creator":{"@type":"Person"',
        '"UserFollowButton"',
    ]
    
    NOT_FOUND_MARKERS = [
        "We couldn't find this page",
        "PAGE NOT FOUND",
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
        if response.status_code == 404:
            return True
        return any(marker in response.text for marker in self.NOT_FOUND_MARKERS)
