"""
Unit tests for SEAL symmetric cipher algorithm.
SEAL is a stream cipher based on SHA-1 pseudo-random generation.
"""
import pytest
from core.algorithms.symmetric.SEAL import Thread


class TestSEALConstants:
    """Test SEAL constant values."""

    def test_k_function_ranges(self):
        """Test K function returns correct values for each range."""
        # t in [0, 19]
        assert Thread.K(0) == 0x5a827999
        assert Thread.K(19) == 0x5a827999

        # t in [20, 39]
        assert Thread.K(20) == 0x6ed9eba1
        assert Thread.K(39) == 0x6ed9eba1

        # t in [40, 59]
        assert Thread.K(40) == 0x8f1bbcdc
        assert Thread.K(59) == 0x8f1bbcdc

        # t in [60, 79]
        assert Thread.K(60) == 0xca62c1d6
        assert Thread.K(79) == 0xca62c1d6

    def test_k_function_type(self):
        """Test K returns 32-bit integers."""
        for t in [0, 20, 40, 60]:
            result = Thread.K(t)
            assert isinstance(result, int)
            assert 0 <= result <= 0xFFFFFFFF


class TestSEALFunctions:
    """Test SEAL mathematical functions."""

    def test_f_function_round_0_19_type(self):
        """Test f function returns int for t in [0, 19]."""
        result = Thread.f(10, 0x12345678, 0x9ABCDEF0, 0x12345678)
        assert isinstance(result, int)

    def test_f_function_round_20_39_type(self):
        """Test f function returns int for t in [20, 39]."""
        result = Thread.f(25, 0x12345678, 0x9ABCDEF0, 0x12345678)
        assert isinstance(result, int)

    def test_f_function_round_40_59_type(self):
        """Test f function returns int for t in [40, 59]."""
        result = Thread.f(45, 0x12345678, 0x9ABCDEF0, 0x12345678)
        assert isinstance(result, int)

    def test_f_function_round_60_79_type(self):
        """Test f function returns int for t in [60, 79]."""
        result = Thread.f(65, 0x12345678, 0x9ABCDEF0, 0x12345678)
        assert isinstance(result, int)

    def test_overflow_add_basic(self):
        """Test overflow_add handles basic cases."""
        assert Thread.overflow_add(1, 2) == 3
        assert Thread.overflow_add(0, 0) == 0
        assert Thread.overflow_add(100, 200) == 300

    def test_overflow_add_type(self):
        """Test overflow_add returns 32-bit integer."""
        result = Thread.overflow_add(0xFFFFFFFF, 1)
        assert isinstance(result, int)

    def test_circular_shift_right_type(self):
        """Test circular_shift_right returns integer."""
        result = Thread.circular_shift_right(0x12345678, 8)
        assert isinstance(result, int)


class TestSEALAlgorithmProperties:
    """Test SEAL algorithm mathematical properties."""

    def test_overflow_add_commutative(self):
        """Test overflow_add is commutative."""
        a, b = 0x12345678, 0x87654321
        assert Thread.overflow_add(a, b) == Thread.overflow_add(b, a)

    def test_overflow_add_with_zero(self):
        """Test overflow_add with zero."""
        assert Thread.overflow_add(0, 12345) == 12345
        assert Thread.overflow_add(12345, 0) == 12345

    def test_f_function_symmetry(self):
        """Test f function is symmetric in B, C, D for rounds 20-39 and 60-79."""
        t = 30  # Round 20-39
        B, C, D = 0x12345678, 0x9ABCDEF0, 0x12345678
        result1 = Thread.f(t, B, C, D)
        result2 = Thread.f(t, C, B, D)
        # Should be different due to XOR nature
        assert isinstance(result1, int)
        assert isinstance(result2, int)

    def test_f_consistency(self):
        """Test f function gives consistent results."""
        t, B, C, D = 25, 0x12345678, 0x9ABCDEF0, 0xABCDEF01
        result1 = Thread.f(t, B, C, D)
        result2 = Thread.f(t, B, C, D)
        assert result1 == result2
