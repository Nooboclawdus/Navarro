"""Base class for platform checkers."""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
import re
import time
import requests

from .enums import CheckResult


# Username validation pattern (most platforms)
USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_.\-]{1,64}$')


def validate_username(username: str) -> Tuple[bool, str]:
    """
    Validate username format.
    Returns (is_valid, error_message).
    """
    if not username:
        return False, "Username cannot be empty"
    if len(username) > 64:
        return False, "Username too long (max 64 characters)"
    if not USERNAME_PATTERN.match(username):
        return False, "Username contains invalid characters (allowed: a-z, A-Z, 0-9, _, ., -)"
    return True, ""


class PlatformChecker(ABC):
    """
    Abstract base class for platform username checkers.
    
    Subclasses must implement:
    - platform_name: Display name of the platform
    - platform_key: Key for rate limiting (lowercase)
    - get_urls(username) -> List[str]
    - detect_found(response) -> bool
    - detect_not_found(response) -> bool
    """
    
    def __init__(self, rate_limiter, session_manager):
        self.rate_limiter = rate_limiter
        self.session_manager = session_manager
        self.timeout = 8
    
    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Return the display name of the platform."""
        pass
    
    @property
    @abstractmethod
    def platform_key(self) -> str:
        """Return the key used for rate limiting/sessions (lowercase)."""
        pass
    
    @abstractmethod
    def get_urls(self, username: str) -> List[str]:
        """
        Return list of URLs to check for this username.
        Most platforms return one URL, some return multiple to try.
        """
        pass
    
    @abstractmethod
    def detect_found(self, response: requests.Response) -> bool:
        """
        Analyze response to determine if profile exists.
        Return True if positive indicators found.
        """
        pass
    
    @abstractmethod
    def detect_not_found(self, response: requests.Response) -> bool:
        """
        Analyze response to determine if profile definitely doesn't exist.
        Return True if negative indicators found.
        """
        pass
    
    def get_profile_url(self, username: str) -> str:
        """Return the canonical profile URL."""
        urls = self.get_urls(username)
        return urls[0] if urls else ""
    
    def check_rate_limit(self, response: requests.Response) -> bool:
        """
        Check if response indicates rate limiting.
        Can be overridden for platform-specific logic.
        """
        if response.status_code == 429:
            return True
        
        if 'retry-after' in response.headers:
            return True
        
        remaining_headers = ['x-ratelimit-remaining', 'x-rate-limit-remaining']
        for header in remaining_headers:
            if header in response.headers:
                try:
                    remaining = int(response.headers.get(header, '1'))
                    if remaining == 0:
                        return True
                except ValueError:
                    pass
        
        rate_limit_patterns = [
            "rate limit exceeded",
            "too many requests",
            "429 too many requests",
        ]
        
        response_text = response.text.lower()
        return any(pattern in response_text for pattern in rate_limit_patterns)
    
    def check(self, username: str) -> CheckResult:
        """
        Main check method - handles the full flow.
        Subclasses rarely need to override this.
        """
        # Validate username
        is_valid, _ = validate_username(username)
        if not is_valid:
            return CheckResult.UNKNOWN_ERROR
        
        # Wait if rate limited
        wait_time = self.rate_limiter.should_wait(self.platform_key)
        if wait_time > 0:
            time.sleep(wait_time)
        
        # Get session
        session = self.session_manager.get_session(self.platform_key)
        
        # Try each URL
        for url in self.get_urls(username):
            try:
                response = session.get(url, timeout=self.timeout, allow_redirects=True)
                
                # Check rate limiting
                if self.check_rate_limit(response):
                    self.rate_limiter.record_request(self.platform_key, was_rate_limited=True)
                    return CheckResult.RATE_LIMITED
                
                # Record successful request
                self.rate_limiter.record_request(self.platform_key)
                
                # Check for not found first (more definitive)
                if self.detect_not_found(response):
                    continue  # Try next URL if multiple
                
                # Check for found indicators
                if self.detect_found(response):
                    return CheckResult.FOUND
                
            except requests.exceptions.Timeout:
                return CheckResult.TIMEOUT
            except requests.exceptions.ConnectionError:
                return CheckResult.NETWORK_ERROR
            except requests.exceptions.RequestException:
                return CheckResult.NETWORK_ERROR
            except Exception:
                return CheckResult.UNKNOWN_ERROR
        
        # If we tried all URLs and found nothing
        return CheckResult.NOT_FOUND
