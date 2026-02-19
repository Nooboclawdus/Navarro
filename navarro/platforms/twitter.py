"""Twitter/X username checker."""
from navarro.core.base import PlatformChecker
from .mixins import SingleURLMixin


class TwitterChecker(SingleURLMixin, PlatformChecker):
    """Twitter/X username checker."""
    
    platform_name = "Twitter/X"
    platform_key = "twitter"
    URL_PATTERN = "https://x.com/{username}"
    
    FOUND_MARKERS = [
        '"screen_name":',
        'property="og:title"',
        'twitter:creator',
        'data-testid="UserName"',
        '/@{username}',
    ]
    
    NOT_FOUND_MARKERS = [
        "This account doesn't exist",
        "Hmm...this page doesn't exist",
        "User not found",
        "page_not_found",
    ]
    
    def detect_found(self, response) -> bool:
        if response.status_code == 404:
            return False
        if response.status_code == 200:
            text = response.text
            # Twitter returns 200 for missing users but includes "doesn't exist"
            if any(marker in text for marker in self.NOT_FOUND_MARKERS):
                return False
            # Check for valid profile indicators
            return (
                f'"screen_name":"{response.url.split("/")[-1].lower()}"'.lower() in text.lower()
                or 'og:url" content="https://twitter.com/' in text
                or 'og:url" content="https://x.com/' in text
                or response.headers.get('x-twitter-response-tags', '') != 'OverCapacity'
            )
        return False
    
    def detect_not_found(self, response) -> bool:
        if response.status_code == 404:
            return True
        text = response.text
        return any(marker in text for marker in self.NOT_FOUND_MARKERS)
