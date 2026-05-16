# CryptographicProtocol 重构计划

## 概述

将 `CryptographicProtocol/` 目录下的7个密码协议从旧UI框架迁移到 Fluent UI。

## 当前状态

### 现有协议列表

| 协议 | 文件 | 复杂度 | 优先级 |
|------|------|--------|--------|
| Diffie-Hellman | `Diffie_Hellman_ui.py` | 高（智能卡） | P2 |
| Digital Envelope | `Digital_Envelope_ui.py`, `Digital_Envelope.py` | 高（RSA+AES） | P2 |
| Digital Certificate | `Digital_Certificate_ui.py`, `Digital_Certificate.py` | 高（PKI） | P3 |
| Verify | `Verify_ui.py` | 中 | P2 |
| Millionaire | `Millionaire_ui.py` | 中（安全多方计算） | P3 |
| Replay Attack | `Replay_Attack_ui.py` | 低 | P3 |
| Zero Knowledge Proof | `Zero_Knowledge_Proof_ui.py` | 中 | P3 |

### 技术债务

1. **使用旧UI框架**
   - 继承自 `CryptographyWidget`
   - 使用 `Group`, `Button`, `PlainTextEdit` 配置
   - 需要迁移到 Fluent UI 组件

2. **智能卡依赖**
   - Diffie-Hellman 等协议依赖智能卡通信
   - 需要保留或模拟智能卡功能

3. **目录位置**
   - 当前在根目录 `CryptographicProtocol/`
   - 建议移动到 `core/protocols/` 或保持现状

## 重构策略

### 阶段1：目录重组（可选）

**选项A：移动到 core/protocols/**
```
core/
├── algorithms/
│   ├── classical/
│   ├── symmetric/
│   ├── asymmetric/
│   ├── hash/
│   └── mathematical/
└── protocols/          # 新增
    ├── diffie_hellman.py
    ├── digital_envelope.py
    └── ...
```

**选项B：保持当前位置**
```
CryptographicProtocol/  # 保持不变
├── __init__.py
├── diffie_hellman.py   # 重命名（去掉_ui后缀）
└── ...
```

**建议：选项B** - 保持当前位置，只重构UI

### 阶段2：UI重构

#### 2.1 创建 Fluent UI Widget

每个协议创建对应的 Fluent Widget：

```python
# ui/widgets/protocols/diffie_hellman_widget.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import ScrollArea, TitleLabel, BodyLabel

class DiffieHellmanWidget(ScrollArea):
    """Diffie-Hellman 密钥交换协议"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        # 使用 Fluent UI 组件
        pass
```

#### 2.2 组件映射

| 旧组件 | 新组件 |
|--------|--------|
| `PlainTextEdit` | `TextEdit` / `LineEdit` |
| `Button` | `PrimaryPushButton` / `PushButton` |
| `Group` | `CardWidget` |
| `CryptographyWidget` | `ScrollArea` |

#### 2.3 智能卡功能

**选项A：保留智能卡功能**
- 创建 `SmartCardWidget` 组件
- 保留 APDU 通信功能

**选项B：移除智能卡功能**
- 简化为纯软件实现
- 移除智能卡相关代码

**建议：选项B** - 先移除智能卡功能，简化重构

### 阶段3：核心逻辑分离

将业务逻辑从UI中分离：

```python
# CryptographicProtocol/diffie_hellman.py
class DiffieHellman:
    """Diffie-Hellman 协议核心逻辑"""
    
    def __init__(self, key_length=16):
        self.key_length = key_length
        self.prime = None
        self.primitive = None
    
    def generate_parameters(self):
        """生成参数 p 和 a"""
        pass
    
    def generate_private_key(self):
        """生成私钥 X_A"""
        pass
    
    def calculate_public_key(self, private_key):
        """计算公钥 Y_A = a^X_A mod p"""
        pass
    
    def calculate_shared_secret(self, other_public_key, private_key):
        """计算共享密钥 K = Y_B^X_A mod p"""
        pass
```

## 实施步骤

### Step 1: 准备工作 ✅

- [x] 分析现有协议
- [x] 制定重构计划
- [x] 创建 `ui/widgets/protocols/` 目录
- [ ] 创建基础组件

### 当前状态

**已完成**:
- 分析了7个密码协议的复杂度和依赖
- 制定了详细的重构计划
- 创建了协议Widget目录结构
- 确定了重构策略（保持目录位置，移除智能卡依赖）
- ✅ 完成 Replay Attack 协议重构（ECDSA签名演示）
- ✅ 完成 Verify 协议重构（挑战-响应验证，AES-ECB加密）
- ✅ 完成 Millionaire Problem 协议重构（安全多方计算，RSA加密）
- ✅ 完成 Zero Knowledge Proof 协议重构（阿里巴巴洞穴，概率验证）
- ✅ 完成 Digital Envelope 协议重构（RSA+AES混合加密）
- ✅ 完成 Diffie-Hellman 协议重构（DH密钥交换，离散对数）
- ✅ 完成 Digital Certificate 协议重构（数字证书，PKI公钥基础设施）

**下一步**:
- 全部7个协议重构已完成
- 可以进行全面测试和文档更新

### Step 2: 简单协议重构（P3） ✅

1. **Replay Attack** - 最简单 ✅
   - [x] 创建 `ui/widgets/protocols/replay_attack_widget.py`
   - [x] 实现 Fluent UI
   - [x] 移除智能卡依赖
   - [x] 测试功能
   - 状态：完成

2. **Verify** - 中等复杂度 ✅
   - [x] 创建 `ui/widgets/protocols/verify_widget.py`
   - [x] 实现 Fluent UI（6个卡片：PC密钥、智能卡密钥、挑战、响应、验证、日志）
   - [x] 移除智能卡依赖，使用 AES-ECB 纯软件模拟
   - [x] 添加到主窗口配置
   - [x] 创建测试脚本 `test_verify.py`
   - 状态：完成

### Step 3: 中等协议重构（P2）

3. **Millionaire Problem** ✅
   - [x] 创建 `ui/widgets/protocols/millionaire_widget.py`
   - [x] 实现 Fluent UI（5个卡片：初始化、李的操作、王的操作、验证、日志）
   - [x] 实现完整的安全多方计算流程
   - [x] 使用简化RSA加密
   - [x] 添加到主窗口配置
   - [x] 创建测试脚本 `test_millionaire.py`
   - 状态：完成

4. **Zero Knowledge Proof** ✅
   - [x] 创建 `ui/widgets/protocols/zkp_widget.py`
   - [x] 实现 Fluent UI（5个卡片：设置、单次验证、批量验证、统计、日志）
   - [x] 实现阿里巴巴洞穴场景
   - [x] 支持单次和批量验证
   - [x] 添加统计分析和结论
   - [x] 添加到主窗口配置
   - [x] 创建测试脚本 `test_zkp.py`
   - 状态：完成

### Step 4: 复杂协议重构（P2-P3）

5. **Digital Envelope** ✅
   - [x] 创建 `ui/widgets/protocols/digital_envelope_widget.py`
   - [x] 实现 Fluent UI（4个卡片：密钥生成、加密、解密、日志）
   - [x] 结合RSA和AES的混合加密方案
   - [x] 使用2048位RSA和128位AES
   - [x] 移除智能卡依赖
   - [x] 添加到主窗口配置
   - [x] 创建测试脚本 `test_digital_envelope.py`
   - 状态：完成

6. **Diffie-Hellman** ✅
   - [x] 创建 `ui/widgets/protocols/diffie_hellman_widget.py`
   - [x] 实现 Fluent UI（5个卡片：参数生成、Alice、Bob、密钥协商、日志）
   - [x] 实现完整的DH密钥交换流程
   - [x] 移除智能卡依赖，纯软件实现
   - [x] 使用异步线程处理大数运算
   - [x] 添加到主窗口配置
   - [x] 创建测试脚本 `test_diffie_hellman.py`
   - 状态：完成

7. **Digital Certificate** ✅
   - [x] 创建 `ui/widgets/protocols/digital_certificate_widget.py`
   - [x] 实现 Fluent UI（5个卡片：CA密钥生成、用户密钥生成、证书颁发、证书验证、日志）
   - [x] 实现完整的PKI证书颁发和验证流程
   - [x] 使用cryptography库生成X.509证书
   - [x] 移除智能卡依赖，纯软件实现
   - [x] 添加到主窗口配置
   - [x] 创建测试脚本 `test_digital_certificate.py`
   - 状态：完成

### Step 5: 集成和测试 ✅

- [x] 更新主窗口导航
- [x] 添加协议分类
- [x] 更新首页显示7个协议
- [x] 全面测试
- [x] 更新文档

## 完成状态

**所有7个密码协议重构已完成！**

1. ✅ Replay Attack - 重放攻击演示（ECDSA签名）
2. ✅ Verify - 挑战-响应验证协议（AES-ECB加密）
3. ✅ Millionaire - 百万富翁问题（安全多方计算，RSA加密）
4. ✅ Zero Knowledge Proof - 零知识证明（阿里巴巴洞穴）
5. ✅ Digital Envelope - 数字信封（RSA+AES混合加密）
6. ✅ Diffie-Hellman - DH密钥交换（离散对数）
7. ✅ Digital Certificate - 数字证书（PKI公钥基础设施）

所有协议均已：
- 迁移到Fluent UI设计
- 移除智能卡依赖
- 使用异步线程处理耗时操作
- 集成到主窗口导航
- 创建独立测试脚本

## 时间估算

- Step 1: 1小时
- Step 2: 2-3小时（2个协议）
- Step 3: 3-4小时（2个协议）
- Step 4: 6-8小时（3个协议）
- Step 5: 2小时

**总计：14-18小时**

## 风险和挑战

1. **智能卡依赖**
   - 风险：移除智能卡功能可能影响教学价值
   - 缓解：保留智能卡代码注释，未来可恢复

2. **复杂业务逻辑**
   - 风险：协议逻辑复杂，重构可能引入bug
   - 缓解：逐步重构，充分测试

3. **时间投入**
   - 风险：重构耗时较长
   - 缓解：分阶段进行，优先级排序

## 决策点

### 决策1：是否移动目录？

**决定：保持当前位置**
- 理由：减少改动范围，降低风险
- 后续可以再考虑重组

### 决策2：是否保留智能卡功能？

**决定：暂时移除**
- 理由：简化重构，降低复杂度
- 保留代码注释，未来可恢复

### 决策3：重构顺序？

**决定：从简单到复杂**
- 理由：快速验证方案，积累经验
- 降低风险

## 下一步行动

1. 创建 `ui/widgets/protocols/` 目录
2. 从 Replay Attack 开始重构
3. 逐步完成其他协议
4. 更新主窗口集成

---

**创建日期**: 2026-03-05  
**状态**: 规划中  
**负责人**: Kiro AI Assistant
