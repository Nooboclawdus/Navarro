"""GitLab username checker."""
import re
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class GitLabChecker(SingleURLMixin, PlatformChecker):
    """GitLab username checker."""
    
    platform_name = "GitLab"
    platform_key = "gitlab"
    URL_PATTERN = "https://gitlab.com/{username}"
    
    def detect_found(self, response) -> bool:
        if response.status_code != 200:
            return False
        # GitLab has username in h1 tag
        return bool(re.search(r'<h1>[\w\-]+', response.text))
    
    def detect_not_found(self, response) -> bool:
        return response.status_code == 404
