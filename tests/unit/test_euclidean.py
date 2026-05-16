"""测试数学基础算法"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class TestGCD:
    """测试欧几里得算法 (GCD)"""

    def test_gcd_same_number(self):
        """测试两个相同的数"""
        # 使用 Euclidean.Thread.gcd 静态方法
        from core.algorithms.mathematical.Euclidean import Thread
        assert Thread.gcd(5, 5) == 5
        assert Thread.gcd(12, 12) == 12

    def test_gcd_coprime(self):
        """测试互质的两个数"""
        from core.algorithms.mathematical.Euclidean import Thread
        assert Thread.gcd(17, 13) == 1
        assert Thread.gcd(7, 11) == 1
        assert Thread.gcd(8, 15) == 1

    def test_gcd_common_divisor(self):
        """测试有公约数的两个数"""
        from core.algorithms.mathematical.Euclidean import Thread
        assert Thread.gcd(12, 8) == 4
        assert Thread.gcd(100, 25) == 25
        assert Thread.gcd(48, 18) == 6

    def test_gcd_zero(self):
        """测试包含0的情况"""
        from core.algorithms.mathematical.Euclidean import Thread
        assert Thread.gcd(0, 5) == 5
        assert Thread.gcd(5, 0) == 5
        assert Thread.gcd(0, 0) == 0

    def test_gcd_large_numbers(self):
        """测试大数"""
        from core.algorithms.mathematical.Euclidean import Thread
        assert Thread.gcd(123456, 789012) == 12
        assert Thread.gcd(1000000, 24) == 8

    def test_gcd_prime_numbers(self):
        """测试质数"""
        from core.algorithms.mathematical.Euclidean import Thread
        assert Thread.gcd(13, 17) == 1
        assert Thread.gcd(97, 101) == 1
        assert Thread.gcd(17, 23) == 1
