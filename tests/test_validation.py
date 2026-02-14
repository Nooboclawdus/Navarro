"""Tests for username validation."""
import pytest
from navarro.core.base import validate_username


class TestValidateUsername:
    """Test username validation function."""
    
    def test_valid_alphanumeric(self):
        """Test valid alphanumeric usernames."""
        assert validate_username("johndoe")[0] is True
        assert validate_username("user123")[0] is True
        assert validate_username("JohnDoe")[0] is True
    
    def test_valid_with_underscore(self):
        """Test valid usernames with underscores."""
        assert validate_username("john_doe")[0] is True
        assert validate_username("_username_")[0] is True
    
    def test_valid_with_dots_hyphens(self):
        """Test valid usernames with dots and hyphens."""
        assert validate_username("john.doe")[0] is True
        assert validate_username("john-doe")[0] is True
        assert validate_username("john.doe-123")[0] is True
    
    def test_empty_username(self):
        """Test empty username is rejected."""
        is_valid, msg = validate_username("")
        assert is_valid is False
        assert "empty" in msg.lower()
    
    def test_too_long_username(self):
        """Test username over 64 chars is rejected."""
        long_name = "a" * 65
        is_valid, msg = validate_username(long_name)
        assert is_valid is False
        assert "long" in msg.lower()
    
    def test_max_length_username(self):
        """Test username at exactly 64 chars is accepted."""
        max_name = "a" * 64
        assert validate_username(max_name)[0] is True
    
    def test_invalid_special_chars(self):
        """Test special characters are rejected."""
        assert validate_username("john@doe")[0] is False
        assert validate_username("john doe")[0] is False  # space
        assert validate_username("john!doe")[0] is False
        assert validate_username("john#doe")[0] is False
        assert validate_username("john$doe")[0] is False
        assert validate_username("john/doe")[0] is False
    
    def test_unicode_rejected(self):
        """Test unicode characters are rejected."""
        assert validate_username("john👍")[0] is False
        assert validate_username("ジョン")[0] is False
