"""Instagram username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class InstagramChecker(SingleURLMixin, PlatformChecker):
    """Instagram username checker."""
    
    platform_name = "Instagram"
    platform_key = "instagram"
    URL_PATTERN = "https://www.instagram.com/{username}/"
    
    # JSON-like patterns in Instagram's HTML
    FOUND_MARKERS = [
        '"username":"',
        '"profile_pic_url"',
        '"biography"',
        '"edge_owner_to_timeline_media"',
        '"is_private"',
        'property="og:title"',
    ]
    
    NOT_FOUND_MARKERS = [
        "Sorry, this page isn't available",
        "The link you followed may be broken",
        "this page is not available",
    ]
    
    def detect_found(self, response) -> bool:
        if response.status_code != 200:
            return False
        text = response.text
        # Must have found markers AND not have not-found markers
        has_found = any(marker in text for marker in self.FOUND_MARKERS)
        has_not_found = any(marker in text for marker in self.NOT_FOUND_MARKERS)
        return has_found and not has_not_found
    
    def detect_not_found(self, response) -> bool:
        if response.status_code == 404:
            return True
        text = response.text
        return any(marker in text for marker in self.NOT_FOUND_MARKERS)
