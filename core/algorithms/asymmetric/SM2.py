#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：sm2_encrypt
@IDE    ：PyCharm
@Author ：LiuXin
@Date   ：2020/8/3 23:01
@Desc   ：
=================================================="""
import logging
from PyQt5 import QtCore
from gmssl.sm2 import CryptSM2, default_ecc_table
from gmssl import func
from infrastructure.converters.TypeConvert import *


def str_add_space(out_str: str) -> str:
    """
    Add a space ever 2 char
    """
    add_space_str = ''
    for i in range(int(len(out_str) / 2)):
        add_space_str += out_str[i * 2:i * 2 + 2]
        add_space_str += ' '
    return add_space_str.strip()


def list_chr(chr_list):
    string = ''
    for i in chr_list:
        string += chr(i)
    return string


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


class SM2EncryptKeyThread(QtCore.QThread):
    call_back = QtCore.pyqtSignal(str, str, str)

    def __init__(self, parent):
        super(SM2EncryptKeyThread, self).__init__(parent)

    def run(self):
        private_key, public_key = _generate_keypair()
        k = func.random_hex(32)
        self.call_back.emit(
            str_add_space(private_key.upper()),
            str_add_space(public_key.upper()),
            str_add_space(k.upper())
        )


class SM2EncryptThread(QtCore.QThread):
    call_back = QtCore.pyqtSignal(str)

    def __init__(self, parent, d, P, k, message):
        super(SM2EncryptThread, self).__init__(parent)
        self.sm2_crypt = CryptSM2(
            public_key=P.replace(" ", ""), private_key=d.replace(" ", ""))
        self.k = k.replace(" ", "")
        self.msg = message

    def run(self) -> None:
        self.encrypt_run()

    def encrypt_run(self) -> None:
        ciphertext = self.sm2_crypt.encrypt(self.msg.encode('utf-8').hex(), self.k)
        self.call_back.emit(str_add_space(ciphertext.upper()))


if __name__ == '__main__':
    P = '435B39CCA8F3B508C1488AFC67BE491A0F7BA07E581A0E4849A5CF70628A7E0A75DDBA78F15FEECB4C7895E2C1CDF5FE01DEBB2CDBADF45399CCF77BBA076A42'
    d = '1649AB77A00637BD5E2EFE283FBF353534AA7F7CB89463F208DDBC2920BB0DA0'
    msg = 'encryption standard'
    k = '4C62EEFD6ECFC2B95B92FD6C3D9575148AFA17425546D49018E5388D49DD7B4F'
    sm2_crypt = CryptSM2(public_key=P, private_key=d)
    ciphertext = sm2_crypt.encrypt(msg.encode('utf-8').hex(), k)
    print(f'ciphertext: {ciphertext}')


class SM2DecryptThread(QtCore.QThread):
    call_back = QtCore.pyqtSignal(str)

    def __init__(self, parent, d, P, ciphertext):
        super(SM2DecryptThread, self).__init__(parent)
        self.sm2_crypt = CryptSM2(public_key=P, private_key=d)
        self.ciphertext = ciphertext.replace(" ", "")

    def run(self) -> None:
        self.decrypt_run()

    def decrypt_run(self) -> None:
        try:
            plaintext = self.sm2_crypt.decrypt(self.ciphertext)
            self.call_back.emit(bytes.fromhex(plaintext).decode('utf-8'))
        except Exception as e:
            logging.error(e)


class SM2SignKeyThread(QtCore.QThread):
    call_back = QtCore.pyqtSignal(str, str)

    def __init__(self, parent):
        super(SM2SignKeyThread, self).__init__(parent)

    def run(self):
        private_key, public_key = _generate_keypair()
        self.call_back.emit(
            str_add_space(private_key.upper()),
            str_add_space(public_key.upper())
        )


class SM2SignThread(QtCore.QThread):
    call_back = QtCore.pyqtSignal(str)

    def __init__(self, parent, d, P, message):
        super(SM2SignThread, self).__init__(parent)
        self.sm2_crypt = CryptSM2(public_key=P.replace(" ", ""), private_key=d.replace(" ", ""))
        self.msg = message

    def run(self) -> None:
        self.sign_run()

    def sign_run(self) -> None:
        try:
            signature = self.sm2_crypt.sign_with_sm3(self.msg.encode('utf-8'))
            self.call_back.emit(str_add_space(signature.upper()))
        except Exception as e:
            logging.error(e)
            self.call_back.emit(f"Error: {str(e)}")


class SM2VerifyThread(QtCore.QThread):
    call_back = QtCore.pyqtSignal(bool, str)

    def __init__(self, parent, P, message, signature):
        super(SM2VerifyThread, self).__init__(parent)
        self.sm2_crypt = CryptSM2(public_key=P.replace(" ", ""), private_key="")
        self.msg = message
        self.signature = signature.replace(" ", "")

    def run(self) -> None:
        self.verify_run()

    def verify_run(self) -> None:
        try:
            result = self.sm2_crypt.verify_with_sm3(self.signature, self.msg.encode('utf-8'))
            self.call_back.emit(result, "Verification successful" if result else "Verification failed")
        except Exception as e:
            logging.error(e)
            self.call_back.emit(False, f"Error: {str(e)}")
