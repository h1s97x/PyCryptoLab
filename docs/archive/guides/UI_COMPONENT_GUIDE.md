# UI组件迁移指南

## 概述

本指南说明如何将旧的UI组件迁移到新的配置驱动模式，使用`CryptographyWidget`基类的`render()`方法。

## 迁移步骤

### 1. 更新导入语句

**旧方式**：
```python
from ui.main_window import Button, PlainTextEdit, Group, ErrorType
from ui.main_window import CryptographyWidget
```

**新方式**：
```python
from ui.main_window import Button, PlainTextEdit, Group, ErrorType, KeyGroup, Key
from ui.main_window import CryptographyWidget
```

### 2. 更新初始化方法

**旧方式**：
```python
def __init__(self):
    CryptographyWidget.__init__(self)
    self.widgets_dict = {}
    self.setWindowTitle("Caesar")
```

**新方式**：
```python
def __init__(self):
    super().__init__()
    self.setWindowTitle("Caesar Cipher")
```

说明：
- 使用`super().__init__()`替代旧式初始化
- 不需要手动初始化`widgets_dict`（基类已处理）

### 3. 配置UI组件

#### 3.1 使用KeyGroup配置密钥输入

**旧方式**（使用Group + PlainTextEdit）：
```python
Group(
    name="Key",
    plain_text_edits=[PlainTextEdit(id="Key", label="Key (Int)", default_text="3")],
    buttons=[]
)
```

**新方式**（使用KeyGroup + Key）：
```python
KeyGroup(
    name="Key",
    key_edit=[Key(id="Key", label="Key (Int)", default_text="3", enabled=True)],
    combo_box=[],
    buttons=[]
)
```

说明：
- `KeyGroup`使用`QLineEdit`而不是`QTextEdit`
- 更适合单行输入（如密钥、参数）
- 获取值时使用`.text()`而不是`.get_text()`

#### 3.2 配置普通文本区域

```python
Group(
    name="Encrypt",
    plain_text_edits=[
        PlainTextEdit(id="Plaintext", label="Plaintext", default_text="Hello"),
        PlainTextEdit(id="Ciphertext", label="Ciphertext", default_text="", read_only=True)
    ],
    buttons=[
        Button(id="Encrypt", name="Encrypt", clicked_function=self.encrypt),
        Button(id="Clean", name="Clean", clicked_function=self.clean)
    ]
)
```

### 4. 调用render()方法

```python
# 配置完成后调用render
self.render()
self.log_message("Component initialized.")
```

### 5. 更新日志记录

**旧方式**：
```python
self.logging.log("Message")
self.logging.log_error(error)
```

**新方式**：
```python
self.log_message("Message")
self.logging_error(error)
```

### 6. 获取组件值

#### KeyGroup中的QLineEdit

**新方式**：
```python
key = self.widgets_dict["Key"].text()  # QLineEdit使用text()
```

#### Group中的TextEdit

```python
plaintext = self.widgets_dict["Plaintext"].get_text()  # TextEdit使用get_text()
```

## 完整示例

### 迁移前（旧方式）

```python
class CaesarWidget(CryptographyWidget):
    def __init__(self):
        CryptographyWidget.__init__(self)
        self.menuBar().setHidden(True)
        self.setWindowTitle("Caesar")
        self.widgets_dict = {}
        
        # 手动创建UI组件
        layout = QVBoxLayout()
        
        # Key输入
        key_label = QLabel("Key (Int)")
        self.key_edit = QLineEdit("3")
        layout.addWidget(key_label)
        layout.addWidget(self.key_edit)
        
        # Plaintext输入
        plaintext_label = QLabel("Plaintext")
        self.plaintext_edit = QTextEdit("Hello")
        layout.addWidget(plaintext_label)
        layout.addWidget(self.plaintext_edit)
        
        # 按钮
        encrypt_button = QPushButton("Encrypt")
        encrypt_button.clicked.connect(self.encrypt)
        layout.addWidget(encrypt_button)
        
        # 设置布局
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        self.logging.log("Caesar loaded.\n")
```

### 迁移后（新方式）

```python
class CaesarWidget(CryptographyWidget):
    def __init__(self):
        super().__init__()
        self.menuBar().setHidden(True)
        self.setWindowTitle("Caesar Cipher")
        
        # 配置UI组件
        self.groups_config = [
            KeyGroup(
                name="Key",
                key_edit=[Key(id="Key", label="Key (Int)", default_text="3", enabled=True)],
                combo_box=[],
                buttons=[]
            ),
            Group(
                name="Encrypt",
                plain_text_edits=[
                    PlainTextEdit(id="Plaintext", label="Plaintext", default_text="Hello"),
                    PlainTextEdit(id="Ciphertext", label="Ciphertext", default_text="", read_only=True)
                ],
                buttons=[
                    Button(id="Encrypt", name="Encrypt", clicked_function=self.encrypt),
                    Button(id="Clean", name="Clean", clicked_function=self.clean)
                ]
            )
        ]
        
        # 渲染UI
        self.render()
        self.log_message("Caesar Cipher loaded.\n")
    
    def encrypt(self):
        """加密方法"""
        key = self.widgets_dict["Key"].text()  # QLineEdit使用text()
        plaintext = self.widgets_dict["Plaintext"].get_text()  # TextEdit使用get_text()
        
        # 加密逻辑...
        ciphertext = self.do_encrypt(plaintext, key)
        
        self.widgets_dict["Ciphertext"].set_text(ciphertext)
        self.log_message(f"Encrypted: {ciphertext}")
```

## 优势对比

### 代码行数

- 旧方式：~150行（手动创建UI）
- 新方式：~80行（配置驱动）
- 减少：~47%

### 可维护性

- ✅ 统一的UI风格
- ✅ 减少重复代码
- ✅ 更容易理解和修改
- ✅ 自动处理布局和样式

### 功能完整性

- ✅ 自动添加日志组件
- ✅ 自动管理widgets_dict
- ✅ 统一的窗口尺寸和样式
- ✅ 更好的错误处理

## 常见问题

### Q1: 如何处理ComboBox？

```python
KeyGroup(
    name="Options",
    key_edit=[],
    combo_box=[
        ComboBox(
            enabled=True,
            id="Mode",
            label="Mode",
            items=["ECB", "CBC", "CFB"],
            changed_function=self.on_mode_changed
        )
    ],
    buttons=[]
)
```

### Q2: 如何处理按钮ID冲突？

确保每个按钮有唯一的ID：

```python
buttons=[
    Button(id="ImportFile1", name="Import File", clicked_function=self.import_plaintext),
    Button(id="ImportFile2", name="Import File", clicked_function=self.import_ciphertext)
]
```

### Q3: 如何禁用某个输入框？

```python
Key(id="Key", label="Key", default_text="", enabled=False)
```

### Q4: 如何设置只读文本框？

```python
PlainTextEdit(id="Output", label="Output", default_text="", read_only=True)
```

## 迁移检查清单

- [ ] 更新导入语句（添加KeyGroup, Key）
- [ ] 使用super().__init__()
- [ ] 移除手动初始化widgets_dict
- [ ] 使用KeyGroup配置密钥输入
- [ ] 使用Group配置文本区域
- [ ] 调用self.render()
- [ ] 更新日志记录方法（log_message）
- [ ] 更新获取值的方法（text() vs get_text()）
- [ ] 确保按钮ID唯一
- [ ] 测试组件功能

## 下一步

完成迁移后：

1. 运行测试确保功能正常
2. 检查UI显示是否正确
3. 验证所有按钮和输入框工作正常
4. 提交代码并更新文档

## 参考

- `ui/main_window.py` - 基类实现
- `ui/widgets/Caesar_ui.py` - 完整示例
- `tests/test_render.py` - 单元测试
- `tests/test_caesar_widget.py` - 集成测试
- `docs/UI_RENDER_OPTIMIZATION.md` - 优化文档

---

**文档版本**：v1.0  
**最后更新**：2026-03-04  
**适用范围**：所有UI组件迁移
