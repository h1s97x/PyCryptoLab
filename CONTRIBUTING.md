# 贡献指南

感谢您对密码学平台的关注！本文档将帮助您了解如何为项目做出贡献。

## 行为准则

参与本项目即表示您同意遵守我们的行为准则。请确保：

- 尊重他人，保持友好和专业
- 建设性地接受批评
- 专注于对社区最有利的事情
- 对其他社区成员表现出同理心

## 开发环境

### 环境要求

- Python 3.8+
- Git
- 支持 Windows/macOS/Linux

### 安装步骤

1. Fork 仓库

2. 克隆您的 Fork

```bash
git clone https://github.com/YOUR_USERNAME/PyCryptoLab.git
cd PyCryptoLab
```

3. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows
```

4. 安装依赖

```bash
pip install -r requirements.txt
pip install pytest pytest-cov flake8 gmssl
```

5. 验证安装

```bash
python main.py
```

## 分支策略

```
main (保护分支)
  ├── feature/xxx     # 新功能
  ├── fix/xxx         # Bug 修复
  ├── docs/xxx        # 文档更新
  └── refactor/xxx    # 重构
```

### 规则

- ❌ 禁止直接推送 `main` 分支
- ❌ 禁止强制推送 `main` 分支 (`git push --force`)
- ✅ 所有更改通过 Pull Request
- ✅ PR 必须通过 CI 检查
- ✅ 必须有 Code Review

## 开发流程

### 1. 创建分支

```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

### 2. 开发

```bash
# 进行代码更改
# 确保运行测试
pytest tests/unit/ -v
flake8 .
```

### 3. 提交

```bash
git add .
git commit -m "feat: add new algorithm widget"
```

#### 提交消息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

**示例**

```
feat(asymmetric): add SM2 digital signature widget

Implement SM2 signature algorithm with:
- Key generation
- Message signing
- Signature verification

Closes #123
```

#### 类型 (Type)

| 类型 | 说明 |
|------|------|
| feat | 新功能 |
| fix | Bug 修复 |
| docs | 文档更新 |
| style | 代码格式调整 |
| refactor | 代码重构 |
| test | 测试相关 |
| chore | 构建/工具相关 |

### 4. 推送并创建 PR

```bash
git push origin feature/your-feature-name
```

在 GitHub 上创建 Pull Request。

#### PR 模板

```markdown
## 变更内容

描述本次变更...

## 类型

- [ ] 新功能 (feat)
- [ ] Bug 修复 (fix)
- [ ] 文档更新 (docs)

## 测试

- [ ] 单元测试通过
- [ ] 本地测试通过

## 截图 (如有 UI 变更)
```

### 5. Code Review

- 等待维护者 Review
- 根据反馈进行修改
- 获得 Approval 后合并

## 代码规范

### Python

- 遵循 [PEP 8](https://pep8.org/)
- 最大行长度: 127 字符
- 使用 type hints（推荐）
- 注释使用英文或中文（与现有代码一致）

### Widget 开发

参考现有 Widget 结构：

```python
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import ...

from core.algorithms.xxx import AlgorithmThread
from infrastructure.Converters import TypeConvert


class AlgorithmWidget(QWidget):
    """算法 Widget 描述"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signal()

    def setup_ui(self):
        """初始化 UI"""
        pass

    def connect_signal(self):
        """连接信号槽"""
        pass

    def execute_algorithm(self):
        """执行算法"""
        pass
```

### 测试规范

```python
import pytest
from core.algorithms.xxx import Algorithm


class TestAlgorithm:
    """算法测试类"""

    def test_basic_functionality(self):
        """测试基本功能"""
        result = Algorithm.do_something()
        assert result == expected

    def test_edge_cases(self):
        """测试边界情况"""
        pass
```

## 项目结构

```
PyCryptoLab/
├── core/
│   └── algorithms/           # 算法后端
│       ├── classical/       # 经典密码
│       ├── symmetric/       # 对称密码
│       ├── asymmetric/      # 公钥密码
│       ├── hash/           # 哈希算法
│       └── mathematical/    # 数学基础
├── ui/
│   └── widgets/            # UI Widget
├── infrastructure/          # 工具函数
├── tests/
│   └── unit/              # 单元测试
└── resources/             # 资源文件
```

## 添加新算法

### 1. 后端实现

在 `core/algorithms/<category>/` 下创建算法文件：

```python
from infrastructure.Thread import BaseThread


class AlgorithmThread(BaseThread):
    """算法线程"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.params = {}

    def run(self):
        """执行算法"""
        try:
            result = self._algorithm(**self.params)
            self.finished_signal.emit(result, "")
        except Exception as e:
            self.error_signal.emit(str(e))
```

### 2. UI Widget

在 `ui/widgets/` 下创建 Widget：

```python
from ui.widgets.template_widget import BaseWidget


class AlgorithmWidget(BaseWidget):
    """算法 Widget"""

    def __init__(self, parent=None):
        super().__init__(parent)
        # 初始化代码
```

### 3. 注册 Widget

更新相关文件：

1. `ui/widgets/__init__.py` - 导出 Widget
2. `ui/main_window.py` - 添加到导航和 widget_map

### 4. 添加测试

在 `tests/unit/` 下创建测试文件：

```bash
pytest tests/unit/test_algorithm.py -v
```

## 常见问题

### Q: CI 失败了怎么办？

A: 检查以下内容：
1. flake8 是否有错误
2. pytest 测试是否通过
3. PYTHONPATH 是否正确设置

### Q: 如何运行特定测试？

```bash
pytest tests/unit/test_xxx.py -v
```

### Q: 可以直接在 main 分支开发吗？

A: ❌ 不可以。所有更改必须在功能分支进行，通过 PR 合并。

## 联系方式

- GitHub Issues: [提交问题](https://github.com/h1s97x/PyCryptoLab/issues)
- 邮箱: (如有)

## 许可证

参与本项目即表示您同意您的贡献将受 MIT 许可证约束。
