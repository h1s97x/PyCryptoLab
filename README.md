# 密码学平台 - Fluent UI

现代化的密码学算法学习与实验平台，采用 Fluent Design 设计语言。

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ 特性

- 🎨 **现代化界面** - 采用 Fluent Design 设计语言
- 🌓 **主题支持** - 深色/浅色主题自动切换
- 📚 **丰富算法** - 28个密码学算法完整实现
- 🔐 **全面覆盖** - 经典密码、对称密码、公钥密码、哈希算法、数学基础
- 📊 **实时反馈** - 操作日志和中间值显示
- 💾 **文件操作** - 支持文件导入/导出
- 📋 **剪贴板** - 一键复制加密结果
- ⚡ **异步处理** - 耗时操作不阻塞界面

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- Windows / macOS / Linux

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
# 自动主题（跟随系统）
python main.py

# 浅色主题
python main.py --theme light

# 深色主题
python main.py --theme dark
```

## 📚 支持的算法 (33/37)

### 经典密码 (7/7) ✅
- ✅ Hill 密码 - 矩阵加密
- ✅ Caesar 密码 - 移位加密
- ✅ Vigenere 密码 - 多表替换
- ✅ Playfair 密码 - 双字母替换
- ✅ Enigma 密码 - 转子密码机
- ✅ Monoalphabetic 密码 - 单表替换
- ✅ Frequency Analysis - 频率分析

### 对称密码 (10/10) ✅
- ✅ AES - 高级加密标准
- ✅ DES - 数据加密标准
- ✅ SM4 - 国密分组密码
- ✅ RC4 - 流密码
- ✅ SPECK - NSA轻量级密码
- ✅ SIMON - NSA轻量级密码
- ✅ Block Mode - ECB/CBC模式
- ✅ SEAL - 伪随机生成算法
- ✅ ZUC - 祖冲之流密码
- ✅ Crypto-1 - RFID加密

### 公钥密码 (7/7) ✅
- ✅ RSA - 公钥加密
- ✅ RSA Sign - RSA数字签名
- ✅ ElGamal - 公钥加密
- ✅ ECDSA - 椭圆曲线数字签名
- ✅ ECC - 椭圆曲线加密
- ✅ SM2 - 国密公钥密码
- ✅ SM2 Sign - 国密数字签名

### 哈希算法 (7/8)
- ✅ MD5 - 消息摘要算法
- ✅ SHA-1 - 安全哈希算法
- ✅ SHA-256 - SHA-2系列
- ✅ SHA-3 - 最新哈希标准
- ✅ SM3 - 国密哈希算法
- ✅ HMAC-MD5 - 消息认证码
- ✅ AES-CBC-MAC - 分组密码MAC
- 🚧 Hash Reverse - 哈希反查

### 数学基础 (3/3) ✅
- ✅ Euler 定理 - 欧拉函数
- ✅ CRT - 中国剩余定理
- ✅ Euclidean - 欧几里得算法

**完成度**: 33/37 (89.2%)

✅ 已完成 | 🚧 开发中

## 📁 项目结构

```
Cryptography/
├── core/                      # 核心算法实现
│   ├── algorithms/           # 算法模块
│   │   ├── classical/       # 经典密码 (7个)
│   │   ├── symmetric/       # 对称密码 (10个)
│   │   ├── asymmetric/      # 非对称密码 (7个)
│   │   ├── hash/            # 哈希算法 (8个)
│   │   └── mathematical/    # 数学基础 (3个)
│   ├── interfaces/          # 接口定义
│   └── validators/          # 验证器
├── ui/                       # 用户界面
│   └── fluent/              # Fluent UI实现
│       ├── main_window.py   # 主窗口
│       ├── components/      # 可复用组件
│       │   └── algorithm_card.py  # 算法卡片组件
│       ├── interfaces/      # 界面页面
│       │   ├── home_interface.py  # 首页
│       │   └── settings_interface.py  # 设置页
│       └── widgets/         # 算法界面 (28个)
├── infrastructure/          # 基础设施
│   ├── converters/         # 类型转换工具
│   ├── security/           # 安全工具
│   └── Path.py             # 路径工具
├── CryptographicProtocol/  # 密码协议
├── resources/              # 资源文件
├── docs/                   # 文档
│   ├── ARCHITECTURE.md     # 架构设计
│   ├── ROADMAP.md         # 项目路线图
│   ├── GITHUB_RELEASE_GUIDE.md
│   ├── build-guide.md     # 构建指南
│   ├── user-guide.md      # 用户指南
│   ├── README.md          # 文档目录
│   └── archive/           # 历史文档归档
│       ├── legacy/        # 过时的项目文档
│       ├── guides/        # 旧版开发指南
│       └── reports/       # 历史报告
├── test_algorithms.py      # 自动化测试脚本
├── main.py                 # 程序入口
└── requirements.txt        # 依赖列表
```

## 🧪 测试

运行单元测试：

```bash
# 安装测试依赖
pip install pytest pytest-cov flake8 gmssl

# 运行所有测试
pytest tests/unit/ -v

# 运行并生成覆盖率报告
pytest tests/unit/ --cov=core --cov-report=html
```

测试内容包括：
- ✅ 33 个算法 Widget 导入测试
- ✅ 77 个单元测试用例
- ✅ 核心算法功能测试

## 📖 文档

- [CHANGELOG](CHANGELOG.md) - 版本更新记录
- [贡献指南](CONTRIBUTING.md) - 如何参与项目贡献
- [用户指南](docs/user-guide.md) - 界面使用说明
- [构建指南](docs/build-guide.md) - 项目构建说明
- [架构说明](docs/ARCHITECTURE.md) - 系统架构设计
- [归档文档](docs/archive/README.md) - 历史文档存档

## 🔄 版本历史

### v2.0 - Fluent UI (当前版本)
- ✅ 33 个算法完整实现 (89.2%)
- ✅ 77 个单元测试用例
- ✅ GitHub Actions CI/CD 流水线
- ✅ 全新 Fluent Design 界面
- ✅ 深色/浅色主题支持
- ✅ 多平台打包支持 (Windows/macOS/Linux)
- ✅ 详细的贡献指南和文档

### v1.0 - Classic UI
- 经典界面设计
- 37个算法原型实现
- 基础功能完整

如需使用经典 UI 版本，请切换到 `classic-ui` 分支：

```bash
git checkout classic-ui
python main.py
```

## 🛠️ 技术栈

- **Python** 3.8+ - 核心语言
- **PyQt5** - GUI框架
- **QFluentWidgets** - Fluent Design组件库
- **NumPy** - 数值计算
- **PyCryptodome** - 密码学库
- **gmpy2** - 大数运算

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

请参阅 [贡献指南](CONTRIBUTING.md) 了解详细的开发流程和代码规范。

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 👥 作者

密码学平台开发团队

## 🙏 致谢

- [QFluentWidgets](https://qfluentwidgets.com/) - 优秀的 Fluent Design 组件库
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - 强大的 Python GUI 框架
- [PyCryptodome](https://www.pycryptodome.org/) - 密码学算法库

---

⭐ 如果这个项目对你有帮助，请给我们一个 Star！
