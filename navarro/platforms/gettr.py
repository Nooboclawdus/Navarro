"""Gettr social platform username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class GettrChecker(SingleURLMixin, PlatformChecker):
    """Gettr user profile checker."""
    
    platform_name = "Gettr"
    platform_key = "gettr"
    URL_PATTERN = "https://gettr.com/user/{username}"
    
    FOUND_MARKERS = [
        '"username":',
        'class="profile-bio',
        'class="user-card',
        'followers',
        'following',
        '"ousrname":',  # Gettr API sometimes uses this
    ]
    
    NOT_FOUND_MARKERS = [
        "User not found",
        "This user doesn't exist",
        "Page not found",
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
