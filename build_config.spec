# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 收集所有需要的数据文件
datas = [
    ('resources', 'resources'),  # 包含HTML和数据文件
    ('ui', 'ui'),  # UI组件
    ('core', 'core'),  # 核心算法
    ('infrastructure', 'infrastructure'),  # 基础设施
]

# 隐藏导入（PyInstaller可能检测不到的模块）
hiddenimports = [
    'PyQt5.QtWebEngineWidgets',
    'qfluentwidgets',
    'cryptography',
    'Crypto',
    'gmpy2',
    'ecdsa',
    'gmssl',
    'gmssl.sm2',
    'gmssl.func',
    # 所有算法模块
    'core.algorithms.classical',
    'core.algorithms.symmetric',
    'core.algorithms.asymmetric',
    'core.algorithms.hash',
    'core.algorithms.mathematical',
    # 所有UI组件
    'ui.components',
    'ui.interfaces',
    'ui.widgets',
    'ui.widgets.protocols',
    'ui.widgets.seal_widget',
    'ui.widgets.zuc_widget',
    'ui.widgets.crypto1_widget',
    'ui.widgets.ecc_widget',
    'ui.widgets.sm2_widget',
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='密码学平台',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可以添加图标文件路径
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='密码学平台',
)
