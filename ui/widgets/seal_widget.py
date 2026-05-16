"""
SEAL 流密码界面 - Fluent Design 版本
SEAL (Simulated Encryption Algorithm) 是 IBM 开发的伪随机生成算法
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import (
    ScrollArea, TitleLabel, BodyLabel,
    InfoBar, MessageBox, LineEdit, PrimaryPushButton
)

from ui.components.algorithm_card import KeyCard, EncryptCard, DecryptCard, LogCard
from infrastructure.converters import TypeConvert


class SEALWidget(ScrollArea):
    """SEAL 流密码界面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sealWidget")
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
        title = TitleLabel("SEAL 伪随机生成算法")
        layout.addWidget(title)

        # 描述
        desc = BodyLabel(
            "SEAL (Simulated Encryption Algorithm) 是 IBM 开发的流密码算法。"
            "它基于 SHA-1 的内部结构，使用 160 位密钥和 32 位初始化向量。"
            "算法通过线性反馈移位寄存器和分组密码结构生成伪随机密钥流。"
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # 密钥配置卡片
        self.keyCard = KeyCard()
        self.keyCard.keyEdit.setPlainText("01 23 45 67 89 AB CD EF 01 23 45 67 89 AB CD EF 01 23 45 67")
        self.keyCard.keyEdit.setPlaceholderText("输入密钥（160位 = 20字节，十六进制）...")
        layout.addWidget(self.keyCard)

        # IV 配置
        self.ivCard = QWidget()
        ivLayout = QVBoxLayout(self.ivCard)
        ivLabel = BodyLabel("初始化向量 (IV)")
        self.ivEdit = LineEdit()
        self.ivEdit.setPlaceholderText("输入 IV（32位 = 4字节，十六进制）...")
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
        self.logCard.log("SEAL 算法已加载", "success")

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
        # 生成20字节（160位）密钥
        key_bytes = os.urandom(20)
        key_hex = ' '.join([f'{b:02X}' for b in key_bytes])
        self.keyCard.setKey(key_hex)
        self.logCard.log(f"已生成随机密钥", "success")
        InfoBar.success(
            title="生成成功",
            content="已生成160位随机密钥",
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

            if len(key_list) != 20:
                raise ValueError(f"密钥必须为20字节，当前为{len(key_list)}字节")

            # 验证 IV
            iv_text = self.ivEdit.text()
            valid, result = self.validateHexInput(iv_text, "IV")
            if not valid:
                raise ValueError(result)
            iv_list = result

            if len(iv_list) != 4:
                raise ValueError(f"IV必须为4字节，当前为{len(iv_list)}字节")

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

            # SEAL 加密：与密钥流异或
            from core.algorithms.symmetric.SEAL import Thread as SEALThread

            # 转换参数
            key_int = TypeConvert.hex_list_to_int(key_list)
            iv_int = TypeConvert.hex_list_to_int(iv_list)
            plaintext_int = TypeConvert.hex_list_to_int(plaintext_list)
            block_size = len(plaintext_list) // 4 if len(plaintext_list) >= 4 else 1
            block_size = max(block_size, 1)

            # 创建加密线程
            thread = SEALThread(self, plaintext_int, key_int, 0, key_size=160, block_size=block_size*8)
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
        """解密（SEAL 是流密码，解密等于加密）"""
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

            # SEAL 解密：与加密相同
            from core.algorithms.symmetric.SEAL import Thread as SEALThread

            key_int = TypeConvert.hex_list_to_int(key_list)
            iv_int = TypeConvert.hex_list_to_int(iv_list)
            ciphertext_int = TypeConvert.hex_list_to_int(ciphertext_list)
            block_size = len(ciphertext_list) // 4 if len(ciphertext_list) >= 4 else 1
            block_size = max(block_size, 1)

            thread = SEALThread(self, ciphertext_int, key_int, 1, key_size=160, block_size=block_size*8)
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
