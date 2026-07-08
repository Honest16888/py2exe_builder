# -*- coding: utf-8 -*-
"""
Py2EXE Builder - Python 程序打包工具
将 Python 脚本打包为独立可执行的 EXE 文件

Author: honest16888
License: MIT
Repository: https://github.com/honest16888/Py2EXE-Builder
"""

import os
import sys
import subprocess
import threading
import traceback
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

LOG_FILE = os.path.join(os.environ.get("TEMP", "."), "py2exe_builder_crash.log")


def _excepthook(exc_type, exc_value, exc_tb):
    """全局异常捕获，写入日志文件"""
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n{'=' * 60}\n{tb}\n")
    except Exception:
        pass
    try:
        messagebox.showerror("程序崩溃", f"异常已记录:\n{LOG_FILE}\n\n{tb[-500:]}")
    except Exception:
        pass


sys.excepthook = _excepthook

# ============================================================ 主题颜色
T = {
    "primary": "#6366f1",
    "primary_d": "#4f46e5",
    "primary_l": "#818cf8",
    "bg": "#0f172a",
    "bg_card": "#1e293b",
    "bg_card2": "#273548",
    "bg_input": "#0f172a",
    "green": "#10b981",
    "green_d": "#059669",
    "red": "#ef4444",
    "orange": "#f59e0b",
    "cyan": "#06b6d4",
    "fg": "#f1f5f9",
    "fg2": "#94a3b8",
    "fg3": "#64748b",
    "border": "#334155",
    "border_l": "#475569",
}


def _find_python():
    """查找系统中可用的 Python 解释器"""
    if not getattr(sys, "frozen", False):
        return sys.executable

    candidates = []
    for n in ("py", "py3", "py3.11", "py3.10", "py3.9"):
        candidates.append(n)

    for base in (
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Python"),
        r"C:\Python311",
        r"C:\Python310",
        r"C:\Python39",
        r"C:\Python3",
    ):
        if os.path.isdir(base):
            for d in sorted(os.listdir(base), reverse=True):
                exe = os.path.join(base, d, "python.exe")
                if os.path.isfile(exe):
                    candidates.append(exe)

    desktop = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")
    mingw = os.path.join(desktop, "myos", "tools", "mingw64", "mingw64", "opt", "bin")
    for n in ("python3.11.exe", "python3.10.exe", "python3.exe", "python.exe"):
        p = os.path.join(mingw, n)
        if os.path.isfile(p):
            candidates.append(p)

    for n in ("python3.exe", "python.exe"):
        candidates.append(n)

    for c in candidates:
        try:
            r = subprocess.run(
                [c, "--version"],
                capture_output=True,
                text=True,
                timeout=10,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            if r.returncode == 0 and "Python" in (r.stdout + r.stderr):
                return c
        except Exception:
            continue
    return None


class Py2EXEBuilder:
    """Py2EXE Builder 主界面"""

    def __init__(self, root):
        self.root = root
        self.root.title("Py2EXE Builder")
        self.root.geometry("760x820")
        self.root.minsize(700, 720)
        self.root.configure(bg=T["bg"])

        try:
            ico = os.path.join(
                os.path.dirname(os.path.abspath(sys.argv[0])), "app_icon.ico"
            )
            if os.path.isfile(ico):
                self.root.iconbitmap(ico)
        except Exception:
            pass

        self.building = False
        self.process = None
        self.python_exe = _find_python()
        self._build_ui()
        self._check_pyinstaller()

    # ---- UI 组件工厂 ----

    def _card(self, parent, title, icon=""):
        """创建带标题的卡片容器"""
        card = tk.Frame(
            parent, bg=T["bg_card"], highlightbackground=T["border"], highlightthickness=1
        )
        card.pack(fill=tk.X, pady=(0, 10))
        hdr = tk.Frame(card, bg=T["bg_card"])
        hdr.pack(fill=tk.X, padx=16, pady=(12, 6))
        if icon:
            tk.Label(
                hdr,
                text=icon,
                font=("Segoe UI Emoji", 11),
                fg=T["primary_l"],
                bg=T["bg_card"],
            ).pack(side=tk.LEFT, padx=(0, 6))
        tk.Label(
            hdr,
            text=title,
            font=("Segoe UI", 11, "bold"),
            fg=T["fg"],
            bg=T["bg_card"],
        ).pack(side=tk.LEFT)
        body = tk.Frame(card, bg=T["bg_card"])
        body.pack(fill=tk.X, padx=16, pady=(0, 14))
        return body

    def _entry(self, parent, var):
        """创建输入框 (pack 布局)"""
        e = tk.Entry(
            parent,
            textvariable=var,
            font=("Cascadia Code", 10),
            bg=T["bg_input"],
            fg=T["fg"],
            insertbackground=T["fg"],
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground=T["border"],
            highlightcolor=T["primary"],
        )
        e.pack(fill=tk.X, ipady=6, pady=(2, 0))
        return e

    def _entry_grid(self, parent, var, row, col):
        """创建输入框 (grid 布局)"""
        e = tk.Entry(
            parent,
            textvariable=var,
            font=("Cascadia Code", 10),
            bg=T["bg_input"],
            fg=T["fg"],
            insertbackground=T["fg"],
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground=T["border"],
            highlightcolor=T["primary"],
        )
        e.grid(row=row, column=col, sticky=tk.EW, padx=8, pady=4, ipady=6)
        return e

    def _btn(self, parent, text, cmd, variant="default", w=None):
        """创建按钮"""
        styles = {
            "default": (T["bg_card2"], T["fg2"], T["border_l"], T["fg"]),
            "primary": (T["primary"], "#ffffff", T["primary_d"], "#ffffff"),
            "success": (T["green"], "#ffffff", T["green_d"], "#ffffff"),
            "ghost": (T["bg_card"], T["fg2"], T["border"], T["fg"]),
        }
        bg, fg, abg, af = styles.get(variant, styles["default"])
        b = tk.Button(
            parent,
            text=text,
            command=cmd,
            font=("Segoe UI", 10),
            bg=bg,
            fg=fg,
            activebackground=abg,
            activeforeground=af,
            relief=tk.FLAT,
            bd=0,
            padx=16,
            pady=6,
            cursor="hand2",
        )
        if w:
            b.config(width=w)
        b.bind("<Enter>", lambda e, b=b, c=abg: b.config(bg=c))
        b.bind("<Leave>", lambda e, b=b, c=bg: b.config(bg=c))
        return b

    # ==================== 界面构建 ====================

    def _build_ui(self):
        canvas = tk.Canvas(self.root, bg=T["bg"], highlightthickness=0)
        vsb = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=canvas.yview)
        self.main = tk.Frame(canvas, bg=T["bg"])
        self.main.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.main, anchor=tk.NW)
        canvas.configure(yscrollcommand=vsb.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
        )
        m = self.main

        # 标题栏
        top = tk.Frame(m, bg=T["primary"], height=72)
        top.pack(fill=tk.X)
        top.pack_propagate(False)
        tk.Label(
            top,
            text="Py2EXE Builder",
            font=("Segoe UI", 20, "bold"),
            fg="#ffffff",
            bg=T["primary"],
        ).pack(side=tk.LEFT, padx=24, pady=16)
        tk.Label(
            top,
            text="Python → EXE 打包工具",
            font=("Segoe UI", 11),
            fg="#c7d2fe",
            bg=T["primary"],
        ).pack(side=tk.LEFT, pady=16)
        tk.Label(
            top,
            text=self.python_exe or "未找到Python",
            font=("Cascadia Code", 9),
            fg="#a5b4fc",
            bg=T["primary"],
        ).pack(side=tk.RIGHT, padx=24)

        content = tk.Frame(m, bg=T["bg"])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(16, 0))

        # 脚本选择
        card = self._card(content, "Python 脚本", "\U0001F4C2")
        row = tk.Frame(card, bg=T["bg_card"])
        row.pack(fill=tk.X)
        self.var_script = tk.StringVar()
        self._entry(row, self.var_script).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10)
        )
        self._btn(row, "\U0001F50D 浏览", self._browse_script, "ghost").pack(
            side=tk.RIGHT
        )

        # 打包模式
        card = self._card(content, "打包模式", "\U0001F4E6")
        mf = tk.Frame(card, bg=T["bg_card"])
        mf.pack(fill=tk.X)
        self.var_mode = tk.StringVar(value="onefile")
        for i, (text, val, desc) in enumerate(
            [
                ("单文件", "onefile", "onefile — 合并为单一 EXE"),
                ("文件夹", "onedir", "onedir — 输出包含依赖的文件夹"),
            ]
        ):
            f = tk.Frame(
                mf,
                bg=T["bg_card2"],
                highlightbackground=T["border"],
                highlightthickness=1,
            )
            f.pack(
                side=tk.LEFT,
                fill=tk.X,
                expand=True,
                padx=(0, 8) if i == 0 else 0,
            )
            tk.Radiobutton(
                f,
                text=text,
                variable=self.var_mode,
                value=val,
                font=("Segoe UI", 11, "bold"),
                bg=T["bg_card2"],
                fg=T["fg"],
                selectcolor=T["bg_input"],
                activebackground=T["bg_card2"],
                activeforeground=T["fg"],
                indicatoron=False,
                padx=12,
                pady=8,
                cursor="hand2",
            ).pack(fill=tk.X)
            tk.Label(
                f,
                text=desc,
                font=("Segoe UI", 8),
                fg=T["fg3"],
                bg=T["bg_card2"],
            ).pack(padx=12, anchor=tk.W, pady=(0, 4))

        # 打包选项
        card = self._card(content, "打包选项", "\u2699\ufe0f")
        opts = tk.Frame(card, bg=T["bg_card"])
        opts.pack(fill=tk.X)
        self.var_hide_console = tk.BooleanVar(value=True)
        self.var_admin = tk.BooleanVar(value=False)
        for text, var in [
            ("隐藏控制台窗口", self.var_hide_console),
            ("请求管理员权限 (UAC)", self.var_admin),
        ]:
            f = tk.Frame(
                opts,
                bg=T["bg_card2"],
                highlightbackground=T["border"],
                highlightthickness=1,
            )
            f.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
            tk.Checkbutton(
                f,
                text=text,
                variable=var,
                font=("Segoe UI", 10),
                bg=T["bg_card2"],
                fg=T["fg"],
                selectcolor=T["bg_input"],
                activebackground=T["bg_card2"],
                activeforeground=T["fg"],
                cursor="hand2",
            ).pack(padx=10, pady=6, anchor=tk.W)

        extra = tk.Frame(card, bg=T["bg_card"])
        extra.pack(fill=tk.X, pady=(8, 0))
        tk.Label(
            extra,
            text="额外 PyInstaller 参数:",
            font=("Segoe UI", 10),
            fg=T["fg2"],
            bg=T["bg_card"],
        ).pack(anchor=tk.W)
        self.var_extra_args = tk.StringVar()
        self._entry(extra, self.var_extra_args).pack(fill=tk.X)

        # 图标设置
        card = self._card(content, "EXE 图标", "\U0001F5BC\ufe0f")
        ir = tk.Frame(card, bg=T["bg_card"])
        ir.pack(fill=tk.X)
        self.var_icon = tk.StringVar()
        self._entry(ir, self.var_icon).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10)
        )
        self._btn(ir, "\U0001F50D", self._browse_icon, "ghost", w=4).pack(
            side=tk.RIGHT, padx=(0, 6)
        )
        self._btn(ir, "\u2715 清除", self._clear_icon, "ghost").pack(side=tk.RIGHT)
        self.lbl_icon_hint = tk.Label(
            card,
            text="支持 .ico 格式，不设置则使用默认图标",
            font=("Segoe UI", 9),
            fg=T["fg3"],
            bg=T["bg_card"],
            anchor="w",
        )
        self.lbl_icon_hint.pack(fill=tk.X, pady=(4, 0))

        # 目录设置 (统一 grid 布局)
        card = self._card(content, "输出目录", "\U0001F4C1")
        dirs = tk.Frame(card, bg=T["bg_card"])
        dirs.pack(fill=tk.X)
        dirs.columnconfigure(1, weight=1)
        self.var_outdir = tk.StringVar()
        self.var_cachedir = tk.StringVar()
        for i, (label, var, cmd) in enumerate(
            [
                ("输出目录", self.var_outdir, self._browse_outdir),
                ("缓存目录", self.var_cachedir, self._browse_cachedir),
            ]
        ):
            tk.Label(
                dirs,
                text=label,
                font=("Segoe UI", 10),
                fg=T["fg2"],
                bg=T["bg_card"],
                width=8,
                anchor="w",
            ).grid(row=i, column=0, sticky=tk.W, pady=4)
            self._entry_grid(dirs, var, i, 1)
            self._btn(dirs, "\U0001F50D", cmd, "ghost", w=4).grid(
                row=i, column=2, pady=4, padx=(0, 4)
            )

        # 依赖管理
        card = self._card(content, "依赖管理", "\U0001F9E9")
        dep = tk.Frame(card, bg=T["bg_card"])
        dep.pack(fill=tk.X)
        self.lbl_dep = tk.Label(
            dep,
            text="\u23f3 检测中...",
            font=("Segoe UI", 10),
            fg=T["orange"],
            bg=T["bg_card"],
        )
        self.lbl_dep.pack(side=tk.LEFT)
        self._btn(
            dep,
            "\U0001F504 安装/更新 PyInstaller",
            self._install_pyinstaller,
            "primary",
        ).pack(side=tk.RIGHT)

        # 进度
        card = self._card(content, "打包进度", "\u26a1")
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "S.Horizontal.TProgressbar",
            troughcolor=T["bg_card2"],
            background=T["green"],
            thickness=8,
            bordercolor=T["bg_card"],
            lightcolor=T["green"],
            darkcolor=T["green"],
        )
        self.progress = ttk.Progressbar(
            card, mode="determinate", style="S.Horizontal.TProgressbar"
        )
        self.progress.pack(fill=tk.X, pady=(0, 4))
        self.lbl_progress = tk.Label(
            card,
            text="就绪",
            font=("Cascadia Code", 9),
            fg=T["fg3"],
            bg=T["bg_card"],
            anchor="w",
        )
        self.lbl_progress.pack(fill=tk.X)

        # 日志
        card = self._card(content, "构建日志", "\U0001F4DC")
        self.log_text = tk.Text(
            card,
            height=7,
            font=("Cascadia Code", 9),
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg=T["bg_input"],
            fg=T["fg2"],
            insertbackground=T["fg"],
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground=T["border"],
            padx=8,
            pady=6,
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # 底部按钮
        bottom = tk.Frame(m, bg=T["bg"])
        bottom.pack(fill=tk.X, padx=20, pady=(12, 20))
        self.btn_build = self._btn(
            bottom, "\u25B6  开始打包", self._start_build, "success"
        )
        self.btn_build.pack(side=tk.LEFT)
        self._btn(
            bottom, "\U0001F4C2 打开输出目录", self._open_output, "default"
        ).pack(side=tk.LEFT, padx=12)
        self.btn_cancel = self._btn(bottom, "取消", self._cancel_build, "default")
        self.btn_cancel.pack(side=tk.RIGHT)
        self.btn_cancel.config(state=tk.DISABLED)

    # ==================== 文件浏览 ====================

    def _browse_script(self):
        p = filedialog.askopenfilename(
            filetypes=[("Python", "*.py"), ("All", "*.*")]
        )
        if p:
            self.var_script.set(p)
            if not self.var_outdir.get():
                self.var_outdir.set(os.path.dirname(p))

    def _browse_icon(self):
        p = filedialog.askopenfilename(filetypes=[("ICO", "*.ico"), ("All", "*.*")])
        if p:
            self.var_icon.set(p)
            name = os.path.basename(p)
            sz = os.path.getsize(p) // 1024
            self.lbl_icon_hint.config(
                text=f"\u2705 已选择: {name} ({sz} KB)", fg=T["green"]
            )

    def _clear_icon(self):
        self.var_icon.set("")
        self.lbl_icon_hint.config(
            text="支持 .ico 格式，不设置则使用默认图标", fg=T["fg3"]
        )

    def _browse_outdir(self):
        p = filedialog.askdirectory()
        if p:
            self.var_outdir.set(p)

    def _browse_cachedir(self):
        p = filedialog.askdirectory()
        if p:
            self.var_cachedir.set(p)

    # ==================== 日志与状态 ====================

    def _log(self, msg):
        def _do():
            try:
                self.log_text.config(state=tk.NORMAL)
                self.log_text.insert(tk.END, msg + "\n")
                self.log_text.see(tk.END)
                self.log_text.config(state=tk.DISABLED)
            except Exception:
                pass

        self.root.after(0, _do)

    def _set_status(self, text, pct=None, color=None):
        def _do():
            try:
                c = color or (T["green"] if pct == 100 else T["fg2"])
                self.lbl_progress.config(text=text, fg=c)
                if pct is not None:
                    self.progress["value"] = pct
            except Exception:
                pass

        self.root.after(0, _do)

    def _run_cmd(self, args, timeout=60):
        cf = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        r = subprocess.run(
            args, capture_output=True, text=True, timeout=timeout, creationflags=cf
        )
        return r.returncode, r.stdout, r.stderr

    # ==================== PyInstaller 管理 ====================

    def _check_pyinstaller(self):
        if not self.python_exe:
            self.lbl_dep.config(text="\u274c 未找到Python", fg=T["red"])
            return

        def _check():
            try:
                code, out, err = self._run_cmd(
                    [self.python_exe, "-m", "PyInstaller", "--version"]
                )
                ver = (out or err).strip()
                if code == 0 and ver:
                    self.root.after(
                        0,
                        lambda: self.lbl_dep.config(
                            text=f"\u2705 PyInstaller v{ver}", fg=T["green"]
                        ),
                    )
                else:
                    self.root.after(
                        0,
                        lambda: self.lbl_dep.config(
                            text="\u26a0\ufe0f 未安装", fg=T["orange"]
                        ),
                    )
            except Exception:
                self.root.after(
                    0,
                    lambda: self.lbl_dep.config(text="\u274c 检测失败", fg=T["red"]),
                )

        threading.Thread(target=_check, daemon=True).start()

    def _install_pyinstaller(self):
        if not self.python_exe:
            messagebox.showerror("错误", "未找到Python")
            return
        self.lbl_dep.config(text="\u23f3 安装中...", fg=T["orange"])
        self._log(">>> pip install --upgrade pyinstaller")
        self.btn_build.config(state=tk.DISABLED)

        def _run():
            try:
                code, out, err = self._run_cmd(
                    [
                        self.python_exe,
                        "-m",
                        "pip",
                        "install",
                        "--upgrade",
                        "pyinstaller",
                    ],
                    timeout=300,
                )
                if out:
                    self._log(out)
                if code != 0 and err:
                    self._log(f"[错误] {err}")
                    self.root.after(
                        0,
                        lambda: self.lbl_dep.config(
                            text="\u274c 安装失败", fg=T["red"]
                        ),
                    )
                else:
                    self.root.after(
                        0,
                        lambda: self.lbl_dep.config(
                            text="\u2705 PyInstaller 已安装", fg=T["green"]
                        ),
                    )
                    self._log(">>> 安装成功")
            except Exception as e:
                self._log(f"[异常] {e}")
                self.root.after(
                    0,
                    lambda: self.lbl_dep.config(text="\u274c 安装失败", fg=T["red"]),
                )
            finally:
                self.root.after(
                    0, lambda: self.btn_build.config(state=tk.NORMAL)
                )

        threading.Thread(target=_run, daemon=True).start()

    # ==================== 打包核心 ====================

    def _start_build(self):
        if self.building:
            return
        if not self.python_exe:
            messagebox.showerror("错误", "未找到Python")
            return
        script = self.var_script.get().strip()
        if not script:
            messagebox.showwarning("提示", "请先选择Python脚本")
            return
        if not os.path.isfile(script):
            messagebox.showerror("错误", f"文件不存在:\n{script}")
            return

        outdir = self.var_outdir.get().strip() or os.path.dirname(script)
        cachedir = self.var_cachedir.get().strip()
        icon_path = self.var_icon.get().strip()

        try:
            os.makedirs(outdir, exist_ok=True)
            if cachedir:
                os.makedirs(cachedir, exist_ok=True)
        except Exception as e:
            messagebox.showerror("错误", f"创建目录失败:\n{e}")
            return

        if icon_path and not os.path.isfile(icon_path):
            messagebox.showerror("错误", f"图标文件不存在:\n{icon_path}")
            return

        cmd = [
            self.python_exe,
            "-m",
            "PyInstaller",
            "--noconfirm",
            "--clean",
            f"--{self.var_mode.get()}",
            "--distpath",
            outdir,
        ]
        if cachedir:
            cmd += ["--workpath", cachedir, "--specpath", cachedir]
        if icon_path:
            cmd += ["--icon", icon_path]
        if self.var_hide_console.get():
            cmd.append("--windowed")
        if self.var_admin.get():
            cmd.append("--uac-admin")
        extra = self.var_extra_args.get().strip()
        if extra:
            cmd += extra.split()
        cmd.append(script)

        self._log(">>> " + " ".join(cmd))
        self._set_status("正在打包...", 0, T["cyan"])
        self.building = True
        self.btn_build.config(state=tk.DISABLED)
        self.btn_cancel.config(state=tk.NORMAL)
        self.progress["value"] = 0
        threading.Thread(target=self._run_build, args=(cmd, outdir), daemon=True).start()

    def _run_build(self, cmd, outdir):
        try:
            cf = getattr(subprocess, "CREATE_NO_WINDOW", 0)
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=cf,
            )
            while True:
                try:
                    line = self.process.stdout.readline()
                except Exception:
                    break
                if not line:
                    break
                line = line.rstrip("\r\n")
                if line:
                    self._log(line)
                    low = line.lower()
                    if "building" in low:
                        self._set_status("编译中...", 30, T["cyan"])
                    elif "installing" in low:
                        self._set_status("安装依赖...", 50, T["cyan"])
                    elif "linking" in low:
                        self._set_status("链接中...", 70, T["cyan"])
                    elif "collecting" in low:
                        self._set_status("收集文件...", 40, T["cyan"])
            self.process.wait()
            rc = self.process.returncode
            if rc == 0:
                self._set_status("打包完成！", 100, T["green"])
                self._log(f"\n>>> \u2705 打包成功！输出: {outdir}")
                self.root.after(
                    0,
                    lambda: messagebox.showinfo("成功", f"打包完成！\n{outdir}"),
                )
            else:
                self._set_status("打包失败", 0, T["red"])
                self._log(f"\n>>> \u274c 失败 (退出码: {rc})")
        except Exception as e:
            self._set_status("异常", 0, T["red"])
            self._log(f"[异常] {e}")
            try:
                with open(LOG_FILE, "a", encoding="utf-8") as f:
                    f.write(f"\n_build: {traceback.format_exc()}\n")
            except Exception:
                pass
        finally:
            self.process = None
            self.building = False
            self.root.after(0, lambda: self.btn_build.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.btn_cancel.config(state=tk.DISABLED))

    def _cancel_build(self):
        if self.process:
            self._log(">>> 取消中...")
            try:
                self.process.kill()
            except Exception:
                pass
        self._set_status("已取消", 0, T["orange"])

    def _open_output(self):
        d = self.var_outdir.get().strip()
        if d and os.path.isdir(d):
            os.startfile(d)
        else:
            messagebox.showinfo("提示", "输出目录不存在或未设置")


def main():
    root = tk.Tk()
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    Py2EXEBuilder(root)
    root.mainloop()


if __name__ == "__main__":
    main()
