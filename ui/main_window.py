"""
Fluent Design 主窗口
使用 QFluentWidgets 实现现代化界面，支持分层导航
"""

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from qfluentwidgets import (
    FluentWindow, NavigationItemPosition, FluentIcon,
    setTheme, Theme, setThemeColor, MessageBox
)
from qfluentwidgets import FluentIcon as FIF


class FluentMainWindow(FluentWindow):
    """基于 Fluent Design 的主窗口"""
    
    def __init__(self):
        super().__init__()
        self.initWindow()
        self.initNavigation()
        self.initCategoryInterfaces()
        self.connectSignals()
    
    def initWindow(self):
        """初始化窗口"""
        self.setWindowTitle("密码学平台")
        self.resize(1200, 800)
    
    def initNavigation(self):
        """初始化导航栏"""
        
        # 延迟导入，避免循环依赖
        from ui.interfaces.home_interface import HomeInterface
        from ui.interfaces.settings_interface import SettingsInterface
        
        # 首页
        self.homeInterface = HomeInterface(self)
        self.addSubInterface(
            self.homeInterface,
            FIF.HOME,
            '首页',
            NavigationItemPosition.TOP
        )
        
        # 创建分类导航组
        self.navigationInterface.addSeparator(NavigationItemPosition.SCROLL)
        
        # 经典密码
        self.addNavigationGroup('经典密码', FIF.FONT, 'classical')
        
        # 对称密码
        self.addNavigationGroup('对称密码', FIF.FINGERPRINT, 'symmetric')
        
        # 公钥密码
        self.addNavigationGroup('公钥密码', FIF.CERTIFICATE, 'asymmetric')
        
        # 哈希算法
        self.addNavigationGroup('哈希算法', FIF.TAG, 'hash')
        
        # 数学基础
        self.addNavigationGroup('数学基础', FIF.EDIT, 'mathematical')
        
        # 密码协议
        self.addNavigationGroup('密码协议', FIF.LINK, 'protocols')
        
        # 设置（底部）
        self.settingsInterface = SettingsInterface(self)
        self.addSubInterface(
            self.settingsInterface,
            FIF.SETTING,
            '设置',
            NavigationItemPosition.BOTTOM
        )
    
    def addNavigationGroup(self, title, icon, category):
        """添加导航组"""
        # 创建父节点
        self.navigationInterface.addItem(
            routeKey=f'{category}_group',
            icon=icon,
            text=title,
            onClick=lambda: self.switchTo(self.categoryInterfaces[category]),
            position=NavigationItemPosition.SCROLL
        )
    
    def initCategoryInterfaces(self):
        """初始化分类界面"""
        from ui.interfaces.category_interface import CategoryInterface
        
        self.categoryInterfaces = {}
        self.algorithmWidgets = {}
        
        # 经典密码分类
        self.categoryInterfaces['classical'] = CategoryInterface(
            '经典密码',
            '古典密码学算法，包括替换密码、置换密码等',
            [
                {'icon': FIF.DOCUMENT, 'name': 'Hill', 'description': '基于矩阵运算的多表替换密码', 'objectName': 'hillWidget'},
                {'icon': FIF.DOCUMENT, 'name': 'Caesar', 'description': '最简单的移位替换密码', 'objectName': 'caesarWidget'},
                {'icon': FIF.DOCUMENT, 'name': 'Vigenere', 'description': '多表替换密码，使用密钥字', 'objectName': 'vigenereWidget'},
                {'icon': FIF.DOCUMENT, 'name': 'Playfair', 'description': '双字母替换密码', 'objectName': 'playfairWidget'},
                {'icon': FIF.DOCUMENT, 'name': 'Enigma', 'description': '二战德军使用的转子密码机', 'objectName': 'enigmaWidget'},
                {'icon': FIF.DOCUMENT, 'name': 'Monoalphabetic', 'description': '单表替换密码', 'objectName': 'monoWidget'},
                {'icon': FIF.DOCUMENT, 'name': 'Frequency Analysis', 'description': '频率分析破解工具', 'objectName': 'freqWidget'},
            ],
            self
        )
        
        # 对称密码分类
        self.categoryInterfaces['symmetric'] = CategoryInterface(
            '对称密码',
            '现代分组密码和流密码算法',
            [
                {'icon': FIF.FINGERPRINT, 'name': 'AES', 'description': '高级加密标准，最广泛使用', 'objectName': 'aesWidget'},
                {'icon': FIF.FINGERPRINT, 'name': 'DES', 'description': '数据加密标准', 'objectName': 'desWidget'},
                {'icon': FIF.FINGERPRINT, 'name': 'SM4', 'description': '国密分组密码算法', 'objectName': 'sm4Widget'},
                {'icon': FIF.FINGERPRINT, 'name': 'RC4', 'description': '流密码算法', 'objectName': 'rc4Widget'},
                {'icon': FIF.FINGERPRINT, 'name': 'SPECK', 'description': 'NSA轻量级分组密码', 'objectName': 'speckWidget'},
                {'icon': FIF.FINGERPRINT, 'name': 'SIMON', 'description': 'NSA轻量级分组密码', 'objectName': 'simonWidget'},
                {'icon': FIF.FINGERPRINT, 'name': 'Block Mode', 'description': 'ECB和CBC分组模式', 'objectName': 'blockModeWidget'},
                {'icon': FIF.FINGERPRINT, 'name': 'SEAL', 'description': 'IBM伪随机生成算法', 'objectName': 'sealWidget'},
                {'icon': FIF.FINGERPRINT, 'name': 'ZUC', 'description': '国密流密码算法（LTE标准）', 'objectName': 'zucWidget'},
                {'icon': FIF.FINGERPRINT, 'name': 'Crypto-1', 'description': 'MIFARE RFID加密算法', 'objectName': 'crypto1Widget'},
            ],
            self
        )
        
        # 公钥密码分类
        self.categoryInterfaces['asymmetric'] = CategoryInterface(
            '公钥密码',
            '非对称加密和数字签名算法',
            [
                {'icon': FIF.CERTIFICATE, 'name': 'RSA', 'description': '最常用的公钥加密算法', 'objectName': 'rsaWidget'},
                {'icon': FIF.CERTIFICATE, 'name': 'RSA Sign', 'description': 'RSA数字签名', 'objectName': 'rsaSignWidget'},
                {'icon': FIF.CERTIFICATE, 'name': 'ElGamal', 'description': '基于离散对数的公钥密码', 'objectName': 'elgamalWidget'},
                {'icon': FIF.CERTIFICATE, 'name': 'ECC', 'description': '椭圆曲线密码学（P-256曲线）', 'objectName': 'eccWidget'},
                {'icon': FIF.CERTIFICATE, 'name': 'ECDSA', 'description': '椭圆曲线数字签名算法', 'objectName': 'ecdsaWidget'},
                {'icon': FIF.CERTIFICATE, 'name': 'SM2', 'description': '国密椭圆曲线公钥密码算法', 'objectName': 'sm2Widget'},
                {'icon': FIF.CERTIFICATE, 'name': 'SM2 Sign', 'description': 'SM2数字签名算法', 'objectName': 'sm2SignWidget'},
            ],
            self
        )
        
        # 哈希算法分类
        self.categoryInterfaces['hash'] = CategoryInterface(
            '哈希算法',
            '消息摘要和消息认证码算法',
            [
                {'icon': FIF.TAG, 'name': 'MD5', 'description': '128位消息摘要算法', 'objectName': 'md5Widget'},
                {'icon': FIF.TAG, 'name': 'SHA-1', 'description': '160位安全哈希算法', 'objectName': 'sha1Widget'},
                {'icon': FIF.TAG, 'name': 'SHA-256', 'description': 'SHA-2系列256位哈希', 'objectName': 'sha256Widget'},
                {'icon': FIF.TAG, 'name': 'SHA-3', 'description': '最新的哈希标准', 'objectName': 'sha3Widget'},
                {'icon': FIF.TAG, 'name': 'SM3', 'description': '国密哈希算法', 'objectName': 'sm3Widget'},
                {'icon': FIF.TAG, 'name': 'HMAC-MD5', 'description': '基于MD5的消息认证码', 'objectName': 'hmacmd5Widget'},
                {'icon': FIF.TAG, 'name': 'AES-CBC-MAC', 'description': '基于AES-CBC的MAC', 'objectName': 'aesCbcMacWidget'},
            ],
            self
        )
        
        # 数学基础分类
        self.categoryInterfaces['mathematical'] = CategoryInterface(
            '数学基础',
            '密码学相关的数学算法和定理',
            [
                {'icon': FIF.EDIT, 'name': 'Euler', 'description': '欧拉定理和欧拉函数', 'objectName': 'eulerWidget'},
                {'icon': FIF.EDIT, 'name': 'CRT', 'description': '中国剩余定理', 'objectName': 'crtWidget'},
                {'icon': FIF.EDIT, 'name': 'Euclidean', 'description': '欧几里得算法求最大公约数', 'objectName': 'euclideanWidget'},
            ],
            self
        )
        
        # 密码协议分类
        self.categoryInterfaces['protocols'] = CategoryInterface(
            '密码协议',
            '基于密码算法构建的安全协议',
            [
                {'icon': FIF.LINK, 'name': 'Replay Attack', 'description': '重放攻击演示 - ECDSA签名', 'objectName': 'replayAttackWidget'},
                {'icon': FIF.LINK, 'name': 'Verify', 'description': '挑战-响应验证协议 - AES加密', 'objectName': 'verifyWidget'},
                {'icon': FIF.LINK, 'name': 'Millionaire', 'description': '百万富翁问题 - 安全多方计算', 'objectName': 'millionaireWidget'},
                {'icon': FIF.LINK, 'name': 'Zero Knowledge Proof', 'description': '零知识证明 - 阿里巴巴洞穴', 'objectName': 'zkpWidget'},
                {'icon': FIF.LINK, 'name': 'Digital Envelope', 'description': '数字信封 - RSA+AES混合加密', 'objectName': 'digitalEnvelopeWidget'},
                {'icon': FIF.LINK, 'name': 'Diffie-Hellman', 'description': 'DH密钥交换 - 离散对数', 'objectName': 'diffieHellmanWidget'},
                {'icon': FIF.LINK, 'name': 'Digital Certificate', 'description': '数字证书 - PKI公钥基础设施', 'objectName': 'digitalCertificateWidget'},
            ],
            self
        )
        
        # 将分类界面添加到窗口（但不添加到导航栏）
        for category, interface in self.categoryInterfaces.items():
            self.stackedWidget.addWidget(interface)
    
    def connectSignals(self):
        """连接信号"""
        # 首页分类点击
        self.homeInterface.categoryClicked.connect(self.onCategoryClicked)
        
        # 分类界面算法点击
        for interface in self.categoryInterfaces.values():
            interface.algorithmClicked.connect(self.onAlgorithmClicked)
    
    def onCategoryClicked(self, category):
        """分类卡片点击"""
        if category in self.categoryInterfaces:
            self.switchTo(self.categoryInterfaces[category])
    
    def onAlgorithmClicked(self, objectName):
        """算法卡片点击"""
        # 延迟加载算法Widget
        if objectName not in self.algorithmWidgets:
            self.loadAlgorithmWidget(objectName)
        
        # 切换到算法界面
        if objectName in self.algorithmWidgets:
            self.switchTo(self.algorithmWidgets[objectName])
    
    def loadAlgorithmWidget(self, objectName):
        """延迟加载算法Widget"""
        widget_map = {
            # 经典密码
            'hillWidget': ('ui.widgets.hill_widget', 'HillWidget'),
            'caesarWidget': ('ui.widgets.caesar_widget', 'CaesarWidget'),
            'vigenereWidget': ('ui.widgets.vigenere_widget', 'VigenereWidget'),
            'playfairWidget': ('ui.widgets.playfair_widget', 'PlayfairWidget'),
            'enigmaWidget': ('ui.widgets.enigma_widget', 'EnigmaWidget'),
            'monoWidget': ('ui.widgets.monoalphabetic_widget', 'MonoalphabeticWidget'),
            'freqWidget': ('ui.widgets.frequency_analysis_widget', 'FrequencyAnalysisWidget'),
            
            # 对称密码
            'aesWidget': ('ui.widgets.aes_widget', 'AESWidget'),
            'desWidget': ('ui.widgets.des_widget', 'DESWidget'),
            'sm4Widget': ('ui.widgets.sm4_widget', 'SM4Widget'),
            'rc4Widget': ('ui.widgets.rc4_widget', 'RC4Widget'),
            'speckWidget': ('ui.widgets.speck_widget', 'SPECKWidget'),
            'simonWidget': ('ui.widgets.simon_widget', 'SIMONWidget'),
            'blockModeWidget': ('ui.widgets.block_mode_widget', 'BlockModeWidget'),
            'sealWidget': ('ui.widgets.seal_widget', 'SEALWidget'),
            'zucWidget': ('ui.widgets.zuc_widget', 'ZUCWidget'),
            'crypto1Widget': ('ui.widgets.crypto1_widget', 'Crypto1Widget'),
            
            # 公钥密码
            'rsaWidget': ('ui.widgets.rsa_widget', 'RSAWidget'),
            'rsaSignWidget': ('ui.widgets.rsa_sign_widget', 'RSASignWidget'),
            'elgamalWidget': ('ui.widgets.elgamal_widget', 'ElGamalWidget'),
            'eccWidget': ('ui.widgets.ecc_widget', 'ECCWidget'),
            'ecdsaWidget': ('ui.widgets.ecdsa_widget', 'ECDSAWidget'),
            'sm2Widget': ('ui.widgets.sm2_widget', 'SM2Widget'),
            'sm2SignWidget': ('ui.widgets.sm2_sign_widget', 'SM2SignWidget'),
            
            # 哈希算法
            'md5Widget': ('ui.widgets.md5_widget', 'MD5Widget'),
            'sha1Widget': ('ui.widgets.sha1_widget', 'SHA1Widget'),
            'sha256Widget': ('ui.widgets.sha256_widget', 'SHA256Widget'),
            'sha3Widget': ('ui.widgets.sha3_widget', 'SHA3Widget'),
            'sm3Widget': ('ui.widgets.sm3_widget', 'SM3Widget'),
            'hmacmd5Widget': ('ui.widgets.hmac_md5_widget', 'HMACMD5Widget'),
            'aesCbcMacWidget': ('ui.widgets.aes_cbc_mac_widget', 'AESCBCMACWidget'),
            
            # 数学基础
            'eulerWidget': ('ui.widgets.euler_widget', 'EulerWidget'),
            'crtWidget': ('ui.widgets.crt_widget', 'CRTWidget'),
            'euclideanWidget': ('ui.widgets.euclidean_widget', 'EuclideanWidget'),
            
            # 密码协议
            'replayAttackWidget': ('ui.widgets.protocols.replay_attack_widget', 'ReplayAttackWidget'),
            'verifyWidget': ('ui.widgets.protocols.verify_widget', 'VerifyWidget'),
            'millionaireWidget': ('ui.widgets.protocols.millionaire_widget', 'MillionaireWidget'),
            'zkpWidget': ('ui.widgets.protocols.zkp_widget', 'ZKPWidget'),
            'digitalEnvelopeWidget': ('ui.widgets.protocols.digital_envelope_widget', 'DigitalEnvelopeWidget'),
            'diffieHellmanWidget': ('ui.widgets.protocols.diffie_hellman_widget', 'DiffieHellmanWidget'),
            'digitalCertificateWidget': ('ui.widgets.protocols.digital_certificate_widget', 'DigitalCertificateWidget'),
        }
        
        if objectName in widget_map:
            module_path, class_name = widget_map[objectName]
            try:
                # 动态导入
                module = __import__(module_path, fromlist=[class_name])
                widget_class = getattr(module, class_name)
                widget = widget_class(self)
                widget.setObjectName(objectName)
                
                # 添加到stackedWidget
                self.stackedWidget.addWidget(widget)
                self.algorithmWidgets[objectName] = widget
                
            except Exception as e:
                MessageBox("错误", f"加载算法失败: {str(e)}", self).exec()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = FluentMainWindow()
    window.show()
    sys.exit(app.exec_())
