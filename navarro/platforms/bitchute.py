"""BitChute video platform username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class BitChuteChecker(SingleURLMixin, PlatformChecker):
    """BitChute channel checker."""
    
    platform_name = "BitChute"
    platform_key = "bitchute"
    URL_PATTERN = "https://www.bitchute.com/channel/{username}/"
    
    FOUND_MARKERS = [
        'class="channel-banner',
        'class="owner',
        'channel-videos',
        'subscriber-count',
        'class="name"',
    ]
    
    NOT_FOUND_MARKERS = [
        "Channel Not Found",
        "This channel does not exist",
        "Page Not Found",
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
