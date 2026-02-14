"""Platform checkers registry."""
from typing import Dict, Type

from navarro.core import PlatformChecker, RateLimiter, SessionManager

# Import all platform checkers
from .github import GitHubChecker
from .gitlab import GitLabChecker
from .reddit import RedditChecker
from .instagram import InstagramChecker
from .tiktok import TikTokChecker
from .linkedin import LinkedInChecker
from .pastebin import PastebinChecker
from .telegram import TelegramChecker
from .snapchat import SnapchatChecker
from .strava import StravaChecker
from .threads import ThreadsChecker
from .mastodon import MastodonChecker
from .bluesky import BlueskyChecker
from .spotify import SpotifyChecker
from .soundcloud import SoundCloudChecker
from .youtube import YouTubeChecker

# Platform registry - maps display names to checker classes
PLATFORM_REGISTRY: Dict[str, Type[PlatformChecker]] = {
    "GitHub": GitHubChecker,
    "GitLab": GitLabChecker,
    "Reddit": RedditChecker,
    "Instagram": InstagramChecker,
    "TikTok": TikTokChecker,
    "LinkedIn": LinkedInChecker,
    "Pastebin": PastebinChecker,
    "Telegram": TelegramChecker,
    "Snapchat": SnapchatChecker,
    "Strava": StravaChecker,
    "Threads": ThreadsChecker,
    "Mastodon": MastodonChecker,
    "Bluesky": BlueskyChecker,
    "Spotify": SpotifyChecker,
    "SoundCloud": SoundCloudChecker,
    "YouTube": YouTubeChecker,
    # More platforms will be added as they're migrated
}


def get_platform_checker(
    platform_name: str, 
    rate_limiter: RateLimiter, 
    session_manager: SessionManager
) -> PlatformChecker:
    """Factory function to instantiate platform checkers."""
    checker_class = PLATFORM_REGISTRY.get(platform_name)
    if checker_class:
        return checker_class(rate_limiter, session_manager)
    raise ValueError(f"Unknown platform: {platform_name}")


def get_all_checkers(
    rate_limiter: RateLimiter, 
    session_manager: SessionManager
) -> Dict[str, PlatformChecker]:
    """Get instances of all registered platform checkers."""
    return {
        name: checker_class(rate_limiter, session_manager)
        for name, checker_class in PLATFORM_REGISTRY.items()
    }


def list_platforms() -> list:
    """List all available platforms."""
    return list(PLATFORM_REGISTRY.keys())
