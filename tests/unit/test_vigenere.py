"""Unit tests for Vigenere cipher algorithm."""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.algorithms.classical.Vigenere import Thread


class TestVigenereEncrypt:
    """Test Vigenere encryption."""

    def test_encrypt_basic(self):
        """Test basic encryption."""
        thread = Thread(None, 'hello', 'key', 0)
        result = thread.encrypt()
        assert result is not None
        assert len(result) == len('hello')

    def test_encrypt_preserves_non_letters(self):
        """Test that non-letter characters are preserved."""
        thread = Thread(None, 'hello world!', 'key', 0)
        result = thread.encrypt()
        assert result[-1] == '!'
        assert ' ' in result

    def test_encrypt_uppercase_input(self):
        """Test encryption with uppercase input."""
        thread = Thread(None, 'HELLO', 'key', 0)
        result = thread.encrypt()
        assert result.isupper() or result.isalpha()

    def test_encrypt_lowercase_input(self):
        """Test encryption with lowercase input."""
        thread = Thread(None, 'hello', 'KEY', 0)
        result = thread.encrypt()
        assert result.islower() or result.isalpha()

    def test_encrypt_empty_input(self):
        """Test encryption with empty input."""
        thread = Thread(None, '', 'key', 0)
        result = thread.encrypt()
        assert result == ''


class TestVigenereDecrypt:
    """Test Vigenere decryption."""

    def test_decrypt_basic(self):
        """Test basic decryption."""
        thread = Thread(None, 'hello', 'key', 1)
        result = thread.decrypt()
        assert result is not None
        assert len(result) == len('hello')

    def test_decrypt_preserves_non_letters(self):
        """Test that non-letter characters are preserved."""
        thread = Thread(None, 'khoor zruog!', 'key', 1)
        result = thread.decrypt()
        assert result[-1] == '!'


class TestVigenereSymmetry:
    """Test Vigenere encryption/decryption symmetry."""

    def test_encrypt_decrypt_roundtrip(self):
        """Test that encrypt then decrypt returns original text."""
        plaintext = 'attackatdawn'
        key = 'LEMON'
        thread = Thread(None, plaintext, key, 0)
        ciphertext = thread.encrypt()
        thread2 = Thread(None, ciphertext, key, 1)
        decrypted = thread2.decrypt()
        assert decrypted == plaintext

    def test_encrypt_decrypt_preserves_spaces(self):
        """Test that encrypt/decrypt preserves spaces."""
        plaintext = 'the quick brown fox'
        key = 'key'
        thread = Thread(None, plaintext, key, 0)
        ciphertext = thread.encrypt()
        thread2 = Thread(None, ciphertext, key, 1)
        decrypted = thread2.decrypt()
        assert decrypted == plaintext

    def test_different_keys_different_results(self):
        """Test that different keys produce different ciphertext."""
        plaintext = 'hello'
        thread1 = Thread(None, plaintext, 'key', 0)
        thread2 = Thread(None, plaintext, 'test', 0)
        assert thread1.encrypt() != thread2.encrypt()


class TestVigenereKeyLength:
    """Test Vigenere with different key lengths."""

    def test_key_shorter_than_plaintext(self):
        """Test when key is shorter than plaintext."""
        thread = Thread(None, 'verylongtext', 'ab', 0)
        result = thread.encrypt()
        assert len(result) == len('verylongtext')

    def test_key_longer_than_plaintext(self):
        """Test when key is longer than plaintext."""
        thread = Thread(None, 'hi', 'verylongkey', 0)
        result = thread.encrypt()
        assert len(result) == len('hi')
