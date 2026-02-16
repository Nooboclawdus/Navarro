"""Behance creative platform username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class BehanceChecker(SingleURLMixin, PlatformChecker):
    """Behance creative portfolio checker."""
    
    platform_name = "Behance"
    platform_key = "behance"
    URL_PATTERN = "https://www.behance.net/{username}"
    
    FOUND_MARKERS = [
        'class="Profile-',
        '"@type":"Person"',
        'class="UserInfo',
        'Appreciations',
        'Projects',
        'class="js-mini-profile',
    ]
    
    NOT_FOUND_MARKERS = [
        "Page not found",
        "Oops! We can't find that page",
        "This page doesn't exist",
        "404",
    ]
    
    def detect_found(self, response) -> bool:
        if response.status_code != 200:
            return False
        text = response.text
        return any(marker in text for marker in self.FOUND_MARKERS)
    
    def detect_not_found(self, response) -> bool:
        if response.status_code == 404:
            return True
        text = response.text
        return any(marker in text for marker in self.NOT_FOUND_MARKERS)
