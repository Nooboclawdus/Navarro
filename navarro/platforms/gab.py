"""Gab social platform username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class GabChecker(SingleURLMixin, PlatformChecker):
    """Gab user profile checker."""
    
    platform_name = "Gab"
    platform_key = "gab"
    URL_PATTERN = "https://gab.com/{username}"
    
    FOUND_MARKERS = [
        '"@type":"Person"',
        'class="account__header',
        'class="display-name',
        'data-account-id',
        'followers',
        'following',
    ]
    
    NOT_FOUND_MARKERS = [
        "This page isn't available",
        "Account not found",
        "The page you requested does not exist",
        "Sorry, that page doesn't exist",
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
