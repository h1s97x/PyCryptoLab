"""
ZUC 祖冲之算法界面 - Fluent Design 版本
ZUC (ZUC) 是中国国密局设计的流密码算法
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import (
    ScrollArea, TitleLabel, BodyLabel,
    InfoBar, MessageBox, LineEdit
)

from ui.components.algorithm_card import KeyCard, EncryptCard, DecryptCard, LogCard
from infrastructure.converters import TypeConvert


class ZUCWidget(ScrollArea):
    """ZUC 祖冲之算法界面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("zucWidget")
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
        title = TitleLabel("ZUC 祖冲之流密码")
        layout.addWidget(title)

        # 描述
        desc = BodyLabel(
            "ZUC (ZUC Algorithm) 是中国国家密码管理局设计的流密码算法，"
            "是 LTE 移动通信系统的国际标准密码算法之一。"
            "算法基于线性反馈移位寄存器 (LFSR) 和非线性布尔函数，"
            "提供 128 位密钥和 128 位初始化向量。"
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # 密钥配置卡片
        self.keyCard = KeyCard()
        self.keyCard.keyEdit.setPlainText("00 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF")
        self.keyCard.keyEdit.setPlaceholderText("输入密钥（128位 = 16字节，十六进制）...")
        layout.addWidget(self.keyCard)

        # IV 配置
        self.ivCard = QWidget()
        ivLayout = QVBoxLayout(self.ivCard)
        ivLabel = BodyLabel("初始化向量 (IV)")
        self.ivEdit = LineEdit()
        self.ivEdit.setPlaceholderText("输入 IV（128位 = 16字节，十六进制）...")
        self.ivEdit.setText("00 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF")
        ivLayout.addWidget(ivLabel)
        ivLayout.addWidget(self.ivEdit)
        layout.addWidget(self.ivCard)

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
        self.logCard.log("ZUC 算法已加载", "success")

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
        # 生成16字节（128位）密钥
        key_bytes = os.urandom(16)
        key_hex = ' '.join([f'{b:02X}' for b in key_bytes])
        self.keyCard.setKey(key_hex)
        self.logCard.log(f"已生成随机密钥", "success")
        InfoBar.success(
            title="生成成功",
            content="已生成128位随机密钥",
            parent=self
        )

        # 同时生成 IV
        iv_bytes = os.urandom(16)
        iv_hex = ' '.join([f'{b:02X}' for b in iv_bytes])
        self.ivEdit.setText(iv_hex)
        self.logCard.log(f"已生成随机 IV", "success")

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

            if len(key_list) != 16:
                raise ValueError(f"密钥必须为16字节，当前为{len(key_list)}字节")

            # 验证 IV
            iv_text = self.ivEdit.text()
            valid, result = self.validateHexInput(iv_text, "IV")
            if not valid:
                raise ValueError(result)
            iv_list = result

            if len(iv_list) != 16:
                raise ValueError(f"IV必须为16字节，当前为{len(iv_list)}字节")

            # 验证明文
            plaintext_text = self.encryptCard.getPlaintext()
            valid, result = self.validateHexInput(plaintext_text, "明文")
            if not valid:
                raise ValueError(result)
            plaintext_list = result

            # 格式化显示
            plaintext_formatted = TypeConvert.hex_list_to_str(plaintext_list)
            key_formatted = TypeConvert.hex_list_to_str(key_list)
            iv_formatted = TypeConvert.hex_list_to_str(iv_list)

            self.encryptCard.setPlaintext(plaintext_formatted)
            self.keyCard.setKey(key_formatted)
            self.ivEdit.setText(iv_formatted)

            self.logCard.log(f"明文长度: {len(plaintext_list)} 字节", "info")
            self.logCard.log(f"密钥长度: {len(key_list)} 字节", "info")
            self.logCard.log(f"IV长度: {len(iv_list)} 字节", "info")

            # ZUC 加密
            from core.algorithms.symmetric.ZUC import Thread as ZUCThread

            # 转换参数
            key_int = TypeConvert.hex_list_to_int(key_list)
            iv_int = TypeConvert.hex_list_to_int(iv_list)
            plaintext_len = len(plaintext_list)

            # 创建加密线程
            thread = ZUCThread(
                self, plaintext_int=plaintext_list,
                key_int=key_int, iv_int=iv_int,
                input_text_len=plaintext_len * 4,
                key_len=len(key_list) * 4,
                encrypt_selected=0
            )
            thread.final_result1.connect(self.onEncryptFinished)
            thread.start()

        except Exception as e:
            self.logCard.log(f"加密失败: {str(e)}", "error")
            MessageBox("错误", f"加密失败: {str(e)}", self).exec()

    def onEncryptFinished(self, key_stream):
        """密钥流生成完成"""
        # ZUC 产生密钥流，需要与明文异或
        try:
            plaintext_text = self.encryptCard.getPlaintext()
            hex_list = TypeConvert.str_to_hex_list(plaintext_text)
            if hex_list is None:
                raise ValueError("明文格式错误")

            # 密钥流处理
            keystream_list = TypeConvert.str_to_hex_list(key_stream)
            if keystream_list is None:
                keystream_list = [0] * len(hex_list)

            # 确保密钥流长度与明文一致
            while len(keystream_list) < len(hex_list):
                keystream_list.append(0)

            # 异或
            ciphertext_list = []
            for i in range(len(hex_list)):
                ciphertext_list.append(hex_list[i] ^ keystream_list[i])

            ciphertext_hex = TypeConvert.hex_list_to_str(ciphertext_list)
            self.encryptCard.setCiphertext(ciphertext_hex)
            self.decryptCard.setCiphertext(ciphertext_hex)

            self.logCard.log(f"密钥流: {key_stream[:50]}...", "success")
            self.logCard.log("加密完成", "success")

            InfoBar.success(
                title="加密成功",
                content="明文已成功加密",
                parent=self
            )
        except Exception as e:
            self.logCard.log(f"处理密钥流失败: {str(e)}", "error")

    def decrypt(self):
        """解密（ZUC 是流密码，解密等于加密）"""
        try:
            self.logCard.log("开始解密...", "info")

            # 验证密钥
            key_text = self.keyCard.getKey()
            valid, result = self.validateHexInput(key_text, "密钥")
            if not valid:
                raise ValueError(result)
            key_list = result

            # 验证 IV
            iv_text = self.ivEdit.text()
            valid, result = self.validateHexInput(iv_text, "IV")
            if not valid:
                raise ValueError(result)
            iv_list = result

            # 验证密文
            ciphertext_text = self.decryptCard.getCiphertext()
            valid, result = self.validateHexInput(ciphertext_text, "密文")
            if not valid:
                raise ValueError(result)
            ciphertext_list = result

            # 格式化显示
            ciphertext_formatted = TypeConvert.hex_list_to_str(ciphertext_list)
            key_formatted = TypeConvert.hex_list_to_str(key_list)
            iv_formatted = TypeConvert.hex_list_to_str(iv_list)

            self.decryptCard.setCiphertext(ciphertext_formatted)
            self.keyCard.setKey(key_formatted)
            self.ivEdit.setText(iv_formatted)

            self.logCard.log(f"密文长度: {len(ciphertext_list)} 字节", "info")

            # ZUC 解密：与加密相同
            from core.algorithms.symmetric.ZUC import Thread as ZUCThread

            key_int = TypeConvert.hex_list_to_int(key_list)
            iv_int = TypeConvert.hex_list_to_int(iv_list)
            ciphertext_len = len(ciphertext_list)

            thread = ZUCThread(
                self, plaintext_int=ciphertext_list,
                key_int=key_int, iv_int=iv_int,
                input_text_len=ciphertext_len * 4,
                key_len=len(key_list) * 4,
                encrypt_selected=0
            )
            thread.final_result1.connect(self.onDecryptFinished)
            thread.start()

        except Exception as e:
            self.logCard.log(f"解密失败: {str(e)}", "error")
            MessageBox("错误", f"解密失败: {str(e)}", self).exec()

    def onDecryptFinished(self, key_stream):
        """密钥流生成完成（解密）"""
        try:
            ciphertext_text = self.decryptCard.getCiphertext()
            hex_list = TypeConvert.str_to_hex_list(ciphertext_text)
            if hex_list is None:
                raise ValueError("密文格式错误")

            keystream_list = TypeConvert.str_to_hex_list(key_stream)
            if keystream_list is None:
                keystream_list = [0] * len(hex_list)

            while len(keystream_list) < len(hex_list):
                keystream_list.append(0)

            # 异或
            plaintext_list = []
            for i in range(len(hex_list)):
                plaintext_list.append(hex_list[i] ^ keystream_list[i])

            plaintext_hex = TypeConvert.hex_list_to_str(plaintext_list)
            self.decryptCard.setPlaintext(plaintext_hex)

            self.logCard.log("解密完成", "success")

            InfoBar.success(
                title="解密成功",
                content="密文已成功解密",
                parent=self
            )
        except Exception as e:
            self.logCard.log(f"处理密钥流失败: {str(e)}", "error")

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
