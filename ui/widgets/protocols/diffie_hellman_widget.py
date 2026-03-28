"""
Diffie-Hellman 密钥交换 - Fluent Design 版本

演示场景：
Diffie-Hellman是一种密钥交换协议，允许两方在不安全的通道上协商出一个共享密钥。

协议步骤：
1. 选择公共参数：大素数 p 和本原根 a
2. Alice 生成私钥 X_A，计算公钥 Y_A = a^X_A mod p
3. Bob 生成私钥 X_B，计算公钥 Y_B = a^X_B mod p
4. Alice 和 Bob 交换公钥
5. Alice 计算共享密钥 K_A = Y_B^X_A mod p
6. Bob 计算共享密钥 K_B = Y_A^X_B mod p
7. K_A = K_B，双方得到相同的共享密钥

注：本版本移除智能卡依赖，使用纯软件模拟
"""

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import (
    ScrollArea, TitleLabel, BodyLabel, CardWidget,
    PrimaryPushButton, PushButton, TextEdit, LineEdit,
    InfoBar, MessageBox, FluentIcon as FIF
)

import secrets
from Crypto.Util import number


def str_add_space(out_str: str) -> str:
    """每2个字符添加一个空格"""
    add_space_str = ''
    for i in range(int(len(out_str) / 2)):
        add_space_str += out_str[i * 2:i * 2 + 2]
        add_space_str += ' '
    return add_space_str.strip()


def _factorize(n):
    """返回 n 的所有素因子集合（试除法）"""
    factors = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
    if n > 1:
        factors.add(n)
    return factors


def find_primitive_root(p, prime_factors_of_p_minus_1=None):
    """找到素数p的本原根

    验证方法：对于 p-1 的每个素因子 q，检查 a^((p-1)/q) mod p != 1。
    如果对所有素因子都满足此条件，则 a 是 p 的本原根。

    Args:
        p: 素数
        prime_factors_of_p_minus_1: p-1 的素因子集合（可选，用于避免重复分解）
    """
    if p == 2:
        return 1

    phi = p - 1
    if prime_factors_of_p_minus_1 is None:
        prime_factors_of_p_minus_1 = _factorize(phi)

    for a in range(2, p):
        is_primitive = True
        for q in prime_factors_of_p_minus_1:
            if pow(a, phi // q, p) == 1:
                is_primitive = False
                break
        if is_primitive:
            return a
    return 2  # 理论上对于素数 p > 2 不会到达这里


class ParamsGenThread(QThread):
    """参数生成线程"""
    finished = pyqtSignal(int, int)
    
    def __init__(self, key_bytes):
        super().__init__()
        self.key_bytes = key_bytes
    
    def run(self):
        try:
            # 生成安全素数 p = 2q + 1，其中 q 也是素数
            # 安全素数的优点：p-1 = 2q 只有两个素因子 {2, q}，
            # 可以高效地验证本原根，且能抵抗小子群攻击
            bits = self.key_bytes * 8
            while True:
                q = number.getPrime(bits - 1)
                p = 2 * q + 1
                if number.isPrime(p):
                    break
            
            # 找到本原根a（对于安全素数，p-1 的素因子为 {2, q}）
            a = find_primitive_root(p, prime_factors_of_p_minus_1={2, q})
            
            self.finished.emit(p, a)
        except Exception as e:
            self.finished.emit(0, 0)


class KeyCalcThread(QThread):
    """密钥计算线程"""
    finished = pyqtSignal(str)
    
    def __init__(self, base, exp, mod, length):
        super().__init__()
        self.base = base
        self.exp = exp
        self.mod = mod
        self.length = length
    
    def run(self):
        try:
            result = pow(self.base, self.exp, self.mod)
            result_hex = hex(result)[2:].upper()
            # 补齐到指定长度
            result_hex = result_hex.zfill(self.length * 2)
            result_formatted = str_add_space(result_hex)
            self.finished.emit(result_formatted)
        except Exception as e:
            self.finished.emit(f"Error: {str(e)}")


class DiffieHellmanWidget(ScrollArea):
    """Diffie-Hellman 密钥交换演示界面"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("diffieHellmanWidget")
        self.prime_p = 0
        self.primitive_a = 0
        self.alice_private = 0
        self.bob_private = 0
        self.initUI()
    
    def initUI(self):
        """初始化UI"""
        self.view = QWidget()
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        
        layout = QVBoxLayout(self.view)
        layout.setSpacing(16)
        layout.setContentsMargins(36, 36, 36, 36)
        
        # 标题
        title = TitleLabel("Diffie-Hellman 密钥交换")
        layout.addWidget(title)
        
        # 描述
        desc = BodyLabel(
            "密钥交换协议：允许双方在不安全的通道上协商出共享密钥。\n"
            "基于离散对数问题的困难性，即使攻击者截获公钥，也无法计算出共享密钥。"
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # 1. 参数生成卡片
        self.paramsCard = self.createParamsCard()
        layout.addWidget(self.paramsCard)
        
        # 2. Alice 卡片
        self.aliceCard = self.createAliceCard()
        layout.addWidget(self.aliceCard)
        
        # 3. Bob 卡片
        self.bobCard = self.createBobCard()
        layout.addWidget(self.bobCard)
        
        # 4. 密钥协商卡片
        self.keyCard = self.createKeyCard()
        layout.addWidget(self.keyCard)
        
        # 5. 日志卡片
        self.logCard = self.createLogCard()
        layout.addWidget(self.logCard)
        
        layout.addStretch()
        
        self.log("Diffie-Hellman 密钥交换演示已加载", "success")
    
    def createParamsCard(self):
        """创建参数生成卡片"""
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setSpacing(12)
        
        # 标题
        title = BodyLabel("⚙️ 步骤1：生成公共参数")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # 密钥长度
        lengthLabel = BodyLabel("密钥长度（字节）")
        layout.addWidget(lengthLabel)
        self.keyLengthEdit = LineEdit()
        self.keyLengthEdit.setText("16")
        self.keyLengthEdit.setPlaceholderText("输入密钥长度（4-32字节）...")
        layout.addWidget(self.keyLengthEdit)
        
        # 素数p
        pLabel = BodyLabel("素数 p (Prime)")
        layout.addWidget(pLabel)
        self.primeEdit = TextEdit()
        self.primeEdit.setReadOnly(True)
        self.primeEdit.setMaximumHeight(60)
        self.primeEdit.setPlaceholderText("点击生成参数...")
        layout.addWidget(self.primeEdit)
        
        # 本原根a
        aLabel = BodyLabel("本原根 a (Primitive Root)")
        layout.addWidget(aLabel)
        self.primitiveEdit = LineEdit()
        self.primitiveEdit.setReadOnly(True)
        self.primitiveEdit.setPlaceholderText("点击生成参数...")
        layout.addWidget(self.primitiveEdit)
        
        # 按钮
        btnLayout = QHBoxLayout()
        self.genParamsBtn = PrimaryPushButton(FIF.SYNC, "生成参数")
        self.genParamsBtn.clicked.connect(self.generateParams)
        self.clearParamsBtn = PushButton(FIF.DELETE, "清空")
        self.clearParamsBtn.clicked.connect(self.clearParams)
        
        btnLayout.addWidget(self.genParamsBtn)
        btnLayout.addWidget(self.clearParamsBtn)
        btnLayout.addStretch()
        layout.addLayout(btnLayout)
        
        return card
    
    def createAliceCard(self):
        """创建 Alice 卡片"""
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setSpacing(12)
        
        # 标题
        title = BodyLabel("👩 步骤2：Alice 生成密钥对")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Alice 私钥
        xaLabel = BodyLabel("Alice 私钥 X_A")
        layout.addWidget(xaLabel)
        self.alicePrivateEdit = TextEdit()
        self.alicePrivateEdit.setReadOnly(True)
        self.alicePrivateEdit.setMaximumHeight(60)
        self.alicePrivateEdit.setPlaceholderText("点击生成...")
        layout.addWidget(self.alicePrivateEdit)
        
        # Alice 公钥
        yaLabel = BodyLabel("Alice 公钥 Y_A = a^X_A mod p")
        layout.addWidget(yaLabel)
        self.alicePublicEdit = TextEdit()
        self.alicePublicEdit.setReadOnly(True)
        self.alicePublicEdit.setMaximumHeight(60)
        self.alicePublicEdit.setPlaceholderText("点击生成...")
        layout.addWidget(self.alicePublicEdit)
        
        # 按钮
        btnLayout = QHBoxLayout()
        self.genAliceBtn = PrimaryPushButton(FIF.FINGERPRINT, "生成 Alice 密钥")
        self.genAliceBtn.clicked.connect(self.generateAliceKeys)
        self.clearAliceBtn = PushButton(FIF.DELETE, "清空")
        self.clearAliceBtn.clicked.connect(self.clearAlice)
        
        btnLayout.addWidget(self.genAliceBtn)
        btnLayout.addWidget(self.clearAliceBtn)
        btnLayout.addStretch()
        layout.addLayout(btnLayout)
        
        return card
    
    def createBobCard(self):
        """创建 Bob 卡片"""
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setSpacing(12)
        
        # 标题
        title = BodyLabel("👨 步骤3：Bob 生成密钥对")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Bob 私钥
        xbLabel = BodyLabel("Bob 私钥 X_B")
        layout.addWidget(xbLabel)
        self.bobPrivateEdit = TextEdit()
        self.bobPrivateEdit.setReadOnly(True)
        self.bobPrivateEdit.setMaximumHeight(60)
        self.bobPrivateEdit.setPlaceholderText("点击生成...")
        layout.addWidget(self.bobPrivateEdit)
        
        # Bob 公钥
        ybLabel = BodyLabel("Bob 公钥 Y_B = a^X_B mod p")
        layout.addWidget(ybLabel)
        self.bobPublicEdit = TextEdit()
        self.bobPublicEdit.setReadOnly(True)
        self.bobPublicEdit.setMaximumHeight(60)
        self.bobPublicEdit.setPlaceholderText("点击生成...")
        layout.addWidget(self.bobPublicEdit)
        
        # 按钮
        btnLayout = QHBoxLayout()
        self.genBobBtn = PrimaryPushButton(FIF.FINGERPRINT, "生成 Bob 密钥")
        self.genBobBtn.clicked.connect(self.generateBobKeys)
        self.clearBobBtn = PushButton(FIF.DELETE, "清空")
        self.clearBobBtn.clicked.connect(self.clearBob)
        
        btnLayout.addWidget(self.genBobBtn)
        btnLayout.addWidget(self.clearBobBtn)
        btnLayout.addStretch()
        layout.addLayout(btnLayout)
        
        return card
    
    def createKeyCard(self):
        """创建密钥协商卡片"""
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setSpacing(12)
        
        # 标题
        title = BodyLabel("🔑 步骤4：计算共享密钥")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Alice 计算的共享密钥
        kaLabel = BodyLabel("Alice 计算的共享密钥 K_A = Y_B^X_A mod p")
        layout.addWidget(kaLabel)
        self.aliceSharedEdit = TextEdit()
        self.aliceSharedEdit.setReadOnly(True)
        self.aliceSharedEdit.setMaximumHeight(60)
        self.aliceSharedEdit.setPlaceholderText("点击计算...")
        layout.addWidget(self.aliceSharedEdit)
        
        # Bob 计算的共享密钥
        kbLabel = BodyLabel("Bob 计算的共享密钥 K_B = Y_A^X_B mod p")
        layout.addWidget(kbLabel)
        self.bobSharedEdit = TextEdit()
        self.bobSharedEdit.setReadOnly(True)
        self.bobSharedEdit.setMaximumHeight(60)
        self.bobSharedEdit.setPlaceholderText("点击计算...")
        layout.addWidget(self.bobSharedEdit)
        
        # 验证结果
        verifyLabel = BodyLabel("验证结果")
        layout.addWidget(verifyLabel)
        self.verifyEdit = TextEdit()
        self.verifyEdit.setReadOnly(True)
        self.verifyEdit.setMaximumHeight(60)
        self.verifyEdit.setPlaceholderText("验证结果...")
        layout.addWidget(self.verifyEdit)
        
        # 按钮
        btnLayout = QHBoxLayout()
        self.calcAliceKeyBtn = PrimaryPushButton(FIF.CALCULATOR, "Alice 计算密钥")
        self.calcAliceKeyBtn.clicked.connect(self.calculateAliceSharedKey)
        self.calcBobKeyBtn = PushButton(FIF.CALCULATOR, "Bob 计算密钥")
        self.calcBobKeyBtn.clicked.connect(self.calculateBobSharedKey)
        self.verifyBtn = PushButton(FIF.ACCEPT, "验证")
        self.verifyBtn.clicked.connect(self.verifyKeys)
        self.clearKeyBtn = PushButton(FIF.DELETE, "清空")
        self.clearKeyBtn.clicked.connect(self.clearKey)
        
        btnLayout.addWidget(self.calcAliceKeyBtn)
        btnLayout.addWidget(self.calcBobKeyBtn)
        btnLayout.addWidget(self.verifyBtn)
        btnLayout.addWidget(self.clearKeyBtn)
        btnLayout.addStretch()
        layout.addLayout(btnLayout)
        
        return card
    
    def createLogCard(self):
        """创建日志卡片"""
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        
        title = BodyLabel("📊 操作日志")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        self.logEdit = TextEdit()
        self.logEdit.setReadOnly(True)
        self.logEdit.setMaximumHeight(150)
        layout.addWidget(self.logEdit)
        
        btnLayout = QHBoxLayout()
        self.clearLogBtn = PushButton(FIF.DELETE, "清空日志")
        self.clearLogBtn.clicked.connect(lambda: self.logEdit.clear())
        btnLayout.addWidget(self.clearLogBtn)
        btnLayout.addStretch()
        layout.addLayout(btnLayout)
        
        return card
    
    # ========== 功能实现 ==========
    
    def generateParams(self):
        """生成公共参数"""
        try:
            key_length = int(self.keyLengthEdit.text())
            
            if key_length < 4 or key_length > 32:
                InfoBar.warning(
                    title="长度无效",
                    content="密钥长度必须在4-32字节之间",
                    parent=self
                )
                return
            
            self.log(f"正在生成 {key_length} 字节的公共参数...", "info")
            self.genParamsBtn.setEnabled(False)
            
            # 创建参数生成线程
            self.paramsThread = ParamsGenThread(key_length)
            self.paramsThread.finished.connect(self.onParamsGenFinished)
            self.paramsThread.start()
            
        except ValueError:
            InfoBar.error(
                title="输入错误",
                content="请输入有效的数字",
                parent=self
            )
        except Exception as e:
            self.log(f"生成参数失败: {str(e)}", "error")
            MessageBox("错误", f"生成失败: {str(e)}", self).exec()
            self.genParamsBtn.setEnabled(True)
    
    def onParamsGenFinished(self, p, a):
        """参数生成完成"""
        self.genParamsBtn.setEnabled(True)
        
        if p == 0 or a == 0:
            self.log("生成参数失败", "error")
            MessageBox("错误", "生成参数失败", self).exec()
            return
        
        self.prime_p = p
        self.primitive_a = a
        
        # 格式化显示
        p_hex = hex(p)[2:].upper()
        p_formatted = str_add_space(p_hex)
        
        self.primeEdit.setPlainText(p_formatted)
        self.primitiveEdit.setText(str(a))
        
        self.log(f"素数 p: {p_formatted[:50]}...", "success")
        self.log(f"本原根 a: {a}", "success")
        
        InfoBar.success(
            title="生成成功",
            content=f"公共参数已生成（{len(p_hex)//2}字节）",
            parent=self
        )
    
    def generateAliceKeys(self):
        """生成 Alice 密钥对"""
        try:
            if self.prime_p == 0 or self.primitive_a == 0:
                InfoBar.warning(
                    title="参数未生成",
                    content="请先生成公共参数",
                    parent=self
                )
                return
            
            key_length = int(self.keyLengthEdit.text())
            
            # 生成 Alice 私钥（使用密码学安全随机数）
            self.alice_private = secrets.randbelow(self.prime_p - 3) + 2
            
            # 格式化私钥
            xa_hex = hex(self.alice_private)[2:].upper().zfill(key_length * 2)
            xa_formatted = str_add_space(xa_hex)
            self.alicePrivateEdit.setPlainText(xa_formatted)
            
            self.log(f"Alice 私钥 X_A: {xa_formatted[:50]}...", "info")
            self.log("正在计算 Alice 公钥...", "info")
            
            # 计算 Alice 公钥
            self.aliceKeyThread = KeyCalcThread(self.primitive_a, self.alice_private, self.prime_p, key_length)
            self.aliceKeyThread.finished.connect(self.onAliceKeyFinished)
            self.aliceKeyThread.start()
            
        except Exception as e:
            self.log(f"生成 Alice 密钥失败: {str(e)}", "error")
            MessageBox("错误", f"生成失败: {str(e)}", self).exec()
    
    def onAliceKeyFinished(self, ya):
        """Alice 公钥计算完成"""
        if "Error" in ya:
            self.log(f"计算失败: {ya}", "error")
            return
        
        self.alicePublicEdit.setPlainText(ya)
        self.log(f"Alice 公钥 Y_A: {ya[:50]}...", "success")
        
        InfoBar.success(
            title="生成成功",
            content="Alice 密钥对已生成",
            parent=self
        )
    
    def generateBobKeys(self):
        """生成 Bob 密钥对"""
        try:
            if self.prime_p == 0 or self.primitive_a == 0:
                InfoBar.warning(
                    title="参数未生成",
                    content="请先生成公共参数",
                    parent=self
                )
                return
            
            key_length = int(self.keyLengthEdit.text())
            
            # 生成 Bob 私钥（使用密码学安全随机数）
            self.bob_private = secrets.randbelow(self.prime_p - 3) + 2
            
            # 格式化私钥
            xb_hex = hex(self.bob_private)[2:].upper().zfill(key_length * 2)
            xb_formatted = str_add_space(xb_hex)
            self.bobPrivateEdit.setPlainText(xb_formatted)
            
            self.log(f"Bob 私钥 X_B: {xb_formatted[:50]}...", "info")
            self.log("正在计算 Bob 公钥...", "info")
            
            # 计算 Bob 公钥
            self.bobKeyThread = KeyCalcThread(self.primitive_a, self.bob_private, self.prime_p, key_length)
            self.bobKeyThread.finished.connect(self.onBobKeyFinished)
            self.bobKeyThread.start()
            
        except Exception as e:
            self.log(f"生成 Bob 密钥失败: {str(e)}", "error")
            MessageBox("错误", f"生成失败: {str(e)}", self).exec()
    
    def onBobKeyFinished(self, yb):
        """Bob 公钥计算完成"""
        if "Error" in yb:
            self.log(f"计算失败: {yb}", "error")
            return
        
        self.bobPublicEdit.setPlainText(yb)
        self.log(f"Bob 公钥 Y_B: {yb[:50]}...", "success")
        
        InfoBar.success(
            title="生成成功",
            content="Bob 密钥对已生成",
            parent=self
        )
    
    def calculateAliceSharedKey(self):
        """Alice 计算共享密钥"""
        try:
            if self.alice_private == 0:
                InfoBar.warning(
                    title="密钥未生成",
                    content="请先生成 Alice 密钥对",
                    parent=self
                )
                return
            
            yb_text = self.bobPublicEdit.toPlainText().replace(" ", "")
            if not yb_text:
                InfoBar.warning(
                    title="公钥未生成",
                    content="请先生成 Bob 密钥对",
                    parent=self
                )
                return
            
            yb = int(yb_text, 16)
            key_length = int(self.keyLengthEdit.text())
            
            self.log("Alice 正在计算共享密钥...", "info")
            
            # 计算共享密钥
            self.aliceSharedThread = KeyCalcThread(yb, self.alice_private, self.prime_p, key_length)
            self.aliceSharedThread.finished.connect(self.onAliceSharedFinished)
            self.aliceSharedThread.start()
            
        except Exception as e:
            self.log(f"计算失败: {str(e)}", "error")
            MessageBox("错误", f"计算失败: {str(e)}", self).exec()
    
    def onAliceSharedFinished(self, ka):
        """Alice 共享密钥计算完成"""
        if "Error" in ka:
            self.log(f"计算失败: {ka}", "error")
            return
        
        self.aliceSharedEdit.setPlainText(ka)
        self.log(f"Alice 共享密钥 K_A: {ka[:50]}...", "success")
        
        InfoBar.success(
            title="计算成功",
            content="Alice 共享密钥已计算",
            parent=self
        )
    
    def calculateBobSharedKey(self):
        """Bob 计算共享密钥"""
        try:
            if self.bob_private == 0:
                InfoBar.warning(
                    title="密钥未生成",
                    content="请先生成 Bob 密钥对",
                    parent=self
                )
                return
            
            ya_text = self.alicePublicEdit.toPlainText().replace(" ", "")
            if not ya_text:
                InfoBar.warning(
                    title="公钥未生成",
                    content="请先生成 Alice 密钥对",
                    parent=self
                )
                return
            
            ya = int(ya_text, 16)
            key_length = int(self.keyLengthEdit.text())
            
            self.log("Bob 正在计算共享密钥...", "info")
            
            # 计算共享密钥
            self.bobSharedThread = KeyCalcThread(ya, self.bob_private, self.prime_p, key_length)
            self.bobSharedThread.finished.connect(self.onBobSharedFinished)
            self.bobSharedThread.start()
            
        except Exception as e:
            self.log(f"计算失败: {str(e)}", "error")
            MessageBox("错误", f"计算失败: {str(e)}", self).exec()
    
    def onBobSharedFinished(self, kb):
        """Bob 共享密钥计算完成"""
        if "Error" in kb:
            self.log(f"计算失败: {kb}", "error")
            return
        
        self.bobSharedEdit.setPlainText(kb)
        self.log(f"Bob 共享密钥 K_B: {kb[:50]}...", "success")
        
        InfoBar.success(
            title="计算成功",
            content="Bob 共享密钥已计算",
            parent=self
        )
    
    def verifyKeys(self):
        """验证共享密钥"""
        try:
            ka_text = self.aliceSharedEdit.toPlainText().replace(" ", "")
            kb_text = self.bobSharedEdit.toPlainText().replace(" ", "")
            
            if not ka_text or not kb_text:
                InfoBar.warning(
                    title="密钥未计算",
                    content="请先计算双方的共享密钥",
                    parent=self
                )
                return
            
            if ka_text == kb_text:
                result = "✅ 验证成功\n\nK_A = K_B\n\nAlice 和 Bob 成功协商出相同的共享密钥！"
                self.log("验证成功：K_A = K_B", "success")
                InfoBar.success(
                    title="验证成功",
                    content="双方共享密钥一致",
                    parent=self
                )
            else:
                result = "❌ 验证失败\n\nK_A ≠ K_B\n\n共享密钥不一致，请检查计算过程。"
                self.log("验证失败：K_A ≠ K_B", "error")
                InfoBar.error(
                    title="验证失败",
                    content="共享密钥不一致",
                    parent=self
                )
            
            self.verifyEdit.setPlainText(result)
            
        except Exception as e:
            self.log(f"验证失败: {str(e)}", "error")
            MessageBox("错误", f"验证失败: {str(e)}", self).exec()
    
    # ========== 清空功能 ==========
    
    def clearParams(self):
        """清空参数"""
        self.primeEdit.clear()
        self.primitiveEdit.clear()
        self.prime_p = 0
        self.primitive_a = 0
        self.log("已清空公共参数", "info")
    
    def clearAlice(self):
        """清空 Alice 数据"""
        self.alicePrivateEdit.clear()
        self.alicePublicEdit.clear()
        self.alice_private = 0
        self.log("已清空 Alice 数据", "info")
    
    def clearBob(self):
        """清空 Bob 数据"""
        self.bobPrivateEdit.clear()
        self.bobPublicEdit.clear()
        self.bob_private = 0
        self.log("已清空 Bob 数据", "info")
    
    def clearKey(self):
        """清空共享密钥"""
        self.aliceSharedEdit.clear()
        self.bobSharedEdit.clear()
        self.verifyEdit.clear()
        self.log("已清空共享密钥", "info")
    
    # ========== 日志功能 ==========
    
    def log(self, message, level='info'):
        """添加日志"""
        icons = {
            'info': 'ℹ️',
            'success': '✅',
            'warning': '⚠️',
            'error': '❌'
        }
        colors = {
            'info': '#3b82f6',
            'success': '#10b981',
            'warning': '#f59e0b',
            'error': '#ef4444'
        }
        
        icon = icons.get(level, 'ℹ️')
        color = colors.get(level, '#3b82f6')
        
        self.logEdit.append(
            f"{icon} <span style='color: {color};'>{message}</span>"
        )
