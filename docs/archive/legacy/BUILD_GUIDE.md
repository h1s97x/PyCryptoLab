# 应用打包指南

本文档说明如何将密码学平台打包成可执行应用，方便分发给其他用户。

## 打包方式

### 方式一：使用打包脚本（推荐）

1. 双击运行 `build.bat`
2. 等待打包完成（约3-5分钟）
3. 在 `dist/密码学平台/` 目录找到可执行文件

### 方式二：手动打包

```bash
# 清理旧文件
rmdir /s /q build dist

# 打包应用
pyinstaller build_config.spec --clean

# 测试运行
cd dist/密码学平台
密码学平台.exe
```

## 打包配置说明

### build_config.spec

打包配置文件，包含以下设置：

- **datas**: 需要包含的数据文件
  - `resources/` - HTML介绍页面和数据文件
  - `ui/` - UI组件
  - `core/` - 核心算法
  - `infrastructure/` - 基础设施

- **hiddenimports**: 隐藏导入的模块
  - PyQt5、QFluentWidgets
  - 密码学库（cryptography, pycryptodome）
  - 所有算法和UI模块

- **console**: False - 不显示控制台窗口

## 打包结果

### 文件结构

```
dist/密码学平台/
├── 密码学平台.exe          # 主程序
├── resources/              # 资源文件
│   ├── html/              # HTML介绍页面
│   └── data/              # 数据文件
├── _internal/             # 依赖库和模块
└── ...其他依赖文件
```

### 文件大小

- 完整应用：约 200-300 MB
- 压缩后：约 80-120 MB

## 分发方式

### 方式一：文件夹分发

将整个 `dist/密码学平台/` 文件夹打包成 ZIP：

```bash
# 自动创建（build.bat已包含）
cd dist
powershell -command "Compress-Archive -Path '密码学平台' -DestinationPath '密码学平台.zip'"
```

### 方式二：安装程序（可选）

使用 Inno Setup 或 NSIS 创建安装程序：

1. 下载 Inno Setup: https://jrsoftware.org/isinfo.php
2. 创建安装脚本
3. 生成 setup.exe

## 用户使用说明

### 系统要求

- Windows 10/11 (64位)
- 无需安装Python
- 无需安装依赖库

### 运行方式

1. 解压 `密码学平台.zip`
2. 双击 `密码学平台.exe`
3. 开始使用

### 首次运行

- 首次启动可能需要10-20秒
- Windows Defender 可能会扫描（正常现象）
- 如果被杀毒软件拦截，添加到白名单

## 常见问题

### Q1: 打包失败

**原因**: 缺少依赖或路径问题

**解决**:
```bash
# 重新安装依赖
pip install -r requirements.txt

# 清理后重新打包
rmdir /s /q build dist
pyinstaller build_config.spec --clean
```

### Q2: 运行时缺少模块

**原因**: hiddenimports 配置不完整

**解决**: 在 `build_config.spec` 的 `hiddenimports` 中添加缺失的模块

### Q3: 文件过大

**原因**: 包含了不必要的依赖

**解决**:
- 使用虚拟环境打包
- 只安装必需的依赖
- 使用 UPX 压缩

### Q4: 杀毒软件误报

**原因**: PyInstaller 打包的程序可能被误判

**解决**:
- 添加到杀毒软件白名单
- 使用代码签名证书
- 向杀毒软件厂商报告误报

## 优化建议

### 减小文件大小

1. **使用虚拟环境**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pyinstaller build_config.spec
```

2. **排除不必要的模块**
```python
# 在 build_config.spec 中添加
excludes=['matplotlib', 'numpy.testing', ...]
```

3. **使用 UPX 压缩**
```python
# 已在配置中启用
upx=True
```

### 提升启动速度

1. **使用 --onefile 模式**（不推荐，会更慢）
2. **优化导入**（延迟导入）
3. **预编译 Python 文件**

### 添加应用图标

1. 准备 `.ico` 文件（256x256）
2. 修改 `build_config.spec`:
```python
icon='resources/icon.ico'
```

## 发布清单

打包前检查：

- [ ] 所有功能测试通过
- [ ] 更新版本号
- [ ] 更新 CHANGELOG.md
- [ ] 清理调试代码
- [ ] 测试打包后的应用

发布时包含：

- [ ] 可执行文件（ZIP）
- [ ] README.md（使用说明）
- [ ] LICENSE（许可证）
- [ ] CHANGELOG.md（更新日志）

## 自动化打包

### GitHub Actions（可选）

创建 `.github/workflows/build.yml`:

```yaml
name: Build Application

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: pip install pyinstaller
      - run: pyinstaller build_config.spec
      - uses: actions/upload-artifact@v2
        with:
          name: 密码学平台
          path: dist/密码学平台/
```

## 技术支持

如有问题，请：

1. 查看本文档的常见问题
2. 检查 PyInstaller 文档
3. 提交 Issue 到项目仓库

---

**最后更新**: 2026-03-05  
**PyInstaller 版本**: 6.12.0  
**Python 版本**: 3.9+
