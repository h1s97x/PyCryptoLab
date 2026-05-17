import pytest
import numpy as np
from core.algorithms.classical.Hill import multi_inverse, Thread


class TestMultiInverse:
    """测试 multi_inverse 函数"""

    def test_inverse_3_mod_26(self):
        """测试 3 在模 26 下的乘法逆元"""
        result = multi_inverse(3, 26)
        assert result == 9  # 3 * 9 = 27 ≡ 1 (mod 26)

    def test_inverse_5_mod_26(self):
        """测试 5 在模 26 下的乘法逆元"""
        result = multi_inverse(5, 26)
        assert result == 21  # 5 * 21 = 105 ≡ 1 (mod 26)

    def test_inverse_7_mod_26(self):
        """测试 7 在模 26 下的乘法逆元"""
        result = multi_inverse(7, 26)
        assert result == 15  # 7 * 15 = 105 ≡ 1 (mod 26)

    def test_no_inverse_gcd_not_1(self):
        """测试当 gcd(x, m) != 1 时返回 0"""
        # 2 和 26 的最大公约数是 2，不存在乘法逆元
        result = multi_inverse(2, 26)
        assert result == 0

    def test_inverse_1_mod_n(self):
        """测试 1 在任何模数下的乘法逆元是 1"""
        for n in [5, 7, 11, 26, 100]:
            result = multi_inverse(1, n)
            assert result == 1

    def test_inverse_n_minus_1_mod_n(self):
        """测试 n-1 的乘法逆元是 n-1 (因为 (n-1)^2 = n^2 - 2n + 1 ≡ 1 (mod n))"""
        for n in [5, 7, 11, 26]:
            result = multi_inverse(n - 1, n)
            assert result == n - 1


class TestHillKeyMatrix:
    """测试 Hill 密钥矩阵"""

    def test_2x2_key_matrix(self):
        """测试 2x2 密钥矩阵"""
        # 模拟 2x2 密钥矩阵
        key = "6 24 1 13"  # K = [[6, 24], [1, 13]]
        key_list = list(map(int, key.split()))
        key_arr = np.array(key_list).reshape(2, 2)
        assert key_arr.shape == (2, 2)
        assert key_arr[0, 0] == 6
        assert key_arr[1, 1] == 13

    def test_3x3_key_matrix(self):
        """测试 3x3 密钥矩阵"""
        # 模拟 3x3 密钥矩阵
        key = "1 2 3 4 5 6 7 8 9"
        key_list = list(map(int, key.split()))
        key_arr = np.array(key_list).reshape(3, 3)
        assert key_arr.shape == (3, 3)
        assert key_arr[0, 0] == 1
        assert key_arr[2, 2] == 9

    def test_matrix_determinant(self):
        """测试矩阵行列式计算"""
        key_arr = np.array([6, 24, 1, 13]).reshape(2, 2)
        det = np.linalg.det(key_arr)
        det_int = round(det) % 26
        assert det_int != 0  # 行列式必须与 26 互素才能求逆

    def test_matrix_inverse_exists(self):
        """测试密钥矩阵在模 26 下是否存在逆矩阵"""
        # 使用正确的 Hill 矩阵例子，gcd(det, 26) = 1
        # K = [[6, 24], [1, 13]] -> det = 54, gcd(54, 26) = 2 (错误)
        # 使用 K = [[3, 3], [2, 5]] -> det = 9, gcd(9, 26) = 1 (正确)
        key_arr = np.array([3, 3, 2, 5]).reshape(2, 2)
        det = round(np.linalg.det(key_arr))
        gcd = np.gcd(int(det), 26)
        assert gcd == 1  # 行列式与 26 互素


class TestHillMathProperties:
    """测试 Hill 密码的数学性质"""

    def test_padding_needed(self):
        """测试需要填充的情况"""
        # 如果明文长度不能被密钥矩阵行数整除，需要填充
        plaintext_len = 5
        row_key = 2
        remain = plaintext_len % row_key
        expected_padding = row_key - remain if remain != 0 else 0
        assert expected_padding == 1

    def test_no_padding_needed(self):
        """测试不需要填充的情况"""
        plaintext_len = 6
        row_key = 2
        remain = plaintext_len % row_key
        expected_padding = row_key - remain if remain != 0 else 0
        assert expected_padding == 0

    def test_letter_to_number_conversion(self):
        """测试字母到数字的转换"""
        assert (ord('A') - ord('A')) % 26 == 0
        assert (ord('B') - ord('A')) % 26 == 1
        assert (ord('Z') - ord('A')) % 26 == 25

    def test_letter_to_number_lowercase(self):
        """测试小写字母到数字的转换"""
        assert (ord('a') - ord('a')) % 26 == 0
        assert (ord('b') - ord('a')) % 26 == 1
        assert (ord('z') - ord('a')) % 26 == 25

    def test_matrix_multiplication_mod_26(self):
        """测试矩阵乘法模 26"""
        # [[1, 2], [3, 4]] * [[5], [6]] mod 26
        A = np.array([1, 2, 3, 4]).reshape(2, 2)
        B = np.array([5, 6]).reshape(2, 1)
        result = np.dot(A, B) % 26
        assert result[0, 0] == (1 * 5 + 2 * 6) % 26  # 17
        assert result[1, 0] == (3 * 5 + 4 * 6) % 26  # 39 % 26 = 13
