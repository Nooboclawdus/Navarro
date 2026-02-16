"""Rumble video platform username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class RumbleChecker(SingleURLMixin, PlatformChecker):
    """Rumble channel/user checker."""
    
    platform_name = "Rumble"
    platform_key = "rumble"
    URL_PATTERN = "https://rumble.com/c/{username}"
    
    FOUND_MARKERS = [
        'class="channel-header',
        '"@type":"Person"',
        'class="channel-subheader',
        'data-channel-id=',
        'subscribers',
    ]
    
    NOT_FOUND_MARKERS = [
        "Page not found",
        "404 Not Found",
        "Channel not found",
        "This channel does not exist",
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
