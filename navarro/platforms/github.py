"""GitHub username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class GitHubChecker(SingleURLMixin, PlatformChecker):
    """GitHub username checker."""
    
    platform_name = "GitHub"
    platform_key = "github"
    URL_PATTERN = "https://github.com/{username}"
    
    FOUND_MARKERS = [
        '"login":',
        '"avatar_url":',
        'data-hovercard-type="user"',
        'class="p-name vcard-fullname',
    ]
    
    NOT_FOUND_MARKERS = [
        "Not Found",
        "This is not the web page you are looking for",
        "Page not found",
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
