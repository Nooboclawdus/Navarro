"""Mixins for common platform check patterns."""
from typing import List
import requests


class SingleURLMixin:
    """
    For platforms with a single URL pattern.
    Subclass defines URL_PATTERN (format string with {username}).
    """
    
    URL_PATTERN: str = ""
    
    def get_urls(self, username: str) -> List[str]:
        return [self.URL_PATTERN.format(username=username)]
    
    def get_profile_url(self, username: str) -> str:
        return self.URL_PATTERN.format(username=username)


class MultiURLMixin:
    """
    For platforms that need to try multiple URL patterns.
    Subclass defines URL_PATTERNS list.
    """
    
    URL_PATTERNS: List[str] = []
    
    def get_urls(self, username: str) -> List[str]:
        return [pattern.format(username=username) for pattern in self.URL_PATTERNS]
    
    def get_profile_url(self, username: str) -> str:
        return self.URL_PATTERNS[0].format(username=username) if self.URL_PATTERNS else ""


class SimpleTextMarkerMixin:
    """
    For platforms that use simple text marker detection.
    Subclass defines FOUND_MARKERS and NOT_FOUND_MARKERS.
    """
    
    FOUND_MARKERS: List[str] = []
    NOT_FOUND_MARKERS: List[str] = []
    
    def detect_found(self, response: requests.Response) -> bool:
        if response.status_code != 200:
            return False
        text = response.text
        return any(marker in text for marker in self.FOUND_MARKERS)
    
    def detect_not_found(self, response: requests.Response) -> bool:
        text = response.text
        return any(marker in text for marker in self.NOT_FOUND_MARKERS)


class JSONMarkerMixin:
    """
    For platforms that have JSON patterns in response.
    """
    
    JSON_FOUND_PATTERNS: List[str] = []
    JSON_NOT_FOUND_PATTERNS: List[str] = []
    
    def detect_found(self, response: requests.Response) -> bool:
        if response.status_code != 200:
            return False
        text = response.text
        return any(pattern in text for pattern in self.JSON_FOUND_PATTERNS)
    
    def detect_not_found(self, response: requests.Response) -> bool:
        text = response.text
        return any(pattern in text for pattern in self.JSON_NOT_FOUND_PATTERNS)


class StatusCodeMixin:
    """
    For platforms where status code alone determines result.
    200 = found, 404 = not found.
    """
    
    def detect_found(self, response: requests.Response) -> bool:
        return response.status_code == 200
    
    def detect_not_found(self, response: requests.Response) -> bool:
        return response.status_code == 404
