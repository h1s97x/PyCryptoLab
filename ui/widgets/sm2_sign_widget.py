#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
SM2 签名算法 Widget
基于 gmssl 库的 SM2 数字签名实现
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QGroupBox
from PyQt5.QtCore import Qt
from qfluentwidgets import LineEdit, PrimaryPushButton, MessageWidget, GroupHeaderCard, SimpleCard

from core.algorithms.asymmetric.SM2 import SM2SignKeyThread, SM2SignThread, SM2VerifyThread


class SM2SignWidget(QWidget):
    """SM2 签名算法界面"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.private_key = ""
        self.public_key = ""
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 密钥生成卡片
        key_card = GroupHeaderCard("密钥生成")
        key_layout = QVBoxLayout()

        self.key_gen_btn = PrimaryPushButton("生成密钥对")
        self.key_gen_btn.clicked.connect(self.generate_keys)
        key_layout.addWidget(self.key_gen_btn)

        key_info = QLabel("私钥和公钥将自动显示在下方的输入框中")
        key_info.setStyleSheet("color: gray;")
        key_layout.addWidget(key_info)

        key_card.body_layout.addLayout(key_layout)
        layout.addWidget(key_card)

        # 密钥输入卡片
        key_input_card = GroupHeaderCard("密钥输入")
        key_input_layout = QVBoxLayout()

        self.private_key_input = LineEdit()
        self.private_key_input.setPlaceholderText("私钥 (64位十六进制)")
        key_input_layout.addWidget(QLabel("私钥:"))
        key_input_layout.addWidget(self.private_key_input)

        self.public_key_input = LineEdit()
        self.public_key_input.setPlaceholderText("公钥 (128位十六进制)")
        key_input_layout.addWidget(QLabel("公钥:"))
        key_input_layout.addWidget(self.public_key_input)

        key_input_card.body_layout.addLayout(key_input_layout)
        layout.addWidget(key_input_card)

        # 签名卡片
        sign_card = GroupHeaderCard("签名")
        sign_layout = QVBoxLayout()

        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("输入要签名的消息...")
        self.message_input.setMaximumHeight(80)
        sign_layout.addWidget(QLabel("消息:"))
        sign_layout.addWidget(self.message_input)

        self.sign_btn = PrimaryPushButton("签名")
        self.sign_btn.clicked.connect(self.do_sign)
        self.sign_btn.setEnabled(False)
        sign_layout.addWidget(self.sign_btn)

        self.signature_output = QTextEdit()
        self.signature_output.setPlaceholderText("签名结果将显示在这里...")
        self.signature_output.setMaximumHeight(60)
        self.signature_output.setReadOnly(True)
        sign_layout.addWidget(QLabel("签名:"))
        sign_layout.addWidget(self.signature_output)

        sign_card.body_layout.addLayout(sign_layout)
        layout.addWidget(sign_card)

        # 验签卡片
        verify_card = GroupHeaderCard("验签")
        verify_layout = QVBoxLayout()

        self.verify_signature_input = QTextEdit()
        self.verify_signature_input.setPlaceholderText("输入要验证的签名...")
        self.verify_signature_input.setMaximumHeight(60)
        verify_layout.addWidget(QLabel("签名:"))
        verify_layout.addWidget(self.verify_signature_input)

        self.verify_btn = PrimaryPushButton("验签")
        self.verify_btn.clicked.connect(self.do_verify)
        self.verify_btn.setEnabled(False)
        verify_layout.addWidget(self.verify_btn)

        self.verify_result = QLabel("")
        self.verify_result.setAlignment(Qt.AlignCenter)
        self.verify_result.setStyleSheet("font-size: 14px; font-weight: bold;")
        verify_layout.addWidget(self.verify_result)

        verify_card.body_layout.addLayout(verify_layout)
        layout.addWidget(verify_card)

        # 消息提示
        self.message_widget = MessageWidget(self)
        layout.addWidget(self.message_widget)

        layout.addStretch()

    def generate_keys(self):
        """生成 SM2 签名密钥对"""
        self.key_gen_thread = SM2SignKeyThread(self)
        self.key_gen_thread.call_back.connect(self.on_keys_generated)
        self.key_gen_thread.start()
        self.key_gen_btn.setEnabled(False)

    def on_keys_generated(self, private_key, public_key):
        """密钥生成完成回调"""
        self.private_key = private_key
        self.public_key = public_key
        self.private_key_input.setText(private_key)
        self.public_key_input.setText(public_key)
        self.sign_btn.setEnabled(True)
        self.verify_btn.setEnabled(True)
        self.key_gen_btn.setEnabled(True)
        self.message_widget.showMessage("密钥生成成功", MessageWidget.Success)

    def do_sign(self):
        """执行签名"""
        private_key = self.private_key_input.text().strip()
        public_key = self.public_key_input.text().strip()
        message = self.message_input.toPlainText().strip()

        if not private_key or not public_key:
            self.message_widget.showMessage("请先生成或输入密钥", MessageWidget.Warning)
            return

        if not message:
            self.message_widget.showMessage("请输入要签名的消息", MessageWidget.Warning)
            return

        self.sign_thread = SM2SignThread(self, private_key, public_key, message)
        self.sign_thread.call_back.connect(self.on_sign_completed)
        self.sign_thread.start()
        self.sign_btn.setEnabled(False)

    def on_sign_completed(self, signature):
        """签名完成回调"""
        self.signature_output.setPlainText(signature)
        self.verify_signature_input.setPlainText(signature)
        self.sign_btn.setEnabled(True)
        if signature.startswith("Error:"):
            self.message_widget.showMessage(signature, MessageWidget.Error)
        else:
            self.message_widget.showMessage("签名成功", MessageWidget.Success)

    def do_verify(self):
        """执行验签"""
        public_key = self.public_key_input.text().strip()
        message = self.message_input.toPlainText().strip()
        signature = self.verify_signature_input.toPlainText().strip()

        if not public_key:
            self.message_widget.showMessage("请输入公钥", MessageWidget.Warning)
            return

        if not message:
            self.message_widget.showMessage("请输入消息", MessageWidget.Warning)
            return

        if not signature:
            self.message_widget.showMessage("请输入签名", MessageWidget.Warning)
            return

        self.verify_thread = SM2VerifyThread(self, public_key, message, signature)
        self.verify_thread.call_back.connect(self.on_verify_completed)
        self.verify_thread.start()
        self.verify_btn.setEnabled(False)

    def on_verify_completed(self, result, message):
        """验签完成回调"""
        self.verify_btn.setEnabled(True)
        if result:
            self.verify_result.setText("验签成功 ✓")
            self.verify_result.setStyleSheet("color: green; font-size: 14px; font-weight: bold;")
        else:
            self.verify_result.setText("验签失败 ✗")
            self.verify_result.setStyleSheet("color: red; font-size: 14px; font-weight: bold;")
        self.message_widget.showMessage(message, MessageWidget.Success if result else MessageWidget.Error)
