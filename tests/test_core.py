"""Tests for core components."""
import pytest
from navarro.core import CheckResult


class TestCheckResult:
    """Test CheckResult enum."""
    
    def test_success_results(self):
        """Test is_success for definitive results."""
        assert CheckResult.FOUND.is_success() is True
        assert CheckResult.NOT_FOUND.is_success() is True
    
    def test_error_results(self):
        """Test is_success returns False for errors."""
        assert CheckResult.RATE_LIMITED.is_success() is False
        assert CheckResult.TIMEOUT.is_success() is False
        assert CheckResult.NETWORK_ERROR.is_success() is False
        assert CheckResult.UNKNOWN_ERROR.is_success() is False
    
    def test_is_error(self):
        """Test is_error method."""
        assert CheckResult.FOUND.is_error() is False
        assert CheckResult.NOT_FOUND.is_error() is False
        assert CheckResult.RATE_LIMITED.is_error() is True
        assert CheckResult.TIMEOUT.is_error() is True
        assert CheckResult.NETWORK_ERROR.is_error() is True
        assert CheckResult.UNKNOWN_ERROR.is_error() is True
