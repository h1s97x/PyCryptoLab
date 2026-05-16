#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from qfluentwidgets import ScrollArea, PushButton, LineEdit, TextEdit, FluentIcon, InfoBar
from qfluentwidgets import StrongBodyLabel, BodyLabel

from core.algorithms.asymmetric.ECC import (
    ECCKeyThread, ECCEncryptThread, ECCDecryptThread
)


class ECCWidget(ScrollArea):
    """ECC 椭圆曲线加密算法 Widget"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.key_a = None
        self.key_b = None
        self.setup_ui()

    def setup_ui(self):
        self.scroll_widget = QtWidgets.QWidget()
        self.setWidget(self.scroll_widget)
        self.setWidgetResizable(True)

        layout = QtWidgets.QVBoxLayout(self.scroll_widget)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(20)

        # Title
        title = StrongBodyLabel("ECC 椭圆曲线密码学")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        # Description
        desc = BodyLabel(
            "椭圆曲线密码学 (Elliptic Curve Cryptography) 基于椭圆曲线数学，"
            "使用较短的密钥即可达到与传统 RSA 相当的安全性。本工具使用 P-256 曲线。"
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Key Generation Section
        key_group = self.create_group("密钥生成")
        key_layout = QtWidgets.QVBoxLayout()

        self.gen_key_btn = PushButton("生成密钥对", FluentIcon.UPDATE)
        self.gen_key_btn.clicked.connect(self.generate_keys)
        key_layout.addWidget(self.gen_key_btn)

        self.key_result = TextEdit()
        self.key_result.setPlaceholderText("密钥生成结果...")
        self.key_result.setReadOnly(True)
        self.key_result.setMaximumHeight(100)
        key_layout.addWidget(self.key_result)

        key_group.layout().addLayout(key_layout)
        layout.addWidget(key_group)

        # Encryption Section
        encrypt_group = self.create_group("加密")
        encrypt_layout = QtWidgets.QGridLayout()

        encrypt_layout.addWidget(BodyLabel("公钥:"), 0, 0)
        self.encrypt_pubkey = LineEdit()
        self.encrypt_pubkey.setPlaceholderText("接收方公钥 (128字符十六进制)")
        encrypt_layout.addWidget(self.encrypt_pubkey, 0, 1)

        encrypt_layout.addWidget(BodyLabel("明文:"), 1, 0)
        self.plaintext_input = LineEdit()
        self.plaintext_input.setPlaceholderText("输入要加密的明文")
        encrypt_layout.addWidget(self.plaintext_input, 1, 1)

        self.encrypt_btn = PushButton("加密", FluentIcon.ENCRYPT)
        self.encrypt_btn.clicked.connect(self.encrypt)
        encrypt_layout.addWidget(self.encrypt_btn, 2, 0, 1, 2)

        encrypt_group.layout().addLayout(encrypt_layout)
        layout.addWidget(encrypt_group)

        # Ciphertext Display
        self.ciphertext_result = TextEdit()
        self.ciphertext_result.setPlaceholderText("加密结果（密文）...")
        self.ciphertext_result.setReadOnly(True)
        self.ciphertext_result.setMaximumHeight(80)
        layout.addWidget(self.ciphertext_result)

        # Decryption Section
        decrypt_group = self.create_group("解密")
        decrypt_layout = QtWidgets.QGridLayout()

        decrypt_layout.addWidget(BodyLabel("私钥:"), 0, 0)
        self.decrypt_privkey = LineEdit()
        self.decrypt_privkey.setPlaceholderText("你的私钥 (64字符十六进制)")
        decrypt_layout.addWidget(self.decrypt_privkey, 0, 1)

        decrypt_layout.addWidget(BodyLabel("密文:"), 1, 0)
        self.ciphertext_input = LineEdit()
        self.ciphertext_input.setPlaceholderText("输入要解密的密文")
        decrypt_layout.addWidget(self.ciphertext_input, 1, 1)

        self.decrypt_btn = PushButton("解密", FluentIcon.DECRYPT)
        self.decrypt_btn.clicked.connect(self.decrypt)
        decrypt_layout.addWidget(self.decrypt_btn, 2, 0, 1, 2)

        decrypt_group.layout().addLayout(decrypt_layout)
        layout.addWidget(decrypt_group)

        # Decryption Result
        self.decrypt_result = TextEdit()
        self.decrypt_result.setPlaceholderText("解密结果（明文）...")
        self.decrypt_result.setReadOnly(True)
        self.decrypt_result.setMaximumHeight(60)
        layout.addWidget(self.decrypt_result)

        layout.addStretch()

    def create_group(self, title):
        group = QtWidgets.QGroupBox(title)
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        layout = QtWidgets.QVBoxLayout()
        group.setLayout(layout)
        return group

    def generate_keys(self):
        self.gen_key_btn.setEnabled(False)
        self.gen_key_btn.setText("生成中...")
        self.key_result.append("正在生成密钥...")

        self.key_thread = ECCKeyThread(self)
        self.key_thread.call_back.connect(self.on_keys_generated)
        self.key_thread.start()

    def on_keys_generated(self, private_key, public_key, r_value, key_a, key_b):
        self.key_a = key_a
        self.key_b = key_b

        result = f"私钥 d: {private_key}\n"
        result += f"公钥 K: {public_key}\n"
        result += f"随机数 r: {r_value}"

        self.key_result.clear()
        self.key_result.append(result)

        # Auto-fill the inputs
        self.decrypt_privkey.setText(private_key.replace(' ', ''))

        self.gen_key_btn.setEnabled(True)
        self.gen_key_btn.setText("生成密钥对")

        InfoBar.success(
            title="密钥生成成功",
            content="已生成 P-256 曲线密钥对",
            parent=self
        ).show()

    def encrypt(self):
        plaintext = self.plaintext_input.text().strip()

        if not plaintext:
            InfoBar.warning(
                title="输入错误",
                content="请输入要加密的明文",
                parent=self
            ).show()
            return

        if not self.key_a or not self.key_b:
            InfoBar.warning(
                title="密钥错误",
                content="请先生成密钥对",
                parent=self
            ).show()
            return

        self.encrypt_btn.setEnabled(False)
        self.encrypt_btn.setText("加密中...")

        self.encrypt_thread = ECCEncryptThread(
            self, plaintext, self.key_a, self.key_b
        )
        self.encrypt_thread.call_back.connect(self.on_encrypted)
        self.encrypt_thread.start()

    def on_encrypted(self, ciphertext):
        self.ciphertext_result.clear()
        self.ciphertext_result.append(ciphertext)
        self.ciphertext_input.setText(ciphertext.replace(' ', ''))

        self.encrypt_btn.setEnabled(True)
        self.encrypt_btn.setText("加密")

        InfoBar.success(
            title="加密成功",
            content=f"密文长度: {len(ciphertext.replace(' ', ''))} 字符",
            parent=self
        ).show()

    def decrypt(self):
        ciphertext = self.ciphertext_input.text().strip()

        if not ciphertext:
            InfoBar.warning(
                title="输入错误",
                content="请输入要解密的密文",
                parent=self
            ).show()
            return

        self.decrypt_btn.setEnabled(False)
        self.decrypt_btn.setText("解密中...")

        self.decrypt_thread = ECCDecryptThread(
            self, ciphertext, self.key_a, self.key_b
        )
        self.decrypt_thread.call_back.connect(self.on_decrypted)
        self.decrypt_thread.start()

    def on_decrypted(self, plaintext):
        self.decrypt_result.clear()
        self.decrypt_result.append(plaintext)

        self.decrypt_btn.setEnabled(True)
        self.decrypt_btn.setText("解密")

        InfoBar.success(
            title="解密成功",
            content="密文已成功解密为明文",
            parent=self
        ).show()
