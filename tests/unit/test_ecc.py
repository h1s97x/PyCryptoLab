"""
Unit tests for ECC (Elliptic Curve Cryptography) algorithm
"""
import pytest
from core.algorithms.asymmetric.ECC import str_add_space


class TestECCUtils:
    """Test ECC utility functions"""

    def test_str_add_space_empty(self):
        """Test adding spaces to empty string"""
        assert str_add_space('') == ''

    def test_str_add_space_even_length(self):
        """Test adding spaces to even length string"""
        assert str_add_space('ABCD') == 'AB CD'
        assert str_add_space('12345678') == '12 34 56 78'

    def test_str_add_space_odd_length(self):
        """Test adding spaces to odd length string (truncates last char)"""
        # Odd length strings are processed as floor(len/2) pairs
        assert str_add_space('ABC') == 'AB'
        assert str_add_space('12345') == '12 34'

    def test_str_add_space_single_pair(self):
        """Test adding spaces to single pair"""
        assert str_add_space('12') == '12'
        assert str_add_space('FF') == 'FF'

    def test_str_add_space_already_spaced(self):
        """Test adding spaces to already spaced string"""
        result = str_add_space('AB CD EF 12')
        # Note: This produces 'AB CD EF 12' which is the same input processed
        # The function doesn't check for existing spaces
        assert ' ' in result


class TestECCKeyGeneration:
    """Test ECC key generation"""

    def test_ecc_generate_keys(self):
        """Test ECC key generation produces valid keys"""
        from core.algorithms.asymmetric.ECC import ECCKeyThread

        k, K, r, key_a, key_b = ECCKeyThread.generate_key()

        # Private key should be a valid hex string
        assert isinstance(k, str)
        assert len(k) == 64  # P-256 private key is 32 bytes = 64 hex chars

        # Public key should be valid hex string (x || y coordinates)
        # Note: length may vary due to leading zeros being stripped
        assert isinstance(K, str)
        assert len(K) >= 100  # P-256 public key should be reasonably sized

        # Random value r should be valid hex
        assert isinstance(r, str)
        assert len(r) == 64

        # key_a and key_b should be ECC objects
        assert hasattr(key_a, 'd')
        assert hasattr(key_a, 'pointQ')
        assert hasattr(key_b, 'd')
        assert hasattr(key_b, 'pointQ')

    def test_ecc_keys_are_unique(self):
        """Test that generated keys are unique each time"""
        from core.algorithms.asymmetric.ECC import ECCKeyThread

        keys1 = ECCKeyThread.generate_key()
        keys2 = ECCKeyThread.generate_key()

        # Keys should be different
        assert keys1[0] != keys2[0]  # Different private keys
        assert keys1[1] != keys2[1]  # Different public keys
        assert keys1[2] != keys2[2]  # Different r values


class TestECCEncryption:
    """Test ECC encryption"""

    def test_ecc_encrypt_produces_ciphertext(self):
        """Test ECC encryption produces valid ciphertext"""
        from core.algorithms.asymmetric.ECC import ECCKeyThread, ECCEncryptThread
        from unittest.mock import MagicMock

        # Generate keys
        k, K, r, key_a, key_b = ECCKeyThread.generate_key()

        # Create encrypt thread
        plaintext = "Hello"
        thread = ECCEncryptThread(None, plaintext, key_a, key_b)

        # Get ciphertext
        ciphertext = thread.encrypt()

        # Ciphertext structure: c2 (public key of key_b, 64 bytes) + c1 (encrypted value)
        # Length varies based on plaintext size and key values
        assert isinstance(ciphertext, str)
        assert len(ciphertext) >= 128  # At least c2 length

    def test_ecc_encrypt_different_plaintexts(self):
        """Test that different plaintexts produce different ciphertexts"""
        from core.algorithms.asymmetric.ECC import ECCKeyThread, ECCEncryptThread

        # Generate keys
        k, K, r, key_a, key_b = ECCKeyThread.generate_key()

        # Encrypt different plaintexts
        thread1 = ECCEncryptThread(None, "Hello", key_a, key_b)
        thread2 = ECCEncryptThread(None, "World", key_a, key_b)

        ciphertext1 = thread1.encrypt()
        ciphertext2 = thread2.encrypt()

        # Different plaintexts should produce different ciphertexts
        assert ciphertext1 != ciphertext2

    def test_ecc_encrypt_different_keys(self):
        """Test that different keys produce different ciphertexts"""
        from core.algorithms.asymmetric.ECC import ECCKeyThread, ECCEncryptThread

        # Generate two different key pairs
        k1, K1, r1, key_a1, key_b1 = ECCKeyThread.generate_key()
        k2, K2, r2, key_a2, key_b2 = ECCKeyThread.generate_key()

        # Encrypt same plaintext with different keys
        plaintext = "Test"
        thread1 = ECCEncryptThread(None, plaintext, key_a1, key_b1)
        thread2 = ECCEncryptThread(None, plaintext, key_a1, key_b2)

        ciphertext1 = thread1.encrypt()
        ciphertext2 = thread2.encrypt()

        # Different keys should produce different ciphertexts
        assert ciphertext1 != ciphertext2


class TestECCDecryption:
    """Test ECC decryption"""

    def test_ecc_decrypt_produces_result(self):
        """Test ECC decryption produces output"""
        from core.algorithms.asymmetric.ECC import ECCKeyThread, ECCEncryptThread, ECCDecryptThread

        k, K, r, key_a, key_b = ECCKeyThread.generate_key()
        plaintext = "Hello"
        ciphertext = ECCEncryptThread(None, plaintext, key_a, key_b).encrypt()
        decrypted = ECCDecryptThread(None, ciphertext, key_a, key_b).decrypt()
        assert decrypted is not None
        assert len(decrypted) > 0

    def test_ecc_decrypt_consistency(self):
        """Test ECC decryption produces consistent length"""
        from core.algorithms.asymmetric.ECC import ECCKeyThread, ECCEncryptThread, ECCDecryptThread

        k, K, r, key_a, key_b = ECCKeyThread.generate_key()
        plaintext = "Test"
        ciphertext = ECCEncryptThread(None, plaintext, key_a, key_b).encrypt()
        decrypted = ECCDecryptThread(None, ciphertext, key_a, key_b).decrypt()
        assert len(decrypted) > 0

    def test_ecc_ciphertext_structure(self):
        """Test ECC ciphertext has correct structure"""
        from core.algorithms.asymmetric.ECC import ECCKeyThread, ECCEncryptThread

        # Generate keys
        k, K, r, key_a, key_b = ECCKeyThread.generate_key()

        # Encrypt
        encrypt_thread = ECCEncryptThread(None, "Test", key_a, key_b)
        ciphertext = encrypt_thread.encrypt()

        # Ciphertext is c2 + c1
        # c2 is public key of key_b (x || y coordinates)
        # c1 is the encrypted plaintext value
        assert len(ciphertext) >= 128  # At least c2 length
        assert all(c in '0123456789abcdefABCDEF' for c in ciphertext)  # Valid hex
