"""Threads username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class ThreadsChecker(SingleURLMixin, PlatformChecker):
    """Threads (Meta) username checker."""
    
    platform_name = "Threads"
    platform_key = "threads"
    URL_PATTERN = "https://www.threads.net/@{username}"
    
    FOUND_MARKERS = [
        '"user":{"pk"',
        '"profile_pic_url"',
        '"thread_items"',
    ]
    
    NOT_FOUND_MARKERS = [
        "Sorry, this page isn't available",
        "User not found",
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
