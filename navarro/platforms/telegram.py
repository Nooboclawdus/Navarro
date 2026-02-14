"""Telegram username checker."""
from navarro.core.base import PlatformChecker
from navarro.core.enums import CheckResult
from .mixins import SingleURLMixin


class TelegramChecker(SingleURLMixin, PlatformChecker):
    """Telegram username checker."""
    
    platform_name = "Telegram"
    platform_key = "telegram"
    URL_PATTERN = "https://t.me/{username}"
    
    def detect_found(self, response) -> bool:
        if response.status_code != 200:
            return False
        
        # Invalid usernames redirect to telegram.org
        if response.url.startswith('https://telegram.org'):
            return False
        
        text = response.text
        username = self._current_username
        
        # Structured data
        if '"@type":"Person"' in text or '"@type":"Organization"' in text:
            return True
        
        # OG image (not default logo)
        if 'og:image' in text and 'cdn' in text:
            if 'telegram_logo' not in text and 'default' not in text:
                return True
        
        # Meta tags with username
        has_title = 'property="og:title"' in text
        has_desc = 'property="og:description"' in text
        if has_title and has_desc and username.lower() in text.lower():
            return True
        
        return False
    
    def detect_not_found(self, response) -> bool:
        if response.status_code == 404:
            return True
        if response.url.startswith('https://telegram.org'):
            return True
        return False
    
    def check(self, username: str) -> CheckResult:
        """Override to store username for detection."""
        self._current_username = username
        return super().check(username)
