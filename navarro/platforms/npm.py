"""npm username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class NpmChecker(SingleURLMixin, PlatformChecker):
    """npm (Node Package Manager) username checker — useful for supply chain OSINT."""
    
    platform_name = "npm"
    platform_key = "npm"
    URL_PATTERN = "https://www.npmjs.com/~{username}"
    
    FOUND_MARKERS = [
        'packages by',
        '"author"',
        'class="w-third',
        'class="b db f5',
    ]
    
    NOT_FOUND_MARKERS = [
        "We cannot find the page you are looking for",
        "404",
        "does not exist",
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
        return False
