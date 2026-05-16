# -*- coding: UTF-8 -*-
"""
ZUC 祖冲之流密码算法单元测试
"""

import pytest
from core.algorithms.symmetric.ZUC import (
    ZUC, Mod, MulByPow2, l1, l2, rotl_uint32
)


class TestZUCTools:
    """ZUC 工具函数测试"""

    def test_mod_normal(self):
        """Mod 函数测试 - 正常情况"""
        # Mod(a, b) = (a + b) & 0x7FFFFFFF + (a + b) >> 31
        result = Mod(0x10000000, 0x7FFFFFFF)
        expected = ((0x10000000 + 0x7FFFFFFF) & 0x7FFFFFFF) + ((0x10000000 + 0x7FFFFFFF) >> 31)
        assert result == expected

    def test_mod_overflow(self):
        """Mod 函数测试 - 溢出情况"""
        result = Mod(0x7FFFFFFF, 0x7FFFFFFF)
        expected = ((0x7FFFFFFF + 0x7FFFFFFF) & 0x7FFFFFFF) + ((0x7FFFFFFF + 0x7FFFFFFF) >> 31)
        assert result == expected

    def test_mod_zero(self):
        """Mod 函数测试 - 零值"""
        result = Mod(0, 0x7FFFFFFF)
        expected = ((0 + 0x7FFFFFFF) & 0x7FFFFFFF) + ((0 + 0x7FFFFFFF) >> 31)
        assert result == expected

    def test_mul_by_pow2_normal(self):
        """MulByPow2 函数测试 - 正常情况"""
        result = MulByPow2(0x12345678, 5)
        assert result == ((0x12345678 << 5) | (0x12345678 >> (31 - 5))) & 0x7FFFFFFF

    def test_mul_by_pow2_zero(self):
        """MulByPow2 函数测试 - 零值"""
        assert MulByPow2(0, 10) == 0

    def test_l1_function(self):
        """l1 函数测试 - 非线性变换"""
        x = 0x12345678
        result = l1(x)
        # l1(x) = x ^ ROTL(x,2) ^ ROTL(x,10) ^ ROTL(x,18) ^ ROTL(x,24)
        expected = x ^ rotl_uint32(x, 2) ^ rotl_uint32(x, 10) ^ rotl_uint32(x, 18) ^ rotl_uint32(x, 24)
        assert result == expected

    def test_l2_function(self):
        """l2 函数测试 - 非线性变换"""
        x = 0x12345678
        result = l2(x)
        # l2(x) = x ^ ROTL(x,8) ^ ROTL(x,14) ^ ROTL(x,22) ^ ROTL(x,30)
        expected = x ^ rotl_uint32(x, 8) ^ rotl_uint32(x, 14) ^ rotl_uint32(x, 22) ^ rotl_uint32(x, 30)
        assert result == expected

    def test_rotl_uint32_normal(self):
        """rotl_uint32 函数测试 - 正常循环左移"""
        x = 0x12345678
        shift = 8
        result = rotl_uint32(x, shift)
        expected = ((x << shift) | (x >> (32 - shift))) & 0xFFFFFFFF
        assert result == expected

    def test_rotl_uint32_full(self):
        """rotl_uint32 函数测试 - 32位循环"""
        x = 0x12345678
        result = rotl_uint32(x, 32)
        assert result == x  # 循环32位等于不变

    def test_rotl_uint32_zero(self):
        """rotl_uint32 函数测试 - 零值"""
        assert rotl_uint32(0, 10) == 0


class TestZUCClass:
    """ZUC 类测试"""

    def test_zuc_initialization(self):
        """ZUC 初始化测试"""
        key = bytes.fromhex('00000000000000000000000000000000')
        iv = bytes.fromhex('00000000000000000000000000000000')
        zuc = ZUC(key, iv)
        assert zuc is not None
        assert len(zuc.lfsr) == 16
        assert len(zuc.x) == 4

    def test_zuc_lfsr_state(self):
        """ZUC LFSR 状态测试"""
        key = bytes.fromhex('0123456789ABCDEF0123456789ABCDEF')
        iv = bytes.fromhex('FEDCBA9876543210FEDCBA9876543210')
        zuc = ZUC(key, iv)
        lfsr = zuc.show_lfsr()
        assert len(lfsr) == 16
        # LFSR 初始化后应该不为全零
        assert any(lfsr) is True

    def test_zuc_key_different(self):
        """ZUC 不同密钥产生不同初始状态"""
        key1 = bytes.fromhex('00000000000000000000000000000000')
        key2 = bytes.fromhex('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
        iv = bytes.fromhex('00000000000000000000000000000000')

        zuc1 = ZUC(key1, iv)
        zuc2 = ZUC(key2, iv)

        # 不同密钥应该产生不同的 LFSR 状态
        assert zuc1.show_lfsr() != zuc2.show_lfsr()

    def test_zuc_iv_different(self):
        """ZUC 不同 IV 产生不同初始状态"""
        key = bytes.fromhex('0123456789ABCDEF0123456789ABCDEF')
        iv1 = bytes.fromhex('00000000000000000000000000000000')
        iv2 = bytes.fromhex('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')

        zuc1 = ZUC(key, iv1)
        zuc2 = ZUC(key, iv2)

        # 不同 IV 应该产生不同的 LFSR 状态
        assert zuc1.show_lfsr() != zuc2.show_lfsr()

    def test_zuc_generate_keystream(self):
        """ZUC 密钥流生成测试"""
        key = bytes.fromhex('0123456789ABCDEF0123456789ABCDEF')
        iv = bytes.fromhex('FEDCBA9876543210FEDCBA9876543210')
        zuc = ZUC(key, iv)

        # 生成密钥流
        keystream1 = zuc.zuc_generate_keystream(4)
        keystream2 = zuc.zuc_generate_keystream(4)

        # 密钥流应该不为零
        assert keystream1 != 0
        assert keystream2 != 0

    def test_zuc_encrypt_decrypt(self):
        """ZUC 加解密测试 - 对称性"""
        key = bytes.fromhex('0123456789ABCDEF0123456789ABCDEF')
        iv = bytes.fromhex('FEDCBA9876543210FEDCBA9876543210')

        plaintext = [0x01, 0x23, 0x45, 0x67]

        # 加密
        zuc_enc = ZUC(key, iv)
        ciphertext = zuc_enc.zuc_encrypt(plaintext)

        # 解密（使用相同密钥流）
        zuc_dec = ZUC(key, iv)
        decrypted = zuc_dec.zuc_encrypt(ciphertext)

        assert decrypted == plaintext
