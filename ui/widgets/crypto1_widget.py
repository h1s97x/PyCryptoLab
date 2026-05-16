"""
Crypto-1 RFID 加密界面 - Fluent Design 版本
Crypto-1 是 MIFARE Classic 卡使用的流密码算法
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import (
    ScrollArea, TitleLabel, BodyLabel,
    InfoBar, MessageBox, LineEdit
)

from ui.components.algorithm_card import KeyCard, EncryptCard, DecryptCard, LogCard
from infrastructure.converters import TypeConvert


class Crypto1Widget(ScrollArea):
    """Crypto-1 RFID 加密界面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("crypto1Widget")
        self.initUI()
        self.connectSignals()

    def initUI(self):
        """初始化UI"""
        self.view = QWidget()
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        layout = QVBoxLayout(self.view)
        layout.setSpacing(16)
        layout.setContentsMargins(36, 36, 36, 36)

        # 标题
        title = TitleLabel("Crypto-1 RFID 加密")
        layout.addWidget(title)

        # 描述
        desc = BodyLabel(
            "Crypto-1 是 NXP 公司为 MIFARE Classic 系列 RFID 卡设计的流密码算法。"
            "该算法使用 48 位线性反馈移位寄存器 (LFSR)，配合三层滤波函数生成密钥流。"
            "主要参数包括 48 位密钥 (UID) 和 32 位输入初始化向量。"
            "<b>注意：此算法已被破解，仅用于学习研究。</b>"
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # 密钥配置卡片
        self.keyCard = KeyCard()
        self.keyCard.keyEdit.setPlainText("00 00 00 00 00 00")
        self.keyCard.keyEdit.setPlaceholderText("输入密钥（48位 = 6字节，十六进制）...")
        layout.addWidget(self.keyCard)

        # Input 配置
        self.inputCard = QWidget()
        inputLayout = QVBoxLayout(self.inputCard)
        inputLabel = BodyLabel("输入值 (Input)")
        self.inputEdit = LineEdit()
        self.inputEdit.setPlaceholderText("输入初始化向量（32位 = 4字节，十六进制）...")
        self.inputEdit.setText("00 00 00 00")
        inputLayout.addWidget(inputLabel)
        inputLayout.addWidget(self.inputEdit)
        layout.addWidget(self.inputCard)

        # 加密卡片
        self.encryptCard = EncryptCard()
        self.encryptCard.plaintextEdit.setPlainText("48 65 6C 6C 6F 20 57 6F 72 6C 64")
        self.encryptCard.plaintextEdit.setPlaceholderText("输入明文（十六进制）...")
        layout.addWidget(self.encryptCard)

        # 解密卡片
        self.decryptCard = DecryptCard()
        self.decryptCard.ciphertextEdit.setPlaceholderText("输入密文（十六进制）...")
        layout.addWidget(self.decryptCard)

        # 日志卡片
        self.logCard = LogCard()
        layout.addWidget(self.logCard)

        layout.addStretch()

        # 初始日志
        self.logCard.log("Crypto-1 算法已加载", "success")

    def connectSignals(self):
        """连接信号"""
        self.keyCard.generateBtn.clicked.connect(self.generateKey)

        self.encryptCard.encryptBtn.clicked.connect(self.encrypt)
        self.encryptCard.copyBtn.clicked.connect(self.copyCiphertext)
        self.encryptCard.clearBtn.clicked.connect(self.encryptCard.clear)

        self.decryptCard.decryptBtn.clicked.connect(self.decrypt)

    def generateKey(self):
        """生成密钥"""
        import os
        # 生成6字节（48位）密钥
        key_bytes = os.urandom(6)
        key_hex = ' '.join([f'{b:02X}' for b in key_bytes])
        self.keyCard.setKey(key_hex)
        self.logCard.log(f"已生成随机密钥", "success")
        InfoBar.success(
            title="生成成功",
            content="已生成48位随机密钥",
            parent=self
        )

    def validateHexInput(self, text, name):
        """验证十六进制输入"""
        try:
            hex_list = TypeConvert.str_to_hex_list(text)

            if hex_list is None or hex_list == 'ERROR_CHARACTER' or hex_list == 'ERROR_LENGTH':
                raise ValueError(f"{name}格式错误")

            if len(hex_list) == 0:
                raise ValueError(f"{name}不能为空")

            return True, hex_list
        except Exception as e:
            return False, str(e)

    def encrypt(self):
        """加密"""
        try:
            self.logCard.log("开始加密...", "info")

            # 验证密钥
            key_text = self.keyCard.getKey()
            valid, result = self.validateHexInput(key_text, "密钥")
            if not valid:
                raise ValueError(result)
            key_list = result

            if len(key_list) != 6:
                raise ValueError(f"密钥必须为6字节，当前为{len(key_list)}字节")

            # 验证 Input
            input_text = self.inputEdit.text()
            valid, result = self.validateHexInput(input_text, "Input")
            if not valid:
                raise ValueError(result)
            input_list = result

            if len(input_list) != 4:
                raise ValueError(f"Input必须为4字节，当前为{len(input_list)}字节")

            # 验证明文
            plaintext_text = self.encryptCard.getPlaintext()
            valid, result = self.validateHexInput(plaintext_text, "明文")
            if not valid:
                raise ValueError(result)
            plaintext_list = result

            # 格式化显示
            plaintext_formatted = TypeConvert.hex_list_to_str(plaintext_list)
            key_formatted = TypeConvert.hex_list_to_str(key_list)
            input_formatted = TypeConvert.hex_list_to_str(input_list)

            self.encryptCard.setPlaintext(plaintext_formatted)
            self.keyCard.setKey(key_formatted)
            self.inputEdit.setText(input_formatted)

            self.logCard.log(f"明文长度: {len(plaintext_list)} 字节", "info")
            self.logCard.log(f"密钥长度: {len(key_list)} 字节", "info")
            self.logCard.log(f"Input长度: {len(input_list)} 字节", "info")

            # Crypto-1 加密
            from core.algorithms.symmetric.Crypto_1 import Thread as Crypto1Thread

            # 转换参数
            key_int = TypeConvert.hex_list_to_int(key_list)
            input_int = TypeConvert.hex_list_to_int(input_list)
            plaintext_int = TypeConvert.hex_list_to_int(plaintext_list)
            plaintext_len = len(plaintext_list)

            # 创建加密线程
            thread = Crypto1Thread(
                self, input_text=plaintext_int,
                input_text_len=plaintext_len,
                key=key_int, key_len=len(key_list),
                input_val=input_int, input_len=len(input_list),
                encrypt_selected=0
            )
            thread.final_result.connect(self.onEncryptFinished)
            thread.start()

        except Exception as e:
            self.logCard.log(f"加密失败: {str(e)}", "error")
            MessageBox("错误", f"加密失败: {str(e)}", self).exec()

    def onEncryptFinished(self, ciphertext):
        """加密完成"""
        self.encryptCard.setCiphertext(ciphertext)
        self.decryptCard.setCiphertext(ciphertext)
        self.logCard.log(f"密文: {ciphertext[:50]}...", "success")
        self.logCard.log("加密完成", "success")

        InfoBar.success(
            title="加密成功",
            content="明文已成功加密",
            parent=self
        )

    def decrypt(self):
        """解密"""
        try:
            self.logCard.log("开始解密...", "info")

            # 验证密钥
            key_text = self.keyCard.getKey()
            valid, result = self.validateHexInput(key_text, "密钥")
            if not valid:
                raise ValueError(result)
            key_list = result

            # 验证 Input
            input_text = self.inputEdit.text()
            valid, result = self.validateHexInput(input_text, "Input")
            if not valid:
                raise ValueError(result)
            input_list = result

            # 验证密文
            ciphertext_text = self.decryptCard.getCiphertext()
            valid, result = self.validateHexInput(ciphertext_text, "密文")
            if not valid:
                raise ValueError(result)
            ciphertext_list = result

            # 格式化显示
            ciphertext_formatted = TypeConvert.hex_list_to_str(ciphertext_list)
            key_formatted = TypeConvert.hex_list_to_str(key_list)
            input_formatted = TypeConvert.hex_list_to_str(input_list)

            self.decryptCard.setCiphertext(ciphertext_formatted)
            self.keyCard.setKey(key_formatted)
            self.inputEdit.setText(input_formatted)

            self.logCard.log(f"密文长度: {len(ciphertext_list)} 字节", "info")

            # Crypto-1 解密
            from core.algorithms.symmetric.Crypto_1 import Thread as Crypto1Thread

            key_int = TypeConvert.hex_list_to_int(key_list)
            input_int = TypeConvert.hex_list_to_int(input_list)
            ciphertext_int = TypeConvert.hex_list_to_int(ciphertext_list)
            ciphertext_len = len(ciphertext_list)

            thread = Crypto1Thread(
                self, input_text=ciphertext_int,
                input_text_len=ciphertext_len,
                key=key_int, key_len=len(key_list),
                input_val=input_int, input_len=len(input_list),
                encrypt_selected=1
            )
            thread.final_result.connect(self.onDecryptFinished)
            thread.start()

        except Exception as e:
            self.logCard.log(f"解密失败: {str(e)}", "error")
            MessageBox("错误", f"解密失败: {str(e)}", self).exec()

    def onDecryptFinished(self, plaintext):
        """解密完成"""
        self.decryptCard.setPlaintext(plaintext)
        self.logCard.log(f"明文: {plaintext[:50]}...", "success")
        self.logCard.log("解密完成", "success")

        InfoBar.success(
            title="解密成功",
            content="密文已成功解密",
            parent=self
        )

    def copyCiphertext(self):
        """复制密文"""
        from PyQt5.QtWidgets import QApplication
        ciphertext = self.encryptCard.getCiphertext()
        QApplication.clipboard().setText(ciphertext)
        self.logCard.log("密文已复制到剪贴板", "success")

    def copyPlaintext(self):
        """复制明文"""
        from PyQt5.QtWidgets import QApplication
        plaintext = self.decryptCard.getPlaintext()
        QApplication.clipboard().setText(plaintext)
        self.logCard.log("明文已复制到剪贴板", "success")
