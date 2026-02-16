"""ResearchGate academic platform username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class ResearchGateChecker(SingleURLMixin, PlatformChecker):
    """ResearchGate researcher profile checker."""
    
    platform_name = "ResearchGate"
    platform_key = "researchgate"
    URL_PATTERN = "https://www.researchgate.net/profile/{username}"
    
    FOUND_MARKERS = [
        'class="nova-legacy-e-text nova-legacy-e-text--size-xl',
        '"@type":"Person"',
        'class="researcher-profile',
        'publications',
        'research-interest',
        'class="profile-header',
    ]
    
    NOT_FOUND_MARKERS = [
        "Page not found",
        "The page you were looking for doesn't exist",
        "This profile is not available",
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
