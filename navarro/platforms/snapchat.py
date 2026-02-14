"""Snapchat username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class SnapchatChecker(SingleURLMixin, PlatformChecker):
    """Snapchat username checker."""
    
    platform_name = "Snapchat"
    platform_key = "snapchat"
    URL_PATTERN = "https://www.snapchat.com/add/{username}"
    
    def detect_found(self, response) -> bool:
        if response.status_code != 200:
            return False
        return 'Snapcode' in response.text
    
    def detect_not_found(self, response) -> bool:
        return response.status_code == 404 or 'Snapcode' not in response.text
