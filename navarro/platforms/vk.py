"""VK username checker."""
from navarro.core.base import PlatformChecker
from navarro.core.enums import CheckResult
from .mixins import SingleURLMixin


class VKChecker(SingleURLMixin, PlatformChecker):
    """VK (VKontakte) username checker."""
    
    platform_name = "VK"
    platform_key = "vk"
    URL_PATTERN = "https://vk.com/{username}"
    
    NOT_FOUND_MARKERS = [
        "Profile not found",
        "страница удалена",
        "страница не найдена",
        "is unavailable",
        "has been deleted",
    ]
    
    def detect_found(self, response) -> bool:
        if response.status_code != 200:
            return False
        text = response.text.lower()
        # Check not-found first
        if any(marker.lower() in text for marker in self.NOT_FOUND_MARKERS):
            return False
        # Profile markers
        if '<div class="page_name"' in response.text or "wall_tab_all" in response.text:
            return True
        return self._current_username.lower() in text
    
    def detect_not_found(self, response) -> bool:
        if response.status_code != 200:
            return True
        return any(marker.lower() in response.text.lower() for marker in self.NOT_FOUND_MARKERS)
    
    def check(self, username: str) -> CheckResult:
        self._current_username = username
        return super().check(username)
