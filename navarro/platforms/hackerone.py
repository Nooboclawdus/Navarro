"""HackerOne username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class HackerOneChecker(SingleURLMixin, PlatformChecker):
    """HackerOne username checker — for OSINT on security researchers."""
    
    platform_name = "HackerOne"
    platform_key = "hackerone"
    URL_PATTERN = "https://hackerone.com/{username}"
    
    FOUND_MARKERS = [
        '"username":',
        'hacker-profile',
        'profile__intro',
        '"reputation":',
        'class="report-count',
        '"signal":',
    ]
    
    NOT_FOUND_MARKERS = [
        "No account was found",
        "Page not found",
        "Something went wrong",
        '"error":"not_found"',
    ]
    
    def detect_found(self, response) -> bool:
        if response.status_code == 404:
            return False
        if response.status_code == 200:
            text = response.text
            if any(marker in text for marker in self.NOT_FOUND_MARKERS):
                return False
            return any(marker in text for marker in self.FOUND_MARKERS)
        return False
    
    def detect_not_found(self, response) -> bool:
        if response.status_code == 404:
            return True
        text = response.text
        return any(marker in text for marker in self.NOT_FOUND_MARKERS)
