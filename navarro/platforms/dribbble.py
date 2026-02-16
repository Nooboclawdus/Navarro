"""Dribbble design platform username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class DribbbleChecker(SingleURLMixin, PlatformChecker):
    """Dribbble designer profile checker."""
    
    platform_name = "Dribbble"
    platform_key = "dribbble"
    URL_PATTERN = "https://dribbble.com/{username}"
    
    FOUND_MARKERS = [
        'class="profile-info',
        '"@type":"Person"',
        'class="bio',
        'Shots',
        'Followers',
        'class="shot-thumbnail',
    ]
    
    NOT_FOUND_MARKERS = [
        "Page not found",
        "Sorry, this page isn't available",
        "404 Not Found",
        "This page doesn't exist",
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
