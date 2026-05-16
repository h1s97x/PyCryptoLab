"""Unit tests for Caesar cipher algorithm."""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.algorithms.classical.Caesar import Thread


class TestCaesarHelper:
    """Test Caesar helper function."""

    def test_judge_letter_lowercase(self):
        """Test judge_letter with lowercase letters."""
        assert Thread.judge_letter('a') is True
        assert Thread.judge_letter('m') is True
        assert Thread.judge_letter('z') is True

    def test_judge_letter_uppercase(self):
        """Test judge_letter with uppercase letters."""
        assert Thread.judge_letter('A') is True
        assert Thread.judge_letter('M') is True
        assert Thread.judge_letter('Z') is True

    def test_judge_letter_non_letter(self):
        """Test judge_letter with non-letter characters."""
        assert Thread.judge_letter('0') is False
        assert Thread.judge_letter(' ') is False
        assert Thread.judge_letter('!') is False
        assert Thread.judge_letter('@') is False


class TestCaesarEncrypt:
    """Test Caesar encryption."""

    def test_encrypt_single_char(self):
        """Test encrypting a single character."""
        thread = Thread(None, 'a', 3, 0)
        assert thread.encrypt('a', 3) == 'd'

    def test_encrypt_wrapping(self):
        """Test encryption with wrapping around alphabet."""
        thread = Thread(None, 'a', 3, 0)
        # z + 3 = c (wrapping)
        assert thread.encrypt('z', 3) == 'c'

    def test_encrypt_uppercase(self):
        """Test encryption with uppercase letters."""
        thread = Thread(None, 'A', 3, 0)
        assert thread.encrypt('A', 3) == 'D'

    def test_encrypt_preserves_non_letters(self):
        """Test that non-letter characters are preserved."""
        thread = Thread(None, 'hello world!', 3, 0)
        assert thread.encrypt('hello world!', 3) == 'khoor zruog!'

    def test_encrypt_key_zero(self):
        """Test encryption with key 0 (no change)."""
        thread = Thread(None, 'test', 0, 0)
        assert thread.encrypt('test', 0) == 'test'


class TestCaesarDecrypt:
    """Test Caesar decryption."""

    def test_decrypt_single_char(self):
        """Test decrypting a single character."""
        thread = Thread(None, 'd', 3, 1)
        assert thread.decrypt('d', 3) == 'a'

    def test_decrypt_wrapping(self):
        """Test decryption with wrapping around alphabet."""
        thread = Thread(None, 'c', 3, 1)
        # c - 3 = z
        assert thread.decrypt('c', 3) == 'z'

    def test_decrypt_uppercase(self):
        """Test decryption with uppercase letters."""
        thread = Thread(None, 'D', 3, 1)
        assert thread.decrypt('D', 3) == 'A'

    def test_decrypt_preserves_non_letters(self):
        """Test that non-letter characters are preserved."""
        thread = Thread(None, 'khoor zruog!', 3, 1)
        assert thread.decrypt('khoor zruog!', 3) == 'hello world!'


class TestCaesarSymmetry:
    """Test Caesar encryption/decryption symmetry."""

    def test_encrypt_decrypt_roundtrip(self):
        """Test that encrypt then decrypt returns original text."""
        thread = Thread(None, 'hello', 5, 0)
        plaintext = 'attackatdawn'
        ciphertext = thread.encrypt(plaintext, 5)
        decrypted = thread.decrypt(ciphertext, 5)
        assert decrypted == plaintext

    def test_different_keys_different_results(self):
        """Test that different keys produce different ciphertext."""
        thread = Thread(None, 'test', 3, 0)
        ciphertext1 = thread.encrypt('test', 3)
        ciphertext2 = thread.encrypt('test', 5)
        assert ciphertext1 != ciphertext2

    def test_caesar_12(self):
        """Test Caesar with key 12 (ROT12)."""
        thread = Thread(None, 'hello', 12, 0)
        assert thread.encrypt('hello', 12) == 'tqxxa'
        assert thread.decrypt('tqxxa', 12) == 'hello'
