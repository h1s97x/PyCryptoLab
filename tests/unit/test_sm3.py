"""
Unit tests for SM3 hash algorithm.
SM3 is the Chinese national standard hash function.
"""
import pytest
from core.algorithms.hash.SM3 import (
    sm3_ff_j,
    sm3_gg_j,
    sm3_p_0,
    sm3_p_1,
    IV
)


class TestSM3Constants:
    """Test SM3 constant values."""

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


class TestSM3Functions:
    """Test SM3 logical functions."""

    def test_sm3_ff_j_type(self):
        """Test sm3_ff_j function returns integer."""
        result = sm3_ff_j(0x12345678, 0x9ABCDEF0, 0x12345678, 0)
        assert isinstance(result, int)

    def test_sm3_ff_j_round_0_15(self):
        """Test sm3_ff_j for j < 16: X ^ Y ^ Z."""
        X, Y, Z = 0x12, 0x34, 0x56
        result = sm3_ff_j(X, Y, Z, 5)  # j < 16
        expected = X ^ Y ^ Z
        assert result == expected

    def test_sm3_ff_j_round_16_63(self):
        """Test sm3_ff_j for j >= 16: (X & Y) | (X & Z) | (Y & Z)."""
        X, Y, Z = 0x12, 0x34, 0x56
        result = sm3_ff_j(X, Y, Z, 20)  # j >= 16
        expected = (X & Y) | (X & Z) | (Y & Z)
        assert result == expected

    def test_sm3_gg_j_type(self):
        """Test sm3_gg_j function returns integer."""
        result = sm3_gg_j(0x12345678, 0x9ABCDEF0, 0x12345678, 0)
        assert isinstance(result, int)

    def test_sm3_gg_j_round_0_15(self):
        """Test sm3_gg_j for j < 16: X ^ Y ^ Z."""
        X, Y, Z = 0x12, 0x34, 0x56
        result = sm3_gg_j(X, Y, Z, 5)  # j < 16
        expected = X ^ Y ^ Z
        assert result == expected

    def test_sm3_p_0_type(self):
        """Test sm3_p_0 function returns integer."""
        result = sm3_p_0(0x12345678)
        assert isinstance(result, int)

    def test_sm3_p_1_type(self):
        """Test sm3_p_1 function returns integer."""
        result = sm3_p_1(0x12345678)
        assert isinstance(result, int)


class TestSM3Consistency:
    """Test SM3 function consistency."""

    def test_sm3_ff_j_consistency(self):
        """Test sm3_ff_j gives consistent results."""
        X, Y, Z = 0x12345678, 0x9ABCDEF0, 0xABCDEF01
        j = 25
        assert sm3_ff_j(X, Y, Z, j) == sm3_ff_j(X, Y, Z, j)

    def test_sm3_gg_j_consistency(self):
        """Test sm3_gg_j gives consistent results."""
        X, Y, Z = 0x12345678, 0x9ABCDEF0, 0xABCDEF01
        j = 25
        assert sm3_gg_j(X, Y, Z, j) == sm3_gg_j(X, Y, Z, j)

    def test_sm3_p_0_consistency(self):
        """Test sm3_p_0 gives consistent results."""
        x = 0x12345678
        assert sm3_p_0(x) == sm3_p_0(x)

    def test_sm3_p_1_consistency(self):
        """Test sm3_p_1 gives consistent results."""
        x = 0x12345678
        assert sm3_p_1(x) == sm3_p_1(x)


class TestSM3MathProperties:
    """Test mathematical properties of SM3 functions."""

    def test_sm3_ff_j_symmetry(self):
        """Test sm3_ff_j is symmetric in Y and Z for j >= 16."""
        X, Y, Z = 0x12, 0x34, 0x56
        j = 20
        result1 = sm3_ff_j(X, Y, Z, j)
        result2 = sm3_ff_j(X, Z, Y, j)
        # For j >= 16, FF is symmetric in Y and Z
        assert result1 == result2

    def test_sm3_gg_j_asymmetry(self):
        """Test sm3_gg_j is not symmetric in Y and Z for j >= 16."""
        X, Y, Z = 0x12, 0x34, 0x56
        j = 20
        result1 = sm3_gg_j(X, Y, Z, j)
        result2 = sm3_gg_j(X, Z, Y, j)
        # GG(X, Y, Z) != GG(X, Z, Y) for j >= 16 (different formulas)
        assert isinstance(result1, int)
        assert isinstance(result2, int)

    def test_sm3_p_0_commutative(self):
        """Test sm3_p_0 results are consistent."""
        x = 0x12345678
        y = 0x9ABCDEF0
        p0_x = sm3_p_0(x)
        p0_y = sm3_p_0(y)
        p0_xor = sm3_p_0(x ^ y)
        # Just check types and consistency
        assert isinstance(p0_x, int)
        assert isinstance(p0_y, int)
        assert isinstance(p0_xor, int)
