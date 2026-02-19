"""Truth Social platform username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class TruthSocialChecker(SingleURLMixin, PlatformChecker):
    """Truth Social user profile checker."""
    
    platform_name = "Truth Social"
    platform_key = "truthsocial"
    URL_PATTERN = "https://truthsocial.com/@{username}"
    
    FOUND_MARKERS = [
        '"@type":"Person"',
        'class="account__header',
        'class="display-name',
        'data-account-id',
        'followers',
        'truths',  # Truth Social calls posts "truths"
    ]
    
    NOT_FOUND_MARKERS = [
        "This page isn't available",
        "Account not found",
        "The page you requested does not exist",
        "Sorry, that page doesn't exist",
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
