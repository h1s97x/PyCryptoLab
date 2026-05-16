# 快速开始 - 项目重构

## 🎯 目标
清理项目结构混乱，删除旧目录，统一使用新的 `core/algorithms` 结构。

## ⚡ 一键执行（推荐）

```bash
python restructure.py
```

这个脚本会自动完成所有步骤，包括备份、更新、测试和清理。

---

## 📋 手动执行（分步骤）

### 步骤 1: 创建备份
```bash
git add .
git commit -m "Backup before restructure"
git tag backup-before-restructure
```

### 步骤 2: 更新导入路径
```bash
python update_imports.py
```

这会自动更新所有 UI 文件中的导入语句：
- `from ClassicCrypto.Caesar import Caesar` → `from core.algorithms.classical.Caesar import Thread as Caesar`
- `from BlockCipher.AES import AES` → `from core.algorithms.symmetric.AES import Thread as AES`
- 等等...

### 步骤 3: 验证更新
```bash
# 查看更改
git diff ui/widgets/

# 运行测试
python test_project.py
python test_algorithms.py
```

### 步骤 4: 清理旧结构
```bash
python cleanup_old_structure.py
```

这会删除：
- `BlockCipher/`
- `ClassicCrypto/`
- `Hash/`
- `PublicKeyCryptography/`
- `StreamCipher/`
- `MathematicalBasis/`
- `CryptographicProtocol/`
- 以及对应的 `.py` 兼容层文件

### 步骤 5: 最终测试
```bash
# 测试导入
python -c "from core.algorithms.classical.Caesar import Thread; print('✓ 导入成功')"

# 启动应用
python main.py
```

### 步骤 6: 提交更改
```bash
git add .
git commit -m "Complete project restructure: remove old directories, update all imports"
```

---

## 🔄 如果出现问题

### 回滚到重构前
```bash
git reset --hard backup-before-restructure
```

### 只回滚文件删除（保留导入更新）
```bash
git checkout HEAD -- BlockCipher/ ClassicCrypto/ Hash/ PublicKeyCryptography/ StreamCipher/ MathematicalBasis/
```

---

## 📊 预期结果

### 重构前
```
项目根目录/
├── BlockCipher/          ← 旧结构（空心化）
├── ClassicCrypto/        ← 旧结构（空心化）
├── Hash/                 ← 旧结构（空心化）
├── core/algorithms/      ← 新结构（已有实现）
└── ui/widgets/           ← 使用旧导入路径
```

### 重构后
```
项目根目录/
├── core/algorithms/      ← 唯一的算法实现位置
│   ├── classical/
│   ├── symmetric/
│   ├── asymmetric/
│   ├── hash/
│   └── mathematical/
└── ui/widgets/           ← 使用新导入路径
```

---

## ✅ 检查清单

重构完成后，确认以下内容：

- [ ] 旧目录已删除（BlockCipher、ClassicCrypto等）
- [ ] 所有 UI 文件使用新导入路径
- [ ] `python test_project.py` 通过
- [ ] `python test_algorithms.py` 通过
- [ ] `python main.py` 可以启动
- [ ] Git 提交已完成

---

## 📝 注意事项

1. **备份很重要**：重构前务必创建 Git 备份
2. **测试很重要**：每个步骤后都要测试
3. **不要跳步骤**：按顺序执行，确保每步成功
4. **保持冷静**：如果出错，可以回滚

---

## 🆘 常见问题

### Q: 导入更新后测试失败？
A: 检查是否有特殊的导入方式未被脚本覆盖，手动修复后重新测试。

### Q: 删除旧目录后应用无法启动？
A: 回滚并检查是否有文件仍在使用旧路径：
```bash
git reset --hard backup-before-restructure
grep -r "from BlockCipher" ui/
grep -r "from ClassicCrypto" ui/
```

### Q: 想保留旧结构作为兼容层？
A: 参考 `RESTRUCTURE_PLAN.md` 中的"方案B：渐进式迁移"

---

## 📞 需要帮助？

查看详细文档：
- `RESTRUCTURE_PLAN.md` - 完整重构方案
- `TEST_REPORT.md` - 测试报告
- `README.md` - 项目说明

---

**准备好了吗？运行 `python restructure.py` 开始重构！** 🚀
