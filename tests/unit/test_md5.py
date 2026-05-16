"""Unit tests for MD5 hash algorithm."""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.algorithms.hash import MD5


class TestMD5Constants:
    """Test MD5 constants."""

    def test_rotate_amounts_length(self):
        """Test that rotate amounts list has correct length."""
        assert len(MD5.rotate_amounts) == 64

    def test_rotate_amounts_range(self):
        """Test that all rotate amounts are in valid range."""
        for amount in MD5.rotate_amounts:
            assert 1 <= amount <= 32

    def test_constants_length(self):
        """Test that constants list has correct length."""
        assert len(MD5.constants) == 64

    def test_constants_range(self):
        """Test that constants are 32-bit values."""
        for c in MD5.constants:
            assert 0 <= c < 0x100000000


class TestMD5Functions:
    """Test MD5 utility functions."""

    def test_left_rotate_identity(self):
        """Test left rotate by 0 returns same value."""
        assert MD5.left_rotate(0x12345678, 0) == 0x12345678

    def test_left_rotate_full_word(self):
        """Test left rotate by full word size returns same value."""
        assert MD5.left_rotate(0x12345678, 32) == 0x12345678

    def test_left_rotate_halves(self):
        """Test left rotate by 16 swaps halves."""
        assert MD5.left_rotate(0x12345678, 16) == 0x56781234

    def test_filter_space_removes_spaces(self):
        """Test filter_space removes all spaces first."""
        assert MD5.filter_space("a b") == "ab"
        assert MD5.filter_space("a  b") == "ab"

    def test_filter_space_groups(self):
        """Test filter_space groups by 8."""
        result = MD5.filter_space("123456789")
        assert "12345678" in result
        assert "9" in result
        assert len(result) == 10  # 8 chars + space + 1

    def test_filter_space_empty(self):
        """Test filter_space with empty string."""
        assert MD5.filter_space("") == ""

    def test_filter_space_exact_8_chars(self):
        """Test filter_space with exactly 8 chars (no space added)."""
        assert MD5.filter_space("12345678") == "12345678"
