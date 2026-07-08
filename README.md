# Py2EXE Builder

一个基于 tkinter 的 Python 图形化打包工具，将 Python 脚本打包为独立可执行的 EXE 文件。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-green.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/)

![Py2EXE Builder](https://via.placeholder.com/800x400/1e293b/818cf8?text=Py2EXE+Builder)

## 功能特性

- **两种打包模式**
  - 单文件模式 (onefile) — 所有内容合并为一个 EXE 文件
  - 文件夹模式 (onedir) — 输出包含所有依赖的文件夹

- **打包选项**
  - 隐藏控制台窗口 — 启动 EXE 时不弹出黑色 CMD 窗口
  - 管理员权限 (UAC) — 请求管理员权限运行

- **自定义图标**
  - 支持为打包后的 EXE 设置自定义图标 (.ico 格式)
  - 不设置则使用默认图标

- **目录管理**
  - 自定义输出目录
  - 自定义缓存目录（构建临时文件）

- **依赖管理**
  - 一键安装/更新 PyInstaller
  - 自动检测 PyInstaller 版本

- **用户体验**
  - 深色主题界面
  - 实时构建日志
  - 打包进度显示
  - 全局异常捕获与日志记录

## 截图

| 主界面 | 打包中 |
|--------|--------|
| ![主界面](https://via.placeholder.com/400x300/0f172a/10b981?text=Main+UI) | ![打包中](https://via.placeholder.com/400x300/0f172a/06b6d4?text=Building...) |

## 快速开始

### 方式一：直接运行 EXE

1. 下载 [Releases](https://github.com/honest16888/Py2EXE-Builder/releases) 中的 `Py2EXE_Builder.exe`
2. 双击运行
3. 选择 Python 脚本，点击"开始打包"

### 方式二：从源码运行

```bash
# 克隆仓库
git clone https://github.com/honest16888/Py2EXE-Builder.git
cd Py2EXE-Builder

# 安装依赖
pip install pyinstaller

# 运行
python py2exe_builder.pyw
```

## 使用说明

1. **选择脚本** — 点击"浏览"选择要打包的 `.py` 文件
2. **选择模式** — 单文件或文件夹模式
3. **设置选项** — 隐藏控制台、管理员权限等
4. **设置图标** — 可选，为 EXE 设置自定义图标
5. **设置目录** — 输出目录和缓存目录
6. **安装依赖** — 首次使用点击"安装/更新 PyInstaller"
7. **开始打包** — 点击"开始打包"按钮

## 系统要求

- Windows 10/11
- Python 3.9 或更高版本
- PyInstaller（工具会自动检测和安装）

## 构建 EXE

如果你想将本工具也打包为 EXE：

```bash
pip install pyinstaller

pyinstaller --noconfirm --clean --onefile --windowed \
  --icon=app_icon.ico \
  --name Py2EXE_Builder \
  py2exe_builder.pyw
```

生成的 EXE 文件位于 `dist/` 目录。

## 项目结构

```
Py2EXE-Builder/
├── py2exe_builder.pyw    # 主程序源码
├── app_icon.ico          # 应用图标
├── LICENSE               # MIT 许可证
├── README.md             # 项目说明
├── CONTRIBUTING.md       # 贡献指南
└── .gitignore            # Git 忽略文件
```

## 贡献

欢迎贡献代码！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 致谢

- [PyInstaller](https://pyinstaller.org/) — Python 打包工具
- [tkinter](https://docs.python.org/3/library/tkinter.html) — Python GUI 库

## 联系方式

- Issues: [GitHub Issues](https://github.com/honest16888/Py2EXE-Builder/issues)
- Email: 3167504185@qq.com
