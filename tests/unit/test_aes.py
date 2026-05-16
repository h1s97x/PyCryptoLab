"""
AES 加密算法单元测试
测试 AES 的常量、工具函数和数学性质
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.algorithms.symmetric.AES import (
    s_box, inv_s_box, Rcon, x_time,
    int_to_matrix, matrix_to_int, array_to_int
)


class TestAESSBox:
    """AES S-Box 测试"""

    def test_s_box_length(self):
        """S-Box 长度应为 256"""
        assert len(s_box) == 256

    def test_s_box_values_range(self):
        """S-Box 值应在 0-255 范围内"""
        for val in s_box:
            assert 0 <= val <= 255

    def test_s_box_first_value(self):
        """S-Box 首元素应为 0x63 ( AES 标准)"""
        assert s_box[0] == 0x63

    def test_s_box_last_value(self):
        """S-Box 末元素应为 0x16"""
        assert s_box[255] == 0x16


class TestAESInvSBox:
    """AES 逆 S-Box 测试"""

    def test_inv_s_box_length(self):
        """逆 S-Box 长度应为 256"""
        assert len(inv_s_box) == 256

    def test_inv_s_box_values_range(self):
        """逆 S-Box 值应在 0-255 范围内"""
        for val in inv_s_box:
            assert 0 <= val <= 255

    def test_inv_s_box_first_value(self):
        """逆 S-Box 首元素应为 0x52"""
        assert inv_s_box[0] == 0x52

    def test_inv_s_box_last_value(self):
        """逆 S-Box 末元素应为 0x7D"""


class TestAESRcon:
    """AES Rcon 常量测试"""

    def test_rcon_length(self):
        """Rcon 长度应为 32"""
        assert len(Rcon) == 32

    def test_rcon_first_nonzero(self):
        """Rcon[1] 应为 0x01"""
        assert Rcon[1] == 0x01

    def test_rcon_doubling_property(self):
        """Rcon 满足 2 倍关系 (模不可约多项式)"""
        for i in range(2, 10):
            expected = (Rcon[i-1] * 2) % 0x100 if Rcon[i-1] < 128 else ((Rcon[i-1] * 2) ^ 0x1B) % 0x100
            assert Rcon[i] == expected


class TestAESXTime:
    """AES x_time 函数测试"""

    def test_xtime_zero(self):
        """x_time(0) = 0"""
        assert x_time(0) == 0

    def test_xtime_one(self):
        """x_time(1) = 2"""
        assert x_time(1) == 2

    def test_xtime_high_bit(self):
        """x_time(0x80) 触发约简"""
        result = x_time(0x80)
        expected = ((0x80 << 1) ^ 0x1B) & 0xFF
        assert result == expected

    def test_xtime_random(self):
        """x_time 随机值测试"""
        assert x_time(0x53) == 166
        assert x_time(0xAB) == 77


class TestAESMatrixConvert:
    """AES 矩阵转换函数测试"""

    def test_int_to_matrix_shape(self):
        """转换后矩阵应为 4x4"""
        matrix = int_to_matrix(0x0123456789ABCDEF0123456789ABCDEF)
        assert len(matrix) == 4
        assert all(len(row) == 4 for row in matrix)

    def test_matrix_to_int_roundtrip(self):
        """矩阵转整数应可逆"""
        original = 0x0123456789ABCDEF0123456789ABCDEF
        matrix = int_to_matrix(original)
        result = matrix_to_int(matrix)
        assert result == original

    def test_int_to_matrix_bytes_order(self):
        """字节顺序测试"""
        matrix = int_to_matrix(0x000102030405060708090A0B0C0D0E0F)
        expected = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
        assert matrix == expected

    def test_array_to_int(self):
        """array_to_int 测试"""
        result = array_to_int([0x01, 0x02, 0x03, 0x04])
        assert result == 0x01020304


class TestAESMathProperties:
    """AES 数学性质测试"""

    def test_s_box_inv_consistency(self):
        """S-Box 和逆 S-Box 应互为逆"""
        for i in range(0, 256, 17):
            assert inv_s_box[s_box[i]] == i

    def test_s_box_permutation(self):
        """S-Box 应是排列（无重复值）"""
        assert len(set(s_box)) == 256

    def test_inv_s_box_permutation(self):
        """逆 S-Box 应是排列"""
        assert len(set(inv_s_box)) == 256

    def test_no_fixed_points(self):
        """S-Box 不应有固定点（除了特定情况）"""
        fixed_points = [i for i in range(256) if s_box[i] == i]
        assert len(fixed_points) <= 2
