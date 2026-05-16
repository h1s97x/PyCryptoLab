# 快速打包指南

## 🚀 一键打包

双击运行 `build.bat`，等待3-5分钟即可完成打包。

## 📦 打包结果

打包完成后，你会得到：

```
dist/
├── 密码学平台/              # 可执行文件夹
│   ├── 密码学平台.exe       # 主程序
│   ├── resources/          # 资源文件
│   └── _internal/          # 依赖库
└── 密码学平台.zip           # 压缩包（用于分发）
```

## 📤 分发给用户

### 方式一：分享压缩包（推荐）

将 `dist/密码学平台.zip` 发送给用户：
- 文件大小：约 80-120 MB
- 用户解压后即可使用

### 方式二：分享文件夹

将整个 `dist/密码学平台/` 文件夹打包发送：
- 文件大小：约 200-300 MB
- 用户直接运行 exe 文件

## 📋 用户使用步骤

1. 解压 `密码学平台.zip`
2. 双击 `密码学平台.exe`
3. 开始使用（无需安装Python）

## ⚙️ 打包配置

如需修改打包配置，编辑 `build_config.spec`：

- **添加文件**: 修改 `datas` 列表
- **添加模块**: 修改 `hiddenimports` 列表
- **修改图标**: 设置 `icon` 参数
- **控制台窗口**: 修改 `console` 参数

## 🔧 故障排除

### 打包失败

```bash
# 清理后重试
rmdir /s /q build dist
pyinstaller build_config.spec --clean
```

### 缺少模块

在 `build_config.spec` 的 `hiddenimports` 中添加：

```python
hiddenimports = [
    'your_missing_module',
    ...
]
```

### 文件过大

使用虚拟环境打包：

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pyinstaller build_config.spec
```

## 📚 详细文档

- **打包指南**: `docs/BUILD_GUIDE.md`
- **用户指南**: `USER_GUIDE.md`
- **发布说明**: `RELEASE_README.md`

## ✅ 打包前检查清单

- [ ] 所有功能测试通过
- [ ] 更新版本号
- [ ] 更新 CHANGELOG.md
- [ ] 清理调试代码
- [ ] 准备发布文档

## 🎉 完成！

打包完成后，你可以：

1. 测试运行 `dist/密码学平台/密码学平台.exe`
2. 将 `密码学平台.zip` 分享给用户
3. 上传到 GitHub Releases

---

**提示**: 首次打包可能需要较长时间，后续打包会更快。
