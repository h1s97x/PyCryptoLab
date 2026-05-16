"""Unit tests for SHA-1 hash algorithm."""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.algorithms.hash.SHA1 import (
    change_result_format, format_w, choose, majority, _left_rotate, primes
)


class TestSHA1Helpers:
    """Test SHA-1 helper functions."""

    def test_change_result_format(self):
        """Test result format change."""
        result = change_result_format("abcdef12")
        # Should have spaces every 2 chars
        parts = result.split()
        assert len(parts) == 4
        assert all(len(p) == 2 for p in parts)

    def test_change_result_format_empty(self):
        """Test format of empty string."""
        result = change_result_format("")
        assert result == ""

    def test_format_w(self):
        """Test W array formatting."""
        w = [0x12345678, 0x9abcdef0]
        result = format_w(w)
        assert '12345678' in result
        assert '9abcdef0' in result

    def test_format_w_empty(self):
        """Test format of empty W array."""
        result = format_w([])
        assert result == ""

    def test_choose_function(self):
        """Test the Ch (choose) function."""
        # If x bit is 1, result = y; if x bit is 0, result = z
        # x=0xFF, y=0xAA, z=0x55 -> result should be 0xAA
        result = choose(0xFF, 0xAA, 0x55)
        assert result == 0xAA

    def test_majority_function(self):
        """Test the Maj (majority) function."""
        # Result bit is 1 if at least 2 of x,y,z bits are 1
        result = majority(0xFF, 0xFF, 0x00)
        assert result == 0xFF

        result = majority(0xFF, 0x00, 0x00)
        assert result == 0x00

    def test_left_rotate(self):
        """Test left rotate function."""
        # Rotate 0x12345678 left by 8 bits
        result = _left_rotate(0x12345678, 8)
        # ((0x12345678 << 8) | (0x12345678 >> 24)) & 0xffffffff
        expected = ((0x12345678 << 8) | (0x12345678 >> 24)) & 0xffffffff
        assert result == expected

    def test_left_rotate_full(self):
        """Test left rotate by 32 bits."""
        result = _left_rotate(0x12345678, 32)
        assert result == 0x12345678

    def test_left_rotate_preserves_32bits(self):
        """Test that left rotate always returns 32-bit value."""
        for val in [0, 1, 0xFFFFFFFF, 0x12345678]:
            result = _left_rotate(val, 16)
            assert 0 <= result <= 0xFFFFFFFF


class TestPrimes:
    """Test prime number generator."""

    def test_primes_generator(self):
        """Test that primes generator yields correct primes."""
        p = primes()
        first_primes = [next(p) for _ in range(10)]
        expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        assert first_primes == expected

    def test_primes_infinite(self):
        """Test that primes generator is infinite."""
        p = primes()
        # Get 100th prime
        for _ in range(99):
            next(p)
        assert next(p) == 541  # 100th prime
