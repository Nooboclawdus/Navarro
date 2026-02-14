"""
Navarro - OSINT Username Checker

A modular Python tool that checks for username availability
across multiple social media and web platforms.
"""
from navarro.core import (
    CheckResult,
    PlatformChecker,
    RateLimiter,
    SessionManager,
)
from navarro.platforms import (
    get_platform_checker,
    get_all_checkers,
    list_platforms,
    PLATFORM_REGISTRY,
)

__version__ = "2.0.0"
__all__ = [
    # Core
    'CheckResult',
    'PlatformChecker',
    'RateLimiter',
    'SessionManager',
    # Platforms
    'get_platform_checker',
    'get_all_checkers',
    'list_platforms',
    'PLATFORM_REGISTRY',
]
