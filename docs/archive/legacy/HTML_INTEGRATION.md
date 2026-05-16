# HTML 算法介绍页面集成方案

## 概述

本文档说明如何将 `resources/html/` 目录下的算法介绍HTML页面集成到密码学平台中。

## 实现方案

### 1. 技术选型

使用 **PyQt5 的 QWebEngineView** 组件来渲染HTML页面，优势：
- 完整支持HTML5、CSS3、JavaScript
- 支持MathJax数学公式渲染
- 支持本地资源加载（CSS、JS、图片）
- 与Fluent UI无缝集成

### 2. 组件架构

#### 2.1 AlgorithmIntroButton (算法介绍按钮)
- 位置：`ui/components/intro_button.py`
- 功能：在算法Widget中添加"算法介绍"按钮
- 特性：
  - 自动映射算法名称到HTML目录
  - 检查HTML文件是否存在
  - 点击打开全屏对话框显示HTML

#### 2.2 AlgorithmIntroDialog (算法介绍对话框)
- 位置：`ui/components/intro_button.py`
- 功能：全屏显示HTML介绍页面
- 特性：
  - 1200x800 默认尺寸
  - 使用QWebEngineView渲染
  - 支持本地资源路径

### 3. 使用方法

#### 3.1 在Widget中添加介绍按钮

```python
from ui.components.intro_button import AlgorithmIntroButton

class YourAlgorithmWidget(ScrollArea):
    def initUI(self):
        # ... 其他UI代码 ...
        
        # 添加算法介绍按钮
        self.introBtn = AlgorithmIntroButton("AES")  # 传入算法名称
        layout.addWidget(self.introBtn)
```

#### 3.2 支持的算法列表

当前已有HTML介绍页面的算法：
- AES (`resources/html/aes/`)
- Caesar (`resources/html/caesar/`)
- DES (`resources/html/des/`)
- Hill (`resources/html/hill/`)
- MD5 (`resources/html/md5/`)
- SM4 (`resources/html/sm4/`)
- Vigenere (`resources/html/vigenere/`)

### 4. 添加新算法介绍

#### 4.1 准备HTML文件

在 `resources/html/` 下创建新目录，结构如下：

```
resources/html/your_algorithm/
├── index.html          # 主HTML文件
├── css/
│   ├── style.css
│   └── prettify.css
├── js/
│   └── ...
└── images/
    └── ...
```

#### 4.2 更新算法名称映射

编辑 `ui/components/intro_button.py`，在 `_getHTMLPath()` 方法中添加映射：

```python
name_map = {
    'AES': 'aes',
    'Caesar': 'caesar',
    # ... 其他映射 ...
    'YourAlgorithm': 'your_algorithm',  # 添加新映射
}
```

#### 4.3 在Widget中使用

```python
self.introBtn = AlgorithmIntroButton("YourAlgorithm")
```

### 5. HTML页面特性

#### 5.1 支持的功能
- ✅ 完整的HTML5/CSS3渲染
- ✅ JavaScript执行
- ✅ MathJax数学公式（通过CDN）
- ✅ 本地图片、CSS、JS资源
- ✅ 页面内导航（锚点链接）
- ✅ 响应式布局

#### 5.2 资源路径处理
- HTML使用相对路径引用资源（`css/style.css`, `images/xxx.png`）
- QWebEngineView使用 `QUrl.fromLocalFile()` 加载，自动处理相对路径

### 6. 示例：AES Widget集成

```python
class AESWidget(ScrollArea):
    def initUI(self):
        layout = QVBoxLayout(self.view)
        
        # 标题
        title = TitleLabel("AES 加密")
        layout.addWidget(title)
        
        # 描述和介绍按钮
        descLayout = QHBoxLayout()
        desc = BodyLabel("AES 算法描述...")
        desc.setWordWrap(True)
        descLayout.addWidget(desc, 1)
        
        # 算法介绍按钮
        self.introBtn = AlgorithmIntroButton("AES")
        descLayout.addWidget(self.introBtn)
        
        layout.addLayout(descLayout)
        
        # ... 其他卡片 ...
```

### 7. 待完成任务

- [ ] 为所有28个算法Widget添加介绍按钮
- [ ] 为没有HTML页面的算法创建介绍页面
- [ ] 统一HTML页面样式（可选）
- [ ] 添加深色主题支持（可选）

### 8. 技术细节

#### 8.1 依赖项
- PyQt5
- PyQtWebEngine (必需)

安装命令：
```bash
pip install PyQtWebEngine
```

或使用核心依赖文件：
```bash
pip install -r requirements_core.txt
```

**重要提示**：
- PyQtWebEngine 必须在创建 QApplication 之前导入
- 如果未安装，点击"算法介绍"按钮会显示友好的错误提示
- main.py 已自动处理导入顺序

#### 8.2 路径解析
- 使用 `Path` 对象处理路径
- 使用 `absolute()` 获取绝对路径
- 使用 `QUrl.fromLocalFile()` 转换为URL

#### 8.3 错误处理
- 检查HTML文件是否存在
- 文件不存在时显示友好提示
- 使用InfoBar提示用户

## 总结

通过 `AlgorithmIntroButton` 组件，可以轻松为任何算法Widget添加HTML介绍页面支持。该方案：
- 简单易用（一行代码添加按钮）
- 扩展性强（支持任意算法）
- 用户体验好（全屏对话框显示）
- 维护成本低（HTML页面独立管理）
