"""Academia.edu academic platform username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class AcademiaChecker(SingleURLMixin, PlatformChecker):
    """Academia.edu researcher profile checker."""
    
    platform_name = "Academia.edu"
    platform_key = "academia"
    URL_PATTERN = "https://independent.academia.edu/{username}"
    
    FOUND_MARKERS = [
        'class="profile-name',
        '"@type":"Person"',
        'class="profile-header',
        'papers',
        'followers',
        'class="js-profile',
    ]
    
    NOT_FOUND_MARKERS = [
        "Page not found",
        "This profile doesn't exist",
        "The page you were looking for doesn't exist",
        "404 Not Found",
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
