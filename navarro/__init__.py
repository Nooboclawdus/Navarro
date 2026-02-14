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
    validate_username,
)
from navarro.platforms import (
    get_platform_checker,
    get_all_checkers,
    list_platforms,
    PLATFORM_REGISTRY,
)

__version__ = "2.0.1"
__all__ = [
    # Core
    'CheckResult',
    'PlatformChecker',
    'RateLimiter',
    'SessionManager',
    'validate_username',
    # Platforms
    'get_platform_checker',
    'get_all_checkers',
    'list_platforms',
    'PLATFORM_REGISTRY',
]
