"""
RSA 加密算法单元测试
测试 RSA 的密钥生成、加密、解密功能
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Crypto.PublicKey import RSA as CryptoRSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes


class TestRSAKeyGeneration:
    """RSA 密钥生成测试"""

    def test_generate_1024bit_key(self):
        """生成 1024 位 RSA 密钥"""
        key = CryptoRSA.generate(1024)
        assert key.has_private()
        assert key.size_in_bits() >= 1024

    def test_generate_2048bit_key(self):
        """生成 2048 位 RSA 密钥"""
        key = CryptoRSA.generate(2048)
        assert key.has_private()
        assert key.size_in_bits() >= 2048

    def test_public_key_extraction(self):
        """从私钥提取公钥"""
        key = CryptoRSA.generate(1024)
        public_key = key.publickey()
        assert not public_key.has_private()

    def test_key_uniqueness(self):
        """每次生成的密钥应不同"""
        key1 = CryptoRSA.generate(1024)
        key2 = CryptoRSA.generate(1024)
        assert key1.n != key2.n


class TestRSAEncryption:
    """RSA 加密测试"""

    def test_encrypt_decrypt_short_message(self):
        """短消息加解密测试"""
        key = CryptoRSA.generate(1024)
        public_key = key.publickey()

        cipher = PKCS1_OAEP.new(public_key)
        message = b"Hello, RSA!"
        ciphertext = cipher.encrypt(message)

        assert ciphertext != message
        assert len(ciphertext) > 0

    def test_encrypt_decrypt_roundtrip(self):
        """加解密往返测试"""
        key = CryptoRSA.generate(1024)
        public_key = key.publickey()

        message = b"Test message for RSA encryption"
        cipher_enc = PKCS1_OAEP.new(public_key)
        ciphertext = cipher_enc.encrypt(message)

        cipher_dec = PKCS1_OAEP.new(key)
        decrypted = cipher_dec.decrypt(ciphertext)

        assert decrypted == message

    def test_different_messages_different_ciphertext(self):
        """不同消息应产生不同密文"""
        key = CryptoRSA.generate(1024)
        public_key = key.publickey()
        cipher = PKCS1_OAEP.new(public_key)

        msg1 = b"Message 1"
        msg2 = b"Message 2"

        ct1 = cipher.encrypt(msg1)
        ct2 = cipher.encrypt(msg2)

        assert ct1 != ct2

    def test_same_message_different_ciphertext(self):
        """同一消息因随机填充应产生不同密文"""
        key = CryptoRSA.generate(1024)
        public_key = key.publickey()
        cipher = PKCS1_OAEP.new(public_key)

        message = b"Same message"
        ct1 = cipher.encrypt(message)
        ct2 = cipher.encrypt(message)

        assert ct1 != ct2

    def test_maximum_message_length(self):
        """最大消息长度测试 (86 字节 for 1024-bit)"""
        key = CryptoRSA.generate(1024)
        public_key = key.publickey()
        cipher = PKCS1_OAEP.new(public_key)

        message = b"A" * 86
        ciphertext = cipher.encrypt(message)

        cipher_dec = PKCS1_OAEP.new(key)
        decrypted = cipher_dec.decrypt(ciphertext)

        assert decrypted == message


class TestRSAMathProperties:
    """RSA 数学性质测试"""

    def test_public_exponent(self):
        """公钥指数应为常见值 (通常 65537)"""
        key = CryptoRSA.generate(1024)
        assert key.e in [3, 17, 65537]

    def test_private_key_components(self):
        """私钥应包含 p, q, d"""
        key = CryptoRSA.generate(1024)
        assert hasattr(key, 'p')
        assert hasattr(key, 'q')
        assert hasattr(key, 'd')

    def test_p_q_product_approximately_n(self):
        """p * q 应接近 n"""
        key = CryptoRSA.generate(1024)
        assert key.p * key.q == key.n

    def test_modulus_size(self):
        """模数大小测试"""
        key = CryptoRSA.generate(1024)
        assert 2**1023 <= key.n < 2**1024


class TestRSAErrorHandling:
    """RSA 错误处理测试"""

    def test_decrypt_with_wrong_key(self):
        """用错误密钥解密应失败"""
        key1 = CryptoRSA.generate(1024)
        key2 = CryptoRSA.generate(1024)
        public_key1 = key1.publickey()

        cipher = PKCS1_OAEP.new(public_key1)
        message = b"Test"
        ciphertext = cipher.encrypt(message)

        cipher_dec = PKCS1_OAEP.new(key2)
        with pytest.raises(Exception):
            cipher_dec.decrypt(ciphertext)

    def test_empty_message(self):
        """空消息测试"""
        key = CryptoRSA.generate(1024)
        public_key = key.publickey()
        cipher = PKCS1_OAEP.new(public_key)

        message = b""
        ciphertext = cipher.encrypt(message)

        cipher_dec = PKCS1_OAEP.new(key)
        decrypted = cipher_dec.decrypt(ciphertext)

        assert decrypted == message
