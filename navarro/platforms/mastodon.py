"""Mastodon username checker."""
import requests
from navarro.core.base import PlatformChecker
from navarro.core.enums import CheckResult


class MastodonChecker(PlatformChecker):
    """Mastodon username checker - checks multiple instances."""
    
    platform_name = "Mastodon"
    platform_key = "mastodon"
    
    INSTANCES = [
        "mastodon.social",
        "hachyderm.io",
        "infosec.exchange",
    ]
    
    def get_urls(self, username: str) -> list:
        return [f"https://{inst}/@{username}" for inst in self.INSTANCES]
    
    def get_profile_url(self, username: str) -> str:
        return f"https://mastodon.social/@{username}"
    
    def detect_found(self, response) -> bool:
        if response.status_code != 200:
            return False
        text = response.text.lower()
        return f"@{self._current_username.lower()}" in text
    
    def detect_not_found(self, response) -> bool:
        return response.status_code == 404
    
    def check(self, username: str) -> CheckResult:
        """Override to try multiple instances."""
        self._current_username = username
        
        wait_time = self.rate_limiter.should_wait(self.platform_key)
        if wait_time > 0:
            import time
            time.sleep(wait_time)
        
        session = self.session_manager.get_session(self.platform_key)
        
        for url in self.get_urls(username):
            try:
                response = session.get(url, timeout=self.timeout)
                
                if self.check_rate_limit(response):
                    self.rate_limiter.record_request(self.platform_key, was_rate_limited=True)
                    return CheckResult.RATE_LIMITED
                
                if self.detect_found(response):
                    self.rate_limiter.record_request(self.platform_key)
                    return CheckResult.FOUND
                
            except requests.exceptions.Timeout:
                continue
            except requests.exceptions.RequestException:
                continue
        
        self.rate_limiter.record_request(self.platform_key)
        return CheckResult.NOT_FOUND
