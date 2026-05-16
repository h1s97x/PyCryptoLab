# QFluentWidgets 快速开始指南

## 安装

### 1. 安装 QFluentWidgets

```bash
pip install PyQt-Fluent-Widgets
```

或者使用 requirements.txt：

```bash
pip install -r requirements.txt
```

### 2. 验证安装

```python
python -c "from qfluentwidgets import FluentWindow; print('安装成功!')"
```

## 运行新UI

### 启动 Fluent Design 版本

```bash
python main_fluent.py
```

### 启动经典版本（原版）

```bash
python main.py
```

## 项目结构

```
ui/
├── fluent/                      # 新的 Fluent Design UI
│   ├── main_window.py          # 主窗口（带导航）
│   ├── components/             # 可复用组件
│   │   └── algorithm_card.py   # 算法卡片组件
│   ├── interfaces/             # 界面
│   │   ├── home_interface.py   # 首页
│   │   └── settings_interface.py # 设置页
│   └── widgets/                # 算法界面
│       ├── hill_widget.py      # Hill算法（完整实现）
│       ├── caesar_widget.py    # Caesar算法（待实现）
│       └── ...
└── (原有UI代码保持不变)
```

## 功能特性

### 已实现

✅ Fluent Design 风格主窗口
✅ 侧边栏导航（支持分类和子项）
✅ 首页仪表板
✅ 设置页面（主题切换）
✅ Hill 算法完整界面
✅ 可复用的卡片组件
✅ 日志系统
✅ 深色/浅色主题自动切换

### 待实现

⏳ 其他算法界面迁移
⏳ 搜索功能
⏳ 收藏功能
⏳ 历史记录
⏳ 拖拽文件支持
⏳ 键盘快捷键

## 核心组件使用

### 1. 算法界面基础结构

```python
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import ScrollArea, TitleLabel, BodyLabel
from ui.components.algorithm_card import KeyCard, EncryptCard, DecryptCard, LogCard

class MyAlgorithmWidget(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        self.view = QWidget()
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        
        layout = QVBoxLayout(self.view)
        layout.setContentsMargins(36, 36, 36, 36)
        
        # 标题
        title = TitleLabel("算法名称")
        layout.addWidget(title)
        
        # 描述
        desc = BodyLabel("算法描述...")
        layout.addWidget(desc)
        
        # 密钥卡片
        self.keyCard = KeyCard()
        layout.addWidget(self.keyCard)
        
        # 加密卡片
        self.encryptCard = EncryptCard()
        layout.addWidget(self.encryptCard)
        
        # 解密卡片
        self.decryptCard = DecryptCard()
        layout.addWidget(self.decryptCard)
        
        # 日志卡片
        self.logCard = LogCard()
        layout.addWidget(self.logCard)
```

### 2. 使用卡片组件

#### KeyCard（密钥配置）

```python
# 获取密钥
key = self.keyCard.getKey()

# 设置密钥
self.keyCard.setKey("your key here")

# 连接按钮信号
self.keyCard.generateBtn.clicked.connect(self.generateKey)
self.keyCard.importBtn.clicked.connect(self.importKey)
```

#### EncryptCard（加密）

```python
# 获取明文
plaintext = self.encryptCard.getPlaintext()

# 设置密文
self.encryptCard.setCiphertext("encrypted text")

# 清空密文
self.encryptCard.clear()

# 连接按钮
self.encryptCard.encryptBtn.clicked.connect(self.encrypt)
self.encryptCard.copyBtn.clicked.connect(self.copy)
```

#### DecryptCard（解密）

```python
# 获取密文
ciphertext = self.decryptCard.getCiphertext()

# 设置明文
self.decryptCard.setPlaintext("decrypted text")

# 连接按钮
self.decryptCard.decryptBtn.clicked.connect(self.decrypt)
```

#### LogCard（日志）

```python
# 添加不同级别的日志
self.logCard.log("普通信息", "info")
self.logCard.log("成功消息", "success")
self.logCard.log("警告信息", "warning")
self.logCard.log("错误信息", "error")

# 清空日志
self.logCard.clear()
```

### 3. 消息提示

```python
from qfluentwidgets import InfoBar, MessageBox

# 成功提示
InfoBar.success(
    title="成功",
    content="操作成功完成",
    parent=self
)

# 错误提示
InfoBar.error(
    title="错误",
    content="操作失败",
    parent=self
)

# 警告提示
InfoBar.warning(
    title="警告",
    content="请注意",
    parent=self
)

# 消息框
MessageBox("标题", "内容", self).exec()
```

### 4. 主题切换

```python
from qfluentwidgets import Theme, setTheme

# 设置浅色主题
setTheme(Theme.LIGHT)

# 设置深色主题
setTheme(Theme.DARK)

# 自动跟随系统
setTheme(Theme.AUTO)
```

## 迁移现有算法界面

### 步骤1: 创建新文件

在 `ui/fluent/widgets/` 目录下创建新文件，例如 `caesar_widget.py`

### 步骤2: 使用模板

```python
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import ScrollArea, TitleLabel, BodyLabel
from ui.components.algorithm_card import KeyCard, EncryptCard, DecryptCard, LogCard

class CaesarWidget(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("caesarWidget")
        self.initUI()
        self.connectSignals()
    
    def initUI(self):
        # ... 参考 hill_widget.py
        pass
    
    def connectSignals(self):
        # ... 连接信号
        pass
    
    def encrypt(self):
        # ... 加密逻辑（复用原有算法代码）
        pass
    
    def decrypt(self):
        # ... 解密逻辑（复用原有算法代码）
        pass
```

### 步骤3: 注册到主窗口

在 `ui/fluent/main_window.py` 中添加：

```python
from ui.widgets.caesar_widget import CaesarWidget

# 在 addClassicalCrypto 方法中添加
self.caesarWidget = CaesarWidget(self)
self.addSubInterface(
    self.caesarWidget,
    FIF.DOCUMENT,
    'Caesar',
    parent=self.navigationInterface.widget('classical')
)
```

## 常见问题

### Q: 如何保持原有算法逻辑不变？

A: 只需要改变UI层，算法实现代码（`core/algorithms/`）完全不需要修改。在新UI中导入原有的算法类即可。

### Q: 新旧UI可以共存吗？

A: 可以！`main.py` 运行原版UI，`main_fluent.py` 运行新版UI，互不影响。

### Q: 如何自定义主题色？

A: 使用 `setThemeColor`：

```python
from qfluentwidgets import setThemeColor
from PyQt5.QtGui import QColor

setThemeColor(QColor(37, 99, 235))  # 自定义蓝色
```

### Q: 组件样式如何调整？

A: QFluentWidgets 支持 QSS 样式表，可以通过 `setStyleSheet` 自定义。

### Q: 如何添加新的导航分类？

A: 在 `main_window.py` 中添加：

```python
self.navigationInterface.addItem(
    routeKey='your_category',
    icon=FIF.YOUR_ICON,
    text='分类名称',
    onClick=lambda: None,
    selectable=False,
    position=NavigationItemPosition.TOP
)
```

## 开发建议

1. **先完成一个算法界面**：以 Hill 为模板，完整实现一个算法
2. **提取通用逻辑**：将重复代码提取到基类或工具函数
3. **保持一致性**：使用统一的组件和交互模式
4. **测试功能**：确保加密解密功能正常
5. **优化体验**：添加加载动画、错误提示等

## 参考资源

- [QFluentWidgets 官方文档](https://qfluentwidgets.com/)
- [组件库示例](https://qfluentwidgets.com/zh/components)
- [GitHub 示例代码](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/tree/master/examples)
- Hill 算法完整实现：`ui/fluent/widgets/hill_widget.py`

## 下一步

1. 运行 `python main_fluent.py` 查看效果
2. 测试 Hill 算法的加密解密功能
3. 参考 Hill 实现，迁移其他算法
4. 根据需要自定义主题和样式
