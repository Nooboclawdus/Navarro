"""Facebook username checker - complex with Graph API fallback."""
import re
import requests
from navarro.core.base import PlatformChecker
from navarro.core.enums import CheckResult


class FacebookChecker(PlatformChecker):
    """
    Facebook username checker.
    
    Strategy:
    1. Try Graph API first (fastest when it works)
    2. For usernames with periods/hyphens, use direct URL check
    3. Use negative detection (look for "not found" indicators)
    """
    
    platform_name = "Facebook"
    platform_key = "facebook"
    
    # User agent that works with Facebook
    FB_UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/125.0.0.0"}
    
    NOT_FOUND_INDICATORS = [
        "This content isn't available right now",
        "This page isn't available",
        "Page Not Found",
        "Content Not Found",
        "The page you requested cannot be displayed",
        "Sorry, this page isn't available",
        '"error":{"message":"Unsupported get request',
        '"error":{"message":"(#803)',
        '"error":{"message":"Invalid username',
        "profile unavailable",
        "Page not found",
    ]
    
    BASIC_FB_INDICATORS = [
        'id="facebook"',
        'property="og:site_name" content="Facebook"',
        'name="twitter:site" content="@facebook"',
        '<title>',
        'www.facebook.com',
    ]
    
    def get_urls(self, username: str) -> list:
        return [f"https://www.facebook.com/{username}"]
    
    def get_profile_url(self, username: str) -> str:
        return f"https://www.facebook.com/{username}"
    
    def detect_found(self, response) -> bool:
        # Not used directly - custom check() method handles this
        return False
    
    def detect_not_found(self, response) -> bool:
        # Not used directly - custom check() method handles this
        return False
    
    def _graph_api_check(self, session, username: str) -> bool:
        """Try Graph API picture endpoint."""
        url = f"https://graph.facebook.com/{username}/picture?type=normal&redirect=false"
        try:
            r = session.get(url, timeout=self.timeout)
            if r.status_code == 200:
                data = r.json().get("data", {})
                return (
                    isinstance(data, dict) and
                    data.get("url") and
                    data.get("width") and
                    "facebook.com" in data.get("url", "")
                )
        except (ValueError, requests.RequestException):
            pass
        return False
    
    def _direct_check(self, session, username: str) -> bool:
        """Check direct profile URL."""
        url = f"https://www.facebook.com/{username}"
        try:
            r = session.get(url, timeout=self.timeout)
            if r.status_code != 200:
                return False
            
            text = r.text
            text_lower = text.lower()
            
            # Check for "not found" indicators
            for indicator in self.NOT_FOUND_INDICATORS:
                if indicator.lower() in text_lower:
                    return False
            
            # Check for basic FB structure
            has_basic_structure = any(ind in text for ind in self.BASIC_FB_INDICATORS)
            if not has_basic_structure:
                return False
            
            # Check for URL match
            url_indicators = [
                f'facebook.com/{username}',
                f'content="https://www.facebook.com/{username}"',
            ]
            has_url_match = any(ind in text for ind in url_indicators)
            
            # For usernames with special chars, be more lenient
            if any(char in username for char in '.-_'):
                return has_basic_structure
            else:
                return has_url_match or '"userID":"' in text or '"pageID":"' in text
            
        except requests.RequestException:
            return False
    
    def check(self, username: str) -> CheckResult:
        """Custom check with Graph API + direct fallback."""
        session = self.session_manager.get_session(self.platform_key)
        session.headers.update(self.FB_UA)
        
        self.rate_limiter.record_request(self.platform_key)
        
        # 1. Try Graph API
        if self._graph_api_check(session, username):
            return CheckResult.FOUND
        
        # 2. Try Graph API with cleaned username
        cleaned = re.sub(r"[.\-]", "", username)
        if cleaned != username and self._graph_api_check(session, cleaned):
            return CheckResult.FOUND
        
        # 3. Direct check
        if self._direct_check(session, username):
            return CheckResult.FOUND
        
        # 4. Direct check with cleaned username
        if cleaned != username and self._direct_check(session, cleaned):
            return CheckResult.FOUND
        
        return CheckResult.NOT_FOUND
