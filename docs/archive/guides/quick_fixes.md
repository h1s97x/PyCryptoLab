# 快速修复指南

## 1. 安装缺失的依赖

```bash
# 安装 pycryptodome (替代 Crypto)
pip install pycryptodome

# 或者如果已经安装了 crypto，卸载后重装
pip uninstall crypto pycrypto
pip install pycryptodome
```

## 2. 验证安装

```bash
python -c "from Crypto.PublicKey import ECC; print('Crypto模块安装成功')"
```

## 3. 运行完整测试

```bash
# 运行项目结构和基础测试
python test_project.py

# 运行算法功能测试
python test_algorithms.py
```

## 4. 启动应用

```bash
# 启动GUI应用
python main.py
```

## 已知问题和解决方案

### 问题1: Vigenere密码方法签名不匹配
**文件**: `core/algorithms/classical/Vigenere.py`
**症状**: `Thread.encrypt() takes 1 positional argument but 3 were given`
**解决**: 需要检查 Thread 类的 encrypt 和 decrypt 方法，确保它们接受 plaintext 和 key 参数

### 问题2: ECC模块缺少Crypto依赖
**文件**: `core/algorithms/asymmetric/ECC.py`
**症状**: `No module named 'Crypto'`
**解决**: 运行 `pip install pycryptodome`

### 问题3: UI组件导入问题
**文件**: `ui/widgets/__init__.py`
**症状**: `cannot import name 'classical' from 'ui.widgets'`
**解决**: 检查 __init__.py 是否正确导出了 classical 模块

## 测试结果摘要

✓ **工作正常的模块**:
- 凯撒密码 (Caesar)
- AES, DES, SM4 (对称加密)
- MD5, SHA1, SHA256, SM3 (哈希算法)
- RSA, SM2 (非对称加密)
- 主窗口 (Main Window)

✗ **需要修复的模块**:
- 维吉尼亚密码 (Vigenere) - 方法签名问题
- ECC - 依赖问题
- UI widgets - 导入配置问题

## 下一步建议

1. 先安装 pycryptodome 解决依赖问题
2. 修复 Vigenere.py 的方法签名
3. 完善 UI widgets 的 __init__.py
4. 运行完整测试验证所有功能
5. 启动 GUI 应用进行手动测试
