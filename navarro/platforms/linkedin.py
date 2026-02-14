"""LinkedIn username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class LinkedInChecker(SingleURLMixin, PlatformChecker):
    """LinkedIn username checker."""
    
    platform_name = "LinkedIn"
    platform_key = "linkedin"
    URL_PATTERN = "https://www.linkedin.com/in/{username}"
    
    PROFILE_MARKERS = [
        '"profile":',
        '"publicIdentifier":"',
        '"firstName":"',
        '"lastName":"',
        '"profilePicture":',
        'property="og:title"',
    ]
    
    NOT_FOUND_MARKERS = [
        "This page doesn't exist",
        "Page not found",
        "profile-unavailable",
        '"status":404',
    ]
    
    def detect_found(self, response) -> bool:
        if response.status_code != 200:
            return False
        text = response.text
        if any(marker in text for marker in self.NOT_FOUND_MARKERS):
            return False
        return any(marker in text for marker in self.PROFILE_MARKERS)
    
    def detect_not_found(self, response) -> bool:
        if response.status_code == 404:
            return True
        return any(marker in response.text for marker in self.NOT_FOUND_MARKERS)
