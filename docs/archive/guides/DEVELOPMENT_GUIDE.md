# 开发指南

本指南帮助开发者快速上手项目开发。

---

## 环境配置

### 系统要求

- Python 3.8+
- PyQt5
- Windows/Linux/macOS

### 安装依赖

```bash
# 克隆项目
git clone <repository-url>
cd Cryptogrphy

# 安装依赖
pip install -r requirements.txt
```

### 运行项目

```bash
# 运行主程序
python main.py

# 运行测试
python tests/test_all_widgets.py
```

---

## 项目结构

```
Cryptogrphy/
├── core/                   # 核心算法
│   └── algorithms/
│       ├── classical/      # 古典密码
│       ├── symmetric/      # 对称加密
│       ├── asymmetric/     # 非对称加密
│       ├── hash/           # 哈希算法
│       └── mathematical/   # 数学基础
│
├── ui/                     # 用户界面
│   ├── widgets/            # UI组件
│   └── main_window.py      # 主窗口
│
├── infrastructure/         # 基础设施
│   ├── converters/         # 类型转换
│   ├── security/           # 安全工具
│   └── Path.py             # 路径管理
│
├── tests/                  # 测试文件
├── scripts/                # 工具脚本
├── docs/                   # 文档
└── resources/              # 资源文件
```

---

## 开发流程

### 1. 创建分支

```bash
# 从develop分支创建功能分支
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### 2. 开发功能

- 遵循代码规范
- 编写测试
- 更新文档

### 3. 提交代码

```bash
# 添加文件
git add .

# 提交（遵循提交规范）
git commit -m "feat: 添加新功能"

# 推送
git push origin feature/your-feature-name
```

### 4. 创建PR

- 在GitHub/GitLab创建Pull Request
- 等待代码审查
- 合并到develop分支

---

## 代码规范

### Git提交规范

使用语义化提交信息：

```
<type>: <subject>

<body>
```

**Type类型**：
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关

**示例**：
```
feat: 添加AES加密算法

- 实现AES-128/192/256
- 支持ECB/CBC/CFB模式
- 添加单元测试
```

### Python代码规范

遵循PEP 8规范：

```python
# 好的示例
class CaesarWidget(CryptographyWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Caesar Cipher")
        
    def encrypt(self):
        """加密方法"""
        plaintext = self.widgets_dict["Plaintext"].get_text()
        # 加密逻辑...
```

### UI组件规范

使用配置驱动模式：

```python
self.groups_config = [
    KeyGroup(
        name="Key",
        key_edit=[Key(id="Key", label="Key", default_text="")],
        combo_box=[],
        buttons=[]
    ),
    Group(
        name="Encrypt",
        plain_text_edits=[
            PlainTextEdit(id="Plaintext", label="Plaintext", default_text=""),
            PlainTextEdit(id="Ciphertext", label="Ciphertext", default_text="", read_only=True)
        ],
        buttons=[
            Button(id="Encrypt", name="Encrypt", clicked_function=self.encrypt)
        ]
    )
]
self.render()
```

---

## 测试指南

### 运行测试

```bash
# 运行所有测试
python tests/test_all_widgets.py

# 运行特定测试
python tests/test_caesar_widget.py
```

### 编写测试

```python
def test_widget():
    """测试组件"""
    from ui.widgets.Caesar_ui import CaesarWidget
    
    widget = CaesarWidget()
    assert widget.windowTitle() == "Caesar Cipher"
    assert len(widget.widgets_dict) > 0
```

---

## 常见任务

### 添加新的加密算法

1. 在 `core/algorithms/` 创建算法文件
2. 在 `ui/widgets/` 创建UI组件
3. 在 `ui/widgets/__init__.py` 导出组件
4. 在 `ui/main_window.py` 添加菜单项
5. 编写测试
6. 更新文档

### 修复Bug

1. 创建Issue描述问题
2. 创建bugfix分支
3. 修复问题并添加测试
4. 提交PR

### 更新文档

1. 修改相应的Markdown文件
2. 更新 `docs/README.md` 导航
3. 提交文档更新

---

## 工具和脚本

### 批量更新脚本

```bash
# 批量更新UI组件
python scripts/batch_update_widgets.py
```

### 语法修复脚本

```bash
# 修复语法错误
python scripts/fix_syntax_errors.py
```

### 测试脚本

```bash
# 快速测试
python tests/quick_test.py

# 批量测试
python tests/test_all_widgets.py
```

---

## 调试技巧

### 使用日志

```python
# 在组件中使用日志
self.log_message("调试信息")
self.logging_error(exception)
```

### 使用断点

```python
# 在代码中添加断点
import pdb; pdb.set_trace()
```

### 查看组件状态

```python
# 打印widgets_dict
print(self.widgets_dict.keys())

# 检查组件值
print(self.widgets_dict["Key"].text())
```

---

## 性能优化

### 测量性能

```python
import time

start = time.time()
# 你的代码
end = time.time()
print(f"耗时: {end - start}秒")
```

### 优化建议

1. 使用延迟导入
2. 避免重复计算
3. 使用缓存
4. 优化算法复杂度

---

## 常见问题

### Q: 如何添加新的UI组件？

A: 参考 [UI组件开发指南](UI_COMPONENT_GUIDE.md)

### Q: 测试失败怎么办？

A: 
1. 查看错误信息
2. 检查导入路径
3. 验证组件配置
4. 运行单个测试定位问题

### Q: 如何更新文档？

A:
1. 修改对应的Markdown文件
2. 遵循Markdown格式
3. 更新文档导航
4. 提交PR

---

## 参考资料

- [系统架构](../ARCHITECTURE.md)
- [UI组件指南](UI_COMPONENT_GUIDE.md)
- [技术路线图](../ROADMAP.md)
- [变更日志](../CHANGELOG.md)

---

## 获取帮助

- 查看文档：`docs/`
- 提交Issue
- 联系维护者

---

**最后更新**：2026-03-04  
**维护者**：开发团队
