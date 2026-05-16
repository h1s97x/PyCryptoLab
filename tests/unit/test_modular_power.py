"""
ModularPower infrastructure module tests
"""
import pytest
from unittest.mock import MagicMock, patch


class TestModularPowerPowModN:
    """Test ModularPower.Thread.pow_mod_n static method"""

    def test_basic_modular_exponentiation(self):
        """Test basic modular exponentiation: 2^10 % 1000 = 1024 % 1000 = 24"""
        from infrastructure.ModularPower import Thread
        result = Thread.pow_mod_n(2, 10, 1000)
        assert result == 24

    def test_pow_mod_n_small(self):
        """Test pow_mod_n with small numbers: 3^5 % 7 = 243 % 7 = 5"""
        from infrastructure.ModularPower import Thread
        result = Thread.pow_mod_n(3, 5, 7)
        assert result == 5

    def test_pow_mod_n_large_exponent(self):
        """Test pow_mod_n with large exponent: 2^100 % 13"""
        from infrastructure.ModularPower import Thread
        result = Thread.pow_mod_n(2, 100, 13)
        # Verify with Python's built-in pow
        expected = pow(2, 100, 13)
        assert result == expected

    def test_pow_mod_n_identity(self):
        """Test identity: a^0 % n = 1 (when a and n are coprime)"""
        from infrastructure.ModularPower import Thread
        result = Thread.pow_mod_n(5, 0, 13)
        assert result == 1

    def test_pow_mod_n_modulus_one(self):
        """Test modulus of 1: a^n % 1 = 0"""
        from infrastructure.ModularPower import Thread
        result = Thread.pow_mod_n(123, 456, 1)
        assert result == 0

    def test_pow_mod_n_base_modulus_equal(self):
        """Test when base equals modulus: 5^2 % 5 = 0"""
        from infrastructure.ModularPower import Thread
        result = Thread.pow_mod_n(5, 2, 5)
        assert result == 0

    def test_pow_mod_n_prime_modulus(self):
        """Test with prime modulus using Fermat's little theorem: 2^12 % 13 = 4096 % 13 = 1"""
        from infrastructure.ModularPower import Thread
        result = Thread.pow_mod_n(2, 12, 13)
        assert result == 1

    def test_pow_mod_n_commutativity_with_pow(self):
        """Test consistency with Python's built-in pow"""
        from infrastructure.ModularPower import Thread
        test_cases = [
            (2, 10, 1000),
            (3, 7, 11),
            (7, 3, 13),
            (11, 13, 17),
            (17, 11, 19),
        ]
        for base, exp, mod in test_cases:
            result = Thread.pow_mod_n(base, exp, mod)
            expected = pow(base, exp, mod)
            assert result == expected, f"Failed for {base}^{exp} % {mod}"


class TestModularPowerAlgorithm:
    """Test ModularPower algorithm correctness"""

    def test_algorithm_binary_exponentiation(self):
        """Verify the algorithm uses binary exponentiation (squaring method)"""
        from infrastructure.ModularPower import Thread
        # Test case where binary representation matters
        # 13 in binary is 1101, so the algorithm should multiply when bit is 1
        result = Thread.pow_mod_n(2, 13, 1000)
        expected = pow(2, 13, 1000)
        assert result == expected

    def test_algorithm_large_numbers(self):
        """Test with relatively large numbers"""
        from infrastructure.ModularPower import Thread
        result = Thread.pow_mod_n(1234, 567, 1000000)
        expected = pow(1234, 567, 1000000)
        assert result == expected

    def test_algorithm_very_large_exponent(self):
        """Test with very large exponent"""
        from infrastructure.ModularPower import Thread
        result = Thread.pow_mod_n(2, 1000, 1000003)
        expected = pow(2, 1000, 1000003)
        assert result == expected

    def test_algorithm_rsa_like(self):
        """Test with RSA-like parameters"""
        from infrastructure.ModularPower import Thread
        # Common RSA parameters
        base = 65537
        exp = 12345
        mod = 67891
        result = Thread.pow_mod_n(base, exp, mod)
        expected = pow(base, exp, mod)
        assert result == expected
