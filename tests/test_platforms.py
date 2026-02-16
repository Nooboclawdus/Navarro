"""Tests for platform checkers."""
import pytest
from navarro.platforms import (
    list_platforms,
    PLATFORM_REGISTRY,
    get_platform_checker,
)
from navarro.core import RateLimiter, SessionManager


class TestPlatformRegistry:
    """Test platform registry functionality."""
    
    def test_platform_count(self):
        """Test we have expected number of platforms."""
        platforms = list_platforms()
        assert len(platforms) >= 35, f"Expected at least 35 platforms, got {len(platforms)}"
    
    def test_all_platforms_instantiable(self):
        """Test all registered platforms can be instantiated."""
        rate_limiter = RateLimiter()
        session_manager = SessionManager()
        
        for name in list_platforms():
            checker = get_platform_checker(name, rate_limiter, session_manager)
            assert checker is not None
            assert checker.platform_name == name
    
    def test_platform_has_required_attributes(self):
        """Test all platforms have required attributes."""
        rate_limiter = RateLimiter()
        session_manager = SessionManager()
        
        for name in list_platforms():
            checker = get_platform_checker(name, rate_limiter, session_manager)
            assert hasattr(checker, 'platform_name')
            assert hasattr(checker, 'platform_key')
            assert hasattr(checker, 'get_urls')
            assert hasattr(checker, 'detect_found')
            assert hasattr(checker, 'detect_not_found')
    
    def test_platform_urls_not_empty(self):
        """Test platforms return non-empty URLs."""
        rate_limiter = RateLimiter()
        session_manager = SessionManager()
        
        for name in list_platforms():
            checker = get_platform_checker(name, rate_limiter, session_manager)
            urls = checker.get_urls("testuser")
            assert len(urls) > 0, f"{name} returned no URLs"
            assert all(url.startswith("http") for url in urls), f"{name} returned invalid URLs"


class TestNewPlatforms:
    """Test newly added platforms (alt-tech, academic, creative)."""
    
    @pytest.fixture
    def rate_limiter(self):
        return RateLimiter()
    
    @pytest.fixture
    def session_manager(self):
        return SessionManager()
    
    def test_rumble_url_pattern(self, rate_limiter, session_manager):
        """Test Rumble URL generation."""
        checker = get_platform_checker("Rumble", rate_limiter, session_manager)
        urls = checker.get_urls("testuser")
        assert "rumble.com/c/testuser" in urls[0]
    
    def test_bitchute_url_pattern(self, rate_limiter, session_manager):
        """Test BitChute URL generation."""
        checker = get_platform_checker("BitChute", rate_limiter, session_manager)
        urls = checker.get_urls("testuser")
        assert "bitchute.com/channel/testuser" in urls[0]
    
    def test_gab_url_pattern(self, rate_limiter, session_manager):
        """Test Gab URL generation."""
        checker = get_platform_checker("Gab", rate_limiter, session_manager)
        urls = checker.get_urls("testuser")
        assert "gab.com/testuser" in urls[0]
    
    def test_truthsocial_url_pattern(self, rate_limiter, session_manager):
        """Test Truth Social URL generation."""
        checker = get_platform_checker("Truth Social", rate_limiter, session_manager)
        urls = checker.get_urls("testuser")
        assert "truthsocial.com/@testuser" in urls[0]
    
    def test_gettr_url_pattern(self, rate_limiter, session_manager):
        """Test Gettr URL generation."""
        checker = get_platform_checker("Gettr", rate_limiter, session_manager)
        urls = checker.get_urls("testuser")
        assert "gettr.com/user/testuser" in urls[0]
    
    def test_researchgate_url_pattern(self, rate_limiter, session_manager):
        """Test ResearchGate URL generation."""
        checker = get_platform_checker("ResearchGate", rate_limiter, session_manager)
        urls = checker.get_urls("testuser")
        assert "researchgate.net/profile/testuser" in urls[0]
    
    def test_academia_url_pattern(self, rate_limiter, session_manager):
        """Test Academia.edu URL generation."""
        checker = get_platform_checker("Academia.edu", rate_limiter, session_manager)
        urls = checker.get_urls("testuser")
        assert "academia.edu/testuser" in urls[0]
    
    def test_behance_url_pattern(self, rate_limiter, session_manager):
        """Test Behance URL generation."""
        checker = get_platform_checker("Behance", rate_limiter, session_manager)
        urls = checker.get_urls("testuser")
        assert "behance.net/testuser" in urls[0]
    
    def test_dribbble_url_pattern(self, rate_limiter, session_manager):
        """Test Dribbble URL generation."""
        checker = get_platform_checker("Dribbble", rate_limiter, session_manager)
        urls = checker.get_urls("testuser")
        assert "dribbble.com/testuser" in urls[0]
