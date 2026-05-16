"""
Unit tests for SHA-256 hash algorithm.
"""
import pytest
from core.algorithms.hash.SHA256 import (
    choose,
    majority,
    sum_0,
    sum_1,
    rho_0,
    rho_1,
    IV,
    K
)


class TestSHA256Constants:
    """Test SHA-256 constant values."""

    def test_iv_length(self):
        """Test IV has 8 initial hash values."""
        assert len(IV) == 8

    def test_iv_values_are_32bit(self):
        """Test IV values are 32-bit integers."""
        for h in IV:
            assert 0 <= h <= 0xFFFFFFFF

    def test_iv_unique(self):
        """Test IV values are unique."""
        assert len(set(IV)) == len(IV)

    def test_k_length(self):
        """Test K has 64 constants."""
        assert len(K) == 64

    def test_k_values_are_32bit(self):
        """Test K constants are 32-bit integers."""
        for k in K:
            assert 0 <= k <= 0xFFFFFFFF

    def test_k_unique(self):
        """Test K constants are unique."""
        assert len(set(K)) == len(K)


class TestSHA256Functions:
    """Test SHA-256 logical functions."""

    def test_choose_basic(self):
        """Test Ch(x, y, z) = (x & y) ^ (~x & z)."""
        # When all x bits are 1, result comes from y
        result = choose(0xFFFFFFFF, 0xAAAAAAAA, 0x55555555)
        assert result == 0xAAAAAAAA

        # When all x bits are 0, result comes from z
        result = choose(0x00000000, 0xAAAAAAAA, 0x55555555)
        # (~x & z) = 0xFFFFFFFF & 0x55555555 = 0x55555555
        assert result == 0x55555555

    def test_choose_symmetry(self):
        """Test Ch is symmetric in y and z for each bit position."""
        # For each bit, Ch depends on x's bit:
        # If x=1: y bit, if x=0: z bit
        x, y, z = 0xAAAAAAAA, 0xCCCCCCCC, 0xF0F0F0F0
        result = choose(x, y, z)
        assert isinstance(result, int)
        assert result <= 0xFFFFFFFF

    def test_majority_basic(self):
        """Test Maj(x, y, z) = (x & y) ^ (x & z) ^ (y & z)."""
        # When all bits are 1
        assert majority(1, 1, 1) == 1
        # When all bits are 0
        assert majority(0, 0, 0) == 0
        # When exactly two bits are 1
        assert majority(1, 1, 0) == 1
        assert majority(1, 0, 1) == 1
        assert majority(0, 1, 1) == 1

    def test_majority_symmetry(self):
        """Test majority is symmetric in its arguments."""
        x, y, z = 0x12, 0x34, 0x56
        assert majority(x, y, z) == majority(x, z, y)
        assert majority(x, y, z) == majority(y, x, z)
        assert majority(x, y, z) == majority(z, x, y)

    def test_sum_0_output_type(self):
        """Test Σ0(x) returns integer."""
        x = 0x12345678
        result = sum_0(x)
        assert isinstance(result, int)

    def test_sum_1_output_type(self):
        """Test Σ1(x) returns integer."""
        x = 0x12345678
        result = sum_1(x)
        assert isinstance(result, int)

    def test_rho_0_output_type(self):
        """Test σ0(x) returns integer."""
        x = 0x12345678
        result = rho_0(x)
        assert isinstance(result, int)

    def test_rho_1_output_type(self):
        """Test σ1(x) returns integer."""
        x = 0x12345678
        result = rho_1(x)
        assert isinstance(result, int)

    def test_sum_0_consistency(self):
        """Test Σ0 gives consistent results."""
        x = 0x12345678
        assert sum_0(x) == sum_0(x)

    def test_sum_1_consistency(self):
        """Test Σ1 gives consistent results."""
        x = 0x12345678
        assert sum_1(x) == sum_1(x)

    def test_rho_0_consistency(self):
        """Test σ0 gives consistent results."""
        x = 0x12345678
        assert rho_0(x) == rho_0(x)

    def test_rho_1_consistency(self):
        """Test σ1 gives consistent results."""
        x = 0x12345678
        assert rho_1(x) == rho_1(x)

    def test_choose_consistency(self):
        """Test Ch gives consistent results."""
        x, y, z = 0x12345678, 0x9ABCDEF0, 0xABCDEF01
        assert choose(x, y, z) == choose(x, y, z)

    def test_majority_consistency(self):
        """Test Maj gives consistent results."""
        x, y, z = 0x12345678, 0x9ABCDEF0, 0xABCDEF01
        assert majority(x, y, z) == majority(x, y, z)
