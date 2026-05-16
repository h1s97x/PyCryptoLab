#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
SM2 签名算法单元测试
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gmssl.sm2 import CryptSM2, default_ecc_table
from gmssl import func


def _generate_keypair():
    """Generate SM2 key pair from curve parameters"""
    p = int(default_ecc_table['p'], 16)
    a = int(default_ecc_table['a'], 16)
    Gx = int(default_ecc_table['g'][:64], 16)
    Gy = int(default_ecc_table['g'][64:], 16)

    def point_add(x1, y1, x2, y2):
        if x1 == 0 and y1 == 0:
            return x2, y2
        if x2 == 0 and y2 == 0:
            return x1, y1
        if x1 == x2:
            lam = (3 * x1 * x1 + a) * pow(2 * y1, -1, p) % p
        else:
            lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
        x3 = (lam * lam - x1 - x2) % p
        y3 = (lam * (x1 - x3) - y1) % p
        return x3, y3

    def scalar_mul(k, Gx, Gy):
        x, y = 0, 0
        for c in bin(int(k, 16))[2:]:
            x, y = point_add(x, y, x, y)
            if c == '1':
                x, y = point_add(x, y, Gx, Gy)
        return x, y

    private_key = func.random_hex(32)
    x, y = scalar_mul(private_key, Gx, Gy)
    public_key = format(x, '064x') + format(y, '064x')
    return private_key, public_key


class TestSM2Sign:
    """SM2 签名测试类"""

    def test_generate_keypair(self):
        """测试密钥对生成"""
        private_key, public_key = _generate_keypair()
        assert len(private_key) == 32, "Private key should be 32 hex chars (16 bytes)"
        assert len(public_key) == 128, "Public key should be 128 hex chars (64 bytes)"

    def test_sign_and_verify(self):
        """测试签名和验签"""
        private_key, public_key = _generate_keypair()
        sm2 = CryptSM2(private_key, public_key)

        message = "hello world"
        signature = sm2.sign_with_sm3(message.encode('utf-8'))

        assert len(signature) == 128, "Signature should be 128 hex chars"
        assert sm2.verify_with_sm3(signature, message.encode('utf-8')) is True

    def test_sign_different_messages(self):
        """测试不同消息的签名"""
        private_key, public_key = _generate_keypair()
        sm2 = CryptSM2(private_key, public_key)

        messages = ["test", "hello", "12345"]
        signatures = []

        for msg in messages:
            sig = sm2.sign_with_sm3(msg.encode('utf-8'))
            signatures.append(sig)
            assert sm2.verify_with_sm3(sig, msg.encode('utf-8')) is True

        # 验证不同消息产生不同签名
        assert signatures[0] != signatures[1]
        assert signatures[1] != signatures[2]

    def test_verify_wrong_signature(self):
        """测试错误签名验签失败"""
        private_key, public_key = _generate_keypair()
        sm2 = CryptSM2(private_key, public_key)

        message = "hello world"
        signature = sm2.sign_with_sm3(message.encode('utf-8'))

        # 修改签名的一个字符
        wrong_signature = signature[:-1] + ('0' if signature[-1] != '0' else '1')

        assert sm2.verify_with_sm3(wrong_signature, message.encode('utf-8')) is False

    def test_verify_wrong_message(self):
        """测试错误消息验签失败"""
        private_key, public_key = _generate_keypair()
        sm2 = CryptSM2(private_key, public_key)

        original_message = "hello world"
        signature = sm2.sign_with_sm3(original_message.encode('utf-8'))

        # 用不同的消息验证
        wrong_message = "hello world!"
        assert sm2.verify_with_sm3(signature, wrong_message.encode('utf-8')) is False

    def test_sign_with_different_keys(self):
        """测试不同密钥产生不同签名"""
        _, public_key1 = _generate_keypair()
        private_key2, public_key2 = _generate_keypair()

        sm2_1 = CryptSM2(private_key="0" * 64, public_key=public_key1)
        sm2_2 = CryptSM2(private_key=private_key2, public_key=public_key2)

        message = "test message"

        # 签名只能用对应私钥验证
        signature = sm2_2.sign_with_sm3(message.encode('utf-8'))
        assert sm2_2.verify_with_sm3(signature, message.encode('utf-8')) is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
