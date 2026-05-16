# 为算法Widget添加介绍按钮 - 快速指南

## 前提条件

1. 算法有对应的HTML介绍页面（位于 `resources/html/算法名/index.html`）
2. 算法Widget文件已存在（位于 `ui/widgets/`）

## 步骤

### 1. 导入组件

在Widget文件顶部添加导入：

```python
from ui.components.intro_button import AlgorithmIntroButton
from PyQt5.QtWidgets import QHBoxLayout  # 如果还没导入
```

### 2. 添加按钮到UI

在 `initUI()` 方法中，找到标题和描述部分，修改为：

**修改前：**
```python
# 标题
title = TitleLabel("算法名称")
layout.addWidget(title)

# 描述
desc = BodyLabel("算法描述...")
desc.setWordWrap(True)
layout.addWidget(desc)
```

**修改后：**
```python
# 标题
title = TitleLabel("算法名称")
layout.addWidget(title)

# 描述和介绍按钮
descLayout = QHBoxLayout()
desc = BodyLabel("算法描述...")
desc.setWordWrap(True)
descLayout.addWidget(desc, 1)

# 算法介绍按钮
self.introBtn = AlgorithmIntroButton("算法名称")
descLayout.addWidget(self.introBtn)

layout.addLayout(descLayout)
```

### 3. 更新算法名称映射（如果需要）

如果是新算法，需要在 `ui/components/intro_button.py` 中添加映射：

```python
name_map = {
    'AES': 'aes',
    'Caesar': 'caesar',
    # ... 其他映射 ...
    'YourAlgorithm': 'your_algorithm',  # 添加新映射
}
```

## 完整示例

以 AES Widget 为例：

```python
"""
AES 加密算法界面 - Fluent Design 版本
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import (
    ScrollArea, TitleLabel, BodyLabel,
    InfoBar, MessageBox
)

from ui.components.algorithm_card import KeyCard, EncryptCard, DecryptCard, LogCard
from ui.components.intro_button import AlgorithmIntroButton
from core.algorithms.symmetric.AES import Thread as AESThread
from infrastructure.converters import TypeConvert


class AESWidget(ScrollArea):
    """AES 加密算法界面"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("aesWidget")
        self.initUI()
        self.connectSignals()
    
    def initUI(self):
        """初始化UI"""
        self.view = QWidget()
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        
        layout = QVBoxLayout(self.view)
        layout.setSpacing(16)
        layout.setContentsMargins(36, 36, 36, 36)
        
        # 标题
        title = TitleLabel("AES 加密")
        layout.addWidget(title)
        
        # 描述和介绍按钮
        descLayout = QHBoxLayout()
        desc = BodyLabel(
            "AES (Advanced Encryption Standard) 是一种对称加密算法，"
            "使用128位密钥对128位数据块进行加密。输入格式为十六进制。"
        )
        desc.setWordWrap(True)
        descLayout.addWidget(desc, 1)
        
        # 算法介绍按钮
        self.introBtn = AlgorithmIntroButton("AES")
        descLayout.addWidget(self.introBtn)
        
        layout.addLayout(descLayout)
        
        # ... 其他卡片 ...
```

## 测试

运行以下命令测试：

```bash
python main.py
```

点击算法界面中的"算法介绍"按钮，应该会打开一个对话框显示HTML介绍页面。

## 批量检查

使用辅助脚本检查哪些算法可以添加介绍按钮：

```bash
python scripts/add_intro_buttons.py
```

## 常见问题

### Q: 点击按钮没有反应？
A: 检查HTML文件路径是否正确，确保 `resources/html/算法名/index.html` 存在。

### Q: 显示"暂无介绍"？
A: 说明该算法还没有HTML介绍页面，需要先创建HTML页面。

### Q: HTML页面样式错乱？
A: 检查HTML中的CSS、JS、图片等资源路径是否使用相对路径。

### Q: 数学公式不显示？
A: 确保HTML中包含MathJax CDN链接，并且有网络连接。

## 相关文档

- [HTML集成方案详细文档](../HTML_INTEGRATION.md)
- [组件开发指南](UI_COMPONENT_GUIDE.md)
- [开发指南](DEVELOPMENT_GUIDE.md)
