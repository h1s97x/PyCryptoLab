import pytest
from core.algorithms.symmetric.SM4 import SM4_BOXES_TABLE, SM4_FK, SM4_CK, SM4_ENCRYPT, SM4_DECRYPT


class TestSM4Constants:
    """Test SM4 constant values"""

    def test_boxes_table_length(self):
        """SM4 S-box table should have 256 elements"""
        assert len(SM4_BOXES_TABLE) == 256

    def test_boxes_table_values_range(self):
        """SM4 S-box values should be 0-255"""
        for val in SM4_BOXES_TABLE:
            assert 0 <= val <= 255

    def test_boxes_contains_all_values(self):
        """SM4 S-box should be a permutation of 0-255"""
        assert sorted(SM4_BOXES_TABLE) == list(range(256))

    def test_boxes_first_value(self):
        """SM4 S-box first element should be 0xd6"""
        assert SM4_BOXES_TABLE[0] == 0xd6

    def test_boxes_last_value(self):
        """SM4 S-box last element should be 0x48"""
        assert SM4_BOXES_TABLE[-1] == 0x48


class TestSM4FK:
    """Test SM4 FK (key parameter)"""

    def test_fk_length(self):
        """SM4 FK should have 4 elements"""
        assert len(SM4_FK) == 4

    def test_fk_values_range(self):
        """SM4 FK values should be 32-bit integers"""
        for val in SM4_FK:
            assert 0 <= val <= 0xFFFFFFFF


class TestSM4CK:
    """Test SM4 CK (constant key)"""

    def test_ck_length(self):
        """SM4 CK should have 32 elements (one per round)"""
        assert len(SM4_CK) == 32

    def test_ck_values_range(self):
        """SM4 CK values should be 32-bit integers"""
        for val in SM4_CK:
            assert 0 <= val <= 0xFFFFFFFF

    def test_ck_unique(self):
        """SM4 CK values should all be unique"""
        assert len(SM4_CK) == len(set(SM4_CK))


class TestSM4Modes:
    """Test SM4 mode constants"""

    def test_encrypt_mode(self):
        """SM4_ENCRYPT should be 0"""
        assert SM4_ENCRYPT == 0

    def test_decrypt_mode(self):
        """SM4_DECRYPT should be 1"""
        assert SM4_DECRYPT == 1
