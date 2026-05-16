#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from qfluentwidgets import ScrollArea, PushButton, LineEdit, TextEdit, FluentIcon, InfoBar
from qfluentwidgets import StrongBodyLabel, BodyLabel

try:
    from gmssl import sm2, func
except ImportError:
    sm2 = None
    func = None

from infrastructure.converters.TypeConvert import TypeConvert


def str_add_space(out_str: str) -> str:
    """每两个字符添加一个空格"""
    return ' '.join([out_str[i:i+2] for i in range(0, len(out_str), 2)])


class SM2Widget(ScrollArea):
    """SM2 国密加密算法 Widget"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.sm2_crypt = None
        self.current_private_key = ''
        self.current_public_key = ''
        self.current_k = ''
        self.setup_ui()

    def setup_ui(self):
        self.scroll_widget = QtWidgets.QWidget()
        self.setWidget(self.scroll_widget)
        self.setWidgetResizable(True)

        layout = QtWidgets.QVBoxLayout(self.scroll_widget)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(20)

        # Title
        title = StrongBodyLabel("SM2 国密算法")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        # Description
        desc = BodyLabel(
            "SM2 是中国国家密码管理局发布的椭圆曲线公钥密码算法标准，"
            "用于替换 RSA 算法。相比 RSA-2048，SM2 使用更短的密钥即可达到相同安全强度。"
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Key Generation Section
        key_group = self.create_group("密钥生成")
        key_layout = QtWidgets.QGridLayout()

        key_layout.addWidget(BodyLabel("公钥 P:"), 0, 0)
        self.public_key_input = LineEdit()
        self.public_key_input.setPlaceholderText("64字符十六进制公钥（可留空自动生成）")
        key_layout.addWidget(self.public_key_input, 0, 1)

        key_layout.addWidget(BodyLabel("私钥 d:"), 1, 0)
        self.private_key_input = LineEdit()
        self.private_key_input.setPlaceholderText("32字符十六进制私钥（可留空自动生成）")
        key_layout.addWidget(self.private_key_input, 1, 1)

        self.init_key_btn = PushButton("初始化密钥", FluentIcon.UPDATE)
        self.init_key_btn.clicked.connect(self.init_keys)
        key_layout.addWidget(self.init_key_btn, 2, 0, 1, 2)

        self.key_result = TextEdit()
        self.key_result.setPlaceholderText("密钥初始化结果...")
        self.key_result.setReadOnly(True)
        self.key_result.setMaximumHeight(100)
        key_layout.addWidget(self.key_result)

        key_group.layout().addLayout(key_layout)
        layout.addWidget(key_group)

        # Encryption Section
        encrypt_group = self.create_group("加密")
        encrypt_layout = QtWidgets.QGridLayout()

        encrypt_layout.addWidget(BodyLabel("明文:"), 0, 0)
        self.plaintext_input = TextEdit()
        self.plaintext_input.setPlaceholderText("输入要加密的明文")
        self.plaintext_input.setMaximumHeight(80)
        encrypt_layout.addWidget(self.plaintext_input, 0, 1)

        self.encrypt_btn = PushButton("加密", FluentIcon.ENCRYPT)
        self.encrypt_btn.clicked.connect(self.encrypt)
        encrypt_layout.addWidget(self.encrypt_btn, 1, 0, 1, 2)

        encrypt_group.layout().addLayout(encrypt_layout)
        layout.addWidget(encrypt_group)

        # Ciphertext Display
        self.ciphertext_result = TextEdit()
        self.ciphertext_result.setPlaceholderText("加密结果（密文）...")
        self.ciphertext_result.setReadOnly(True)
        self.ciphertext_result.setMaximumHeight(100)
        layout.addWidget(self.ciphertext_result)

        # Decryption Section
        decrypt_group = self.create_group("解密")
        decrypt_layout = QtWidgets.QGridLayout()

        decrypt_layout.addWidget(BodyLabel("密文:"), 0, 0)
        self.ciphertext_input = TextEdit()
        self.ciphertext_input.setPlaceholderText("输入要解密的密文")
        self.ciphertext_input.setMaximumHeight(80)
        decrypt_layout.addWidget(self.ciphertext_input, 0, 1)

        self.decrypt_btn = PushButton("解密", FluentIcon.DECRYPT)
        self.decrypt_btn.clicked.connect(self.decrypt)
        decrypt_layout.addWidget(self.decrypt_btn, 1, 0, 1, 2)

        decrypt_group.layout().addLayout(decrypt_layout)
        layout.addWidget(decrypt_group)

        # Decryption Result
        self.decrypt_result = TextEdit()
        self.decrypt_result.setPlaceholderText("解密结果（明文）...")
        self.decrypt_result.setReadOnly(True)
        self.decrypt_result.setMaximumHeight(80)
        layout.addWidget(self.decrypt_result)

        layout.addStretch()

        # Check gmssl availability
        if sm2 is None:
            InfoBar.warning(
                title="依赖缺失",
                content="gmssl 库未安装，SM2 功能不可用",
                parent=self
            ).show()
            self.setEnabled(False)

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

    def init_keys(self):
        if sm2 is None:
            InfoBar.warning(
                title="错误",
                content="gmssl 库未安装",
                parent=self
            ).show()
            return

        public_key = self.public_key_input.text().strip()
        private_key = self.private_key_input.text().strip()

        try:
            # Create SM2 crypt instance
            self.sm2_crypt = sm2.CryptSM2(
                public_key=public_key if public_key else None,
                private_key=private_key if private_key else None
            )

            # If no keys provided, generate new ones
            if not public_key or not private_key:
                d, P = self.sm2_crypt.generate_key()
                self.current_private_key = d
                self.current_public_key = P
                self.public_key_input.setText(str_add_space(P.upper()))
                self.private_key_input.setText(str_add_space(d.upper()))
            else:
                self.current_private_key = private_key.replace(' ', '')
                self.current_public_key = public_key.replace(' ', '')

            # Generate random k
            self.current_k = func.random_hex(self.sm2_crypt.para_len)

            result = f"公钥 P: {str_add_space(self.current_public_key.upper())}\n"
            result += f"私钥 d: {str_add_space(self.current_private_key.upper())}\n"
            result += f"随机数 k: {str_add_space(self.current_k.upper())}"

            self.key_result.clear()
            self.key_result.append(result)

            InfoBar.success(
                title="初始化成功",
                content="SM2 密钥已就绪",
                parent=self
            ).show()

        except Exception as e:
            InfoBar.error(
                title="初始化失败",
                content=str(e),
                parent=self
            ).show()

    def encrypt(self):
        if self.sm2_crypt is None:
            InfoBar.warning(
                title="密钥错误",
                content="请先初始化密钥",
                parent=self
            ).show()
            return

        plaintext = self.plaintext_input.toPlainText().strip()

        if not plaintext:
            InfoBar.warning(
                title="输入错误",
                content="请输入要加密的明文",
                parent=self
            ).show()
            return

        self.encrypt_btn.setEnabled(False)
        self.encrypt_btn.setText("加密中...")

        try:
            # Encrypt
            ciphertext = self.sm2_crypt.encrypt(
                plaintext.encode('utf-8'),
                self.current_k
            )

            self.ciphertext_result.clear()
            self.ciphertext_result.append(str_add_space(ciphertext.upper()))
            self.ciphertext_input.clear()
            self.ciphertext_input.append(ciphertext.upper())

            InfoBar.success(
                title="加密成功",
                content=f"密文长度: {len(ciphertext)} 字符",
                parent=self
            ).show()

        except Exception as e:
            InfoBar.error(
                title="加密失败",
                content=str(e),
                parent=self
            ).show()

        finally:
            self.encrypt_btn.setEnabled(True)
            self.encrypt_btn.setText("加密")

    def decrypt(self):
        if self.sm2_crypt is None:
            InfoBar.warning(
                title="密钥错误",
                content="请先初始化密钥",
                parent=self
            ).show()
            return

        ciphertext = self.ciphertext_input.toPlainText().strip()

        if not ciphertext:
            InfoBar.warning(
                title="输入错误",
                content="请输入要解密的密文",
                parent=self
            ).show()
            return

        self.decrypt_btn.setEnabled(False)
        self.decrypt_btn.setText("解密中...")

        try:
            # Decrypt
            plaintext = self.sm2_crypt.decrypt(ciphertext.lower())

            self.decrypt_result.clear()
            self.decrypt_result.append(plaintext.decode('utf-8'))

            InfoBar.success(
                title="解密成功",
                content="密文已成功解密",
                parent=self
            ).show()

        except Exception as e:
            InfoBar.error(
                title="解密失败",
                content=str(e),
                parent=self
            ).show()

        finally:
            self.decrypt_btn.setEnabled(True)
            self.decrypt_btn.setText("解密")
