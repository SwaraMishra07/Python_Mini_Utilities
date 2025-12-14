"""
Tests for password_checker.py input validation and strength checking.
"""

import sys
import os

# Add tools directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))

from password_checker import check_password_strength, validate_password_input, MIN_PASSWORD_LENGTH


class TestValidatePasswordInput:
    """Tests for the validate_password_input function."""

    def test_valid_password(self):
        """Test that valid passwords pass validation."""
        is_valid, error = validate_password_input("password123")
        assert is_valid is True
        assert error is None

    def test_none_password(self):
        """Test that None password fails validation."""
        is_valid, error = validate_password_input(None)
        assert is_valid is False
        assert "None" in error

    def test_empty_password(self):
        """Test that empty string fails validation."""
        is_valid, error = validate_password_input("")
        assert is_valid is False
        assert "empty" in error.lower()

    def test_whitespace_only_password(self):
        """Test that whitespace-only password fails validation."""
        is_valid, error = validate_password_input("   ")
        assert is_valid is False
        assert "whitespace" in error.lower()

    def test_too_short_password(self):
        """Test that very short passwords fail validation."""
        is_valid, error = validate_password_input("ab")
        assert is_valid is False
        assert "too short" in error.lower()
        assert str(MIN_PASSWORD_LENGTH) in error

    def test_minimum_length_password(self):
        """Test that password at minimum length passes validation."""
        is_valid, error = validate_password_input("a" * MIN_PASSWORD_LENGTH)
        assert is_valid is True
        assert error is None

    def test_non_string_password(self):
        """Test that non-string password fails validation."""
        is_valid, error = validate_password_input(12345)
        assert is_valid is False
        assert "string" in error.lower()


class TestCheckPasswordStrength:
    """Tests for the check_password_strength function."""

    def test_weak_password_lowercase_only(self):
        """Test that lowercase-only password is weak."""
        result = check_password_strength("password")
        assert result == "Weak"

    def test_weak_password_short(self):
        """Test that short password is weak."""
        result = check_password_strength("pass")
        assert result == "Weak"

    def test_medium_password(self):
        """Test that password with 3 criteria is medium."""
        result = check_password_strength("Password")  # upper + lower + length>=8
        assert result == "Medium"

    def test_strong_password(self):
        """Test that password meeting all criteria is strong."""
        result = check_password_strength("Password1")  # upper + lower + digit + length>=8
        assert result == "Strong"

    def test_empty_password_returns_error(self):
        """Test that empty password returns error message."""
        result = check_password_strength("")
        assert "empty" in result.lower()

    def test_none_password_returns_error(self):
        """Test that None password returns error message."""
        result = check_password_strength(None)
        assert "None" in result

    def test_too_short_password_returns_error(self):
        """Test that too short password returns error message."""
        result = check_password_strength("ab")
        assert "too short" in result.lower()

    def test_whitespace_password_returns_error(self):
        """Test that whitespace-only password returns error message."""
        result = check_password_strength("    ")
        assert "whitespace" in result.lower()


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
