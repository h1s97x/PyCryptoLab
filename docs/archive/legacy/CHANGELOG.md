# 变更日志

本文档记录项目的重要变更和版本更新。

---

## [2.1.0] - 2026-03-05

### HTML 算法介绍页面集成 ✅

#### 新增功能
- 创建 `AlgorithmIntroButton` 组件，支持在算法Widget中嵌入HTML介绍页面
- 使用 QWebEngineView 渲染完整的HTML内容（支持CSS、JS、MathJax）
- 实现全屏对话框显示算法介绍
- 集成7个算法的HTML介绍页面：AES, Caesar, DES, Hill, MD5, SM4, Vigenere

#### 技术实现
- 新增 `ui/components/intro_button.py` - 算法介绍按钮组件
- 新增 `ui/components/html_viewer.py` - HTML查看器组件
- 新增 `docs/HTML_INTEGRATION.md` - 集成方案文档
- 新增 `scripts/add_intro_buttons.py` - 批量集成辅助脚本

#### 使用方法
```python
from ui.components.intro_button import AlgorithmIntroButton
self.introBtn = AlgorithmIntroButton("AES")
```

---

## [2.0.0] - 2026-03-04

### Fluent UI 重构完成 ✅

#### 重大变更
- 完全重写UI层，采用Fluent Design设计语言
- 使用QFluentWidgets组件库替代传统PyQt5组件
- 实现深色/浅色主题自动切换
- 采用现代化卡片式布局

#### 新增功能
- 实现28个密码学算法的Fluent UI界面（28/37，75.7%）
- 创建可复用组件库（KeyCard, EncryptCard, DecryptCard, LogCard, HashCard, RSAKeyCard）
- 添加实时操作日志和中间值显示
- 支持文件导入/导出功能
- 支持剪贴板一键复制
- 异步处理耗时操作，不阻塞界面

#### 已实现算法
- 经典密码：7/7（100%）- Hill, Caesar, Vigenere, Playfair, Enigma, Monoalphabetic, Frequency Analysis
- 对称密码：8/10（80%）- AES, DES, SM4, RC4, SPECK, SIMON, Block Mode
- 公钥密码：4/7（57.1%）- RSA, RSA Sign, ElGamal, ECDSA
- 哈希算法：7/8（87.5%）- MD5, SHA-1, SHA-256, SHA-3, SM3, HMAC-MD5, AES-CBC-MAC
- 数学基础：3/3（100%）- Euler, CRT, Euclidean

#### Bug修复
- 修复TypeConvert导入错误
- 修复SHA3和SM3的HashCard属性错误
- 修复Euler组件的FluentIcon属性错误
- 移除ECC组件的错误引用

#### 测试
- 创建自动化测试脚本 `test_algorithms.py`
- 测试通过率：100%（28个widgets + 5个核心算法 + 主窗口）
- 所有组件可正常导入和运行

#### 文档
- 更新README.md，添加完整算法列表和项目信息
- 创建DEVELOPMENT_PROGRESS.md跟踪开发进度
- 创建BRANCH_MIGRATION.md记录分支迁移
- 保留classic-ui分支作为旧版本参考

#### 项目清理
- 删除45个旧UI文件
- 整合根目录和ui目录文件
- 统一main.py作为唯一入口点

---

## [1.0.0] - Classic UI

### 经典版本（已归档）

#### 特性
- 传统PyQt5界面设计
- 37个算法原型实现
- 基础功能完整

#### 访问方式
```bash
git checkout classic-ui
python main.py
```

**注意**：经典UI版本已停止维护，建议使用Fluent UI版本

---

## 版本说明

### 版本号规则

采用语义化版本号：`主版本号.次版本号.修订号`

- **主版本号**：重大架构变更或不兼容的API修改
- **次版本号**：新功能添加，向后兼容
- **修订号**：Bug修复和小改进

### 开发路线图

| 版本 | 状态 | 说明 |
|------|------|------|
| 2.0.0 | ✅ 已完成 | Fluent UI重构，28个算法实现 |
| 2.1.0 | 🚧 计划中 | 完成剩余9个算法 |
| 2.2.0 | 📋 规划中 | 性能优化和用户体验改进 |
| 3.0.0 | 💡 构思中 | 密码协议和高级功能 |

---

## 统计数据

### 当前版本 (v2.0.0)

| 指标 | 数值 |
|------|------|
| 已实现算法 | 28/37 (75.7%) |
| UI组件数 | 28个 |
| 可复用组件 | 6个 |
| 测试通过率 | 100% |
| 代码行数 | ~15,000 |
| 文档数量 | 20+ |

### 算法完成度

| 分类 | 完成度 |
|------|--------|
| 经典密码 | 7/7 (100% ✅) |
| 对称密码 | 8/10 (80%) |
| 公钥密码 | 4/7 (57.1%) |
| 哈希算法 | 7/8 (87.5%) |
| 数学基础 | 3/3 (100% ✅) |

---

## 下一步计划

### v2.1.0 - 算法完善（开发中）

**目标**：完成剩余9个算法实现

待实现算法：
- 对称密码：SEAL, ZUC, Crypto-1
- 公钥密码：ECC, SM2, SM2 Sign
- 哈希算法：Hash Reverse

**预计完成时间**：2-3周

### v2.2.0 - 性能优化（规划中）

**目标**：提升性能和用户体验

计划改进：
- 优化大文件处理性能
- 改进UI响应速度
- 添加进度条显示
- 优化内存使用
- 添加批量处理功能

### v3.0.0 - 高级功能（构思中）

**目标**：扩展密码协议和高级应用

计划功能：
- Diffie-Hellman密钥交换
- 数字证书管理
- 数字信封
- 零知识证明
- 重放攻击演示
- 百万富翁问题

---

## 参考

- [开发进度](DEVELOPMENT_PROGRESS.md) - 查看详细的开发进度
- [架构文档](ARCHITECTURE.md) - 了解系统设计
- [分支迁移](BRANCH_MIGRATION.md) - 版本切换指南
- [快速开始](guides/QUICK_START.md) - 快速上手指南

---

**最后更新**：2026-03-04  
**当前版本**：v2.0.0 Fluent UI  
**维护者**：密码学平台开发团队
