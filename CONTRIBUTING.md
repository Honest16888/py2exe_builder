# 贡献指南

感谢你对 Py2EXE Builder 的关注！我们欢迎所有形式的贡献。

## 如何贡献

### 报告 Bug

1. 在 [Issues](https://github.com/honest16888/Py2EXE-Builder/issues) 中搜索是否已有相同问题
2. 如果没有，创建新的 Issue，包含：
   - 问题描述
   - 复现步骤
   - 期望行为
   - 实际行为
   - 系统信息（Windows 版本、Python 版本）
   - 错误日志（如果有）

### 提交功能建议

1. 在 Issues 中创建新 Issue，标记为 "enhancement"
2. 描述功能需求和使用场景

### 提交代码

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m 'Add some feature'`
4. 推送到分支：`git push origin feature/your-feature`
5. 创建 Pull Request

## 开发环境

```bash
# 克隆仓库
git clone https://github.com/honest16888/Py2EXE-Builder.git
cd Py2EXE-Builder

# 创建虚拟环境（可选）
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install pyinstaller

# 运行
python py2exe_builder.pyw
```

## 代码规范

- 遵循 PEP 8 Python 代码规范
- 使用有意义的变量名和函数名
- 为公共函数添加文档字符串
- 保持代码简洁，避免过度工程化

## 提交信息规范

使用清晰的提交信息：

- `feat: 添加新功能`
- `fix: 修复 Bug`
- `docs: 更新文档`
- `style: 代码格式调整`
- `refactor: 重构代码`
- `test: 添加测试`
- `chore: 构建/工具变更`

## 问题标签

- `bug` — Bug 报告
- `enhancement` — 功能建议
- `documentation` — 文档改进
- `good first issue` — 适合新手
- `help wanted` — 需要帮助

## 行为准则

- 尊重每一位参与者
- 接受建设性的批评
- 专注于对社区最有利的事情
- 对其他社区成员表示同理心

## 许可证

贡献即表示你同意你的代码在 [MIT 许可证](LICENSE) 下发布。

## 联系方式

如有任何问题，请通过 Issues 或邮件联系。
