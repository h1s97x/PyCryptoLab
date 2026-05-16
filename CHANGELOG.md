# Changelog

所有重要的项目更新都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
本项目遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added
- 添加 SEAL 算法 Widget
- 添加 ZUC 算法 Widget
- 添加 Crypto-1 算法 Widget
- 添加 ECC 算法 Widget
- 添加 SM2 算法 Widget
- 添加 SM2 签名算法

### Changed
- 更新 `build_config.spec` 添加新 Widget imports

## [2.0.0] - 2024-XX-XX

### Added

#### GitHub Actions CI/CD
- `.github/workflows/ci.yml` - 持续集成流水线
  - `lint`: flake8 代码检查
  - `test`: pytest 单元测试
  - `build-check`: 模块导入验证
- `.github/workflows/release.yml` - 发布流水线
  - 多平台构建（Windows/Ubuntu/macOS）
  - 自动创建 GitHub Release

#### 单元测试 (77 个测试用例)
- `tests/unit/test_type_convert.py` - 22 个测试用例
- `tests/unit/test_euclidean.py` - 6 个测试用例
- `tests/unit/test_sm2_sign.py` - 6 个测试用例
- `tests/unit/test_zuc.py` - 16 个测试用例
- `tests/unit/test_crypto1.py` - 14 个测试用例
- `tests/unit/test_ecc.py` - 13 个测试用例

#### 算法 Widget
- `seal_widget.py` - SEAL 伪随机生成算法
- `zuc_widget.py` - ZUC 祖冲之流密码
- `crypto1_widget.py` - Crypto-1 RFID 加密
- `ecc_widget.py` - ECC 椭圆曲线密码
- `sm2_widget.py` - SM2 公钥加密
- `sm2_sign_widget.py` - SM2 数字签名

### Changed
- `pyproject.toml` - 项目元数据和工具配置
- `README.md` - 更新文档和算法状态
- `requirements.txt` - 依赖管理

## [2.0.0-alpha] - 2024-XX-XX

### Added
- 全新 Fluent Design 界面
- 深色/浅色主题切换
- 28 个密码学算法实现

### Features
- 🎨 现代化 Fluent Design 界面
- 🌓 主题自动/手动切换
- 📚 经典密码、对称密码、公钥密码、哈希算法
- 🔐 实时日志和中间值显示
- 💾 文件导入/导出
- 📋 剪贴板支持
- ⚡ 异步处理

## [1.0.0] - 2023-XX-XX

### Added
- 经典界面设计
- 37 个算法原型实现
- 基础功能完整

---

## 版本号规则

版本格式：`MAJOR.MINOR.PATCH`

- **MAJOR**: 破坏性 API 变更
- **MINOR**: 新功能（向后兼容）
- **PATCH**: Bug 修复（向后兼容）

预发布版本：`MAJOR.MINOR.PATCH-alpha/beta/rc`

## 分支策略

- `main` - 主分支，受保护
- `feature/*` - 功能分支
- `fix/*` - 修复分支

## 提交规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关

---
