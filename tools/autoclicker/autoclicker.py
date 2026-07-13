"""
AutoClicker - 多步骤宏工具（合并版）
功能: 窗口绑定 + 多步骤宏 + 录制回放 + 随机偏移 + 图片识别 + Game Mode
用法: 以管理员身份运行 → python autoclicker.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import threading
import random
import time
import json
import os
import ctypes
import ctypes.wintypes

os.environ["OPENCV_LOG_LEVEL"] = "SILENT"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    import win32api
    import win32gui
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

try:
    import pyautogui
    pyautogui.FAILSAFE = False
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

try:
    from pynput import keyboard as kb_listener
    from pynput import mouse as mouse_listener
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False

# Interception 驱动检测
INTERCEPTION_AVAILABLE = False
try:
    import interception
    _ctx = interception.lib.interception_create_context()
    if _ctx and not interception.lib.interception_is_invalid(_ctx):
        INTERCEPTION_AVAILABLE = True
        interception.lib.interception_destroy_context(_ctx)
except Exception:
    pass


# ===========================================================================
# SendInput 常量与结构体
# ===========================================================================
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_WHEEL = 0x0800
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_KEYUP = 0x0002

_VK_TO_SCANCODE = {
    "enter": 0x1C, "return": 0x1C, "space": 0x39, "tab": 0x0F,
    "escape": 0x01, "esc": 0x01, "backspace": 0x0E, "delete": 0x53,
    "home": 0x47, "end": 0x4F, "pageup": 0x49, "pagedown": 0x51,
    "up": 0x48, "down": 0x50, "left": 0x4B, "right": 0x4D,
    "f1": 0x3B, "f2": 0x3C, "f3": 0x3D, "f4": 0x3E,
    "f5": 0x3F, "f6": 0x40, "f7": 0x41, "f8": 0x42,
    "f9": 0x43, "f10": 0x44, "f11": 0x57, "f12": 0x58,
    "ctrl": 0x1D, "alt": 0x38, "shift": 0x2A,
}


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long), ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong), ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong), ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class _INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", ctypes.c_ulong * 6),
        ("hi", ctypes.c_ulong * 2),
    ]


class SENDINPUT(ctypes.Structure):
    _anonymous_ = ("u",)
    _fields_ = [
        ("type", ctypes.c_uint),
        ("u", _INPUT_UNION),
    ]


# ===========================================================================
# 模块级辅助函数
# ===========================================================================

def _make_move_input(screen_x, screen_y):
    user32 = ctypes.windll.user32
    w = user32.GetSystemMetrics(0)
    h = user32.GetSystemMetrics(1)
    inp = SENDINPUT()
    inp.type = INPUT_MOUSE
    inp.mi.dx = int((screen_x / w) * 65535)
    inp.mi.dy = int((screen_y / h) * 65535)
    inp.mi.dwFlags = MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE
    return inp


def _make_button_inputs(click_type):
    flags = {
        "left": (MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP),
        "right": (MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP),
        "middle": (MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP),
    }
    if click_type == "double":
        pairs = [flags["left"], flags["left"]]
    else:
        pairs = [flags.get(click_type, flags["left"])]
    inputs = []
    for down_f, up_f in pairs:
        d = SENDINPUT()
        d.type = INPUT_MOUSE
        d.mi.dwFlags = down_f
        inputs.append(d)
        u = SENDINPUT()
        u.type = INPUT_MOUSE
        u.mi.dwFlags = up_f
        inputs.append(u)
    return inputs


def _send_input_array(inputs):
    arr = (SENDINPUT * len(inputs))(*inputs)
    ctypes.windll.user32.SendInput(len(inputs), ctypes.byref(arr), ctypes.sizeof(SENDINPUT))


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def cv2_read_image(path):
    """读取图片，支持中文路径"""
    try:
        data = np.fromfile(path, dtype=np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)
        return img
    except Exception:
        return None


# ===========================================================================
# MacroStep 数据模型
# ===========================================================================

class MacroStep:
    __slots__ = ("action", "params")

    def __init__(self, action, params=None):
        self.action = action
        self.params = params or {}

    def describe(self):
        if self.action == "left_click":
            desc = f"左键点击  ({self.params.get('x',0)}, {self.params.get('y',0)})"
        elif self.action == "right_click":
            desc = f"右键点击  ({self.params.get('x',0)}, {self.params.get('y',0)})"
        elif self.action == "wait":
            desc = f"等待  {self.params.get('duration',0)} ms"
        elif self.action == "key_press":
            desc = f"按键  {self.params.get('key','')}"
        elif self.action == "image_click":
            name = os.path.basename(self.params.get("image", ""))
            timeout = self.params.get("timeout", 10)
            conf = self.params.get("confidence", 0.90)
            region_tag = " [区域]" if self.params.get("search_region") else ""
            scroll_cfg = self.params.get("scroll_on_miss")
            scroll_tag = f" [滚轮x{scroll_cfg.get('max_scrolls',0)}]" if scroll_cfg else ""
            desc = f"识图点击  [{name}]  超时{timeout}s 精度{conf:.0%}{region_tag}{scroll_tag}"
        elif self.action == "capture_save":
            name = os.path.basename(self.params.get("path", ""))
            region = self.params.get("region", {})
            w, h = region.get("w", 0), region.get("h", 0)
            desc = f"截图保存  [{name}]  {w}x{h}"
        elif self.action == "conditional_branch":
            name = os.path.basename(self.params.get("check_image", ""))
            timeout = self.params.get("timeout", 0.5)
            sub_count = len(self.params.get("sub_steps", []))
            sub_info = f"{sub_count}步" if sub_count > 0 else "自动点击"
            desc = f"条件分支  [{name}]  超时{timeout}s  {sub_info}"
        else:
            desc = "未知步骤"
        if self.params.get("run_once"):
            desc += "  [仅首次]"
        pd = self.params.get("post_delay", 0)
        if pd > 0:
            desc += f"  [+{pd}ms]"
        return desc

    def action_label(self):
        return {
            "left_click": "左键点击", "right_click": "右键点击",
            "wait": "等待延时", "key_press": "键盘按键",
            "image_click": "识图点击",
            "capture_save": "截图保存",
            "conditional_branch": "条件分支",
        }.get(self.action, self.action)

    def to_dict(self):
        return {"action": self.action, "params": self.params}

    @staticmethod
    def from_dict(d):
        return MacroStep(d["action"], d.get("params", {}))


# ===========================================================================
# 主程序
# ===========================================================================

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker - 多步骤宏工具")
        self.root.geometry("920x820")
        self.root.resizable(True, True)
        self.root.minsize(780, 600)

        # 运行状态
        self._lock = threading.Lock()
        self.is_running = False
        self.current_loop = 0
        self.current_step_idx = -1
        self.start_time = None
        self.stop_event = threading.Event()
        self.worker_thread = None

        # 宏步骤
        self.steps: list[MacroStep] = []
        self.loop_count = tk.IntVar(value=1)
        self.loop_infinite = tk.BooleanVar(value=False)

        # 窗口绑定
        self.target_hwnd = None
        self.pending_hwnd = None
        self.bind_to_window = tk.BooleanVar(value=False)
        self.click_method = tk.StringVar(value="sendinput")
        self.use_game_mode = tk.BooleanVar(value=False)
        self._window_map = {}

        # 随机偏移
        self.random_offset_enabled = tk.BooleanVar(value=False)
        self.random_offset_px = tk.IntVar(value=3)

        # 拟人模式
        self.human_mode = tk.BooleanVar(value=False)
        self.wait_variance = tk.IntVar(value=30)  # 等待时间 ±N%
        self.press_duration_min = tk.IntVar(value=30)   # 按压最短 ms
        self.press_duration_max = tk.IntVar(value=120)  # 按压最长 ms

        # 录制
        self.is_recording = False
        self.is_record_paused = False
        self._record_events = []
        self._record_start_time = 0
        self._record_pause_offset = 0  # 累计暂停时长
        self._record_pause_point = 0   # 本次暂停开始时间
        self._mouse_listener = None
        self._kb_listener_recorder = None

        # 图片识别
        self.screenshot_path = tk.StringVar(value="")

        # 热键
        self.hotkey_listener = None
        self.highlight_rect = None

        # 点击标记
        self._click_marker_overlays = []
        self._click_marker_counter = 0

        # 配置
        self.configs = {}
        self.config_file = "autoclicker_configs.json"
        self.load_all_configs()

        self.apply_styles()
        self.create_widgets()
        self.list_all_windows()
        self.start_hotkey_listener()

    # ==================================================================
    #  UI 构建
    # ==================================================================
    def create_widgets(self):
        main = ttk.Frame(self.root, padding="6")
        main.pack(fill=tk.BOTH, expand=True)

        self._build_step_list_ui(main)
        self._build_loop_record_ui(main)
        self._build_window_ui(main)
        self._build_options_ui(main)
        self._build_status_ui(main)
        self._build_control_ui(main)
        self._build_config_ui(main)

        hint = ttk.Label(main, text="提示: F9 开始 | F10 停止 | F2 暂停录制 | 以管理员运行可解决模拟器点击无效问题",
                         foreground=self._colors["dim"])
        hint.pack(fill=tk.X, pady=3)

    def _build_step_list_ui(self, parent):
        frame = ttk.LabelFrame(parent, text="宏步骤列表", padding="4")
        frame.pack(fill=tk.BOTH, expand=True, pady=2)

        cols = ("#", "action", "detail")
        self.step_tree = ttk.Treeview(frame, columns=cols, show="headings", height=5, selectmode="browse")
        self.step_tree.heading("#", text="#", anchor="center")
        self.step_tree.heading("action", text="动作", anchor="center")
        self.step_tree.heading("detail", text="详情", anchor="w")
        self.step_tree.column("#", width=35, anchor="center", stretch=False)
        self.step_tree.column("action", width=80, anchor="center", stretch=False)
        self.step_tree.column("detail", width=350, anchor="w")

        sb = ttk.Scrollbar(frame, orient="vertical", command=self.step_tree.yview)
        self.step_tree.configure(yscrollcommand=sb.set)
        self.step_tree.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.step_tree.bind("<Button-3>", self._show_step_context_menu)
        self.step_tree.bind("<Double-1>", self._on_step_double_click)

        # 执行日志（带滚动条）
        C = self._colors
        log_frame = ttk.Frame(frame)
        log_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(2, 2))
        self.step_log = tk.Text(log_frame, height=10, bg=C["input"], fg=C["dim"],
                                font=("Consolas", 10), state=tk.DISABLED,
                                relief=tk.FLAT, borderwidth=1, highlightthickness=0)
        log_sb = ttk.Scrollbar(log_frame, orient="vertical", command=self.step_log.yview)
        self.step_log.configure(yscrollcommand=log_sb.set)
        self.step_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.step_log.tag_configure("info", foreground=C["dim"])
        self.step_log.tag_configure("success", foreground=C["success"])
        self.step_log.tag_configure("fail", foreground=C["danger"])
        self.step_log.tag_configure("warn", foreground=C["warn"])
        self.step_log.tag_configure("running", foreground=C["accent"])

        # 按钮行（添加 + 编辑合并为一行）
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(2, 0))
        for text, cmd in [
            ("+ 左键", lambda: self.add_click_step("left")),
            ("+ 右键", lambda: self.add_click_step("right")),
            ("+ 等待", self.add_wait_step),
            ("+ 按键", self.add_key_step),
            ("+ 截图", self.capture_and_match),
            ("+ 截图保存", self.add_capture_step),
            ("+ 条件", self.add_conditional_branch),
            ("+ 图片", self.add_image_step),
            ("|", None),
            ("▲", self.move_step_up), ("▼", self.move_step_down),
            ("✕", self.delete_step), ("清空", self.clear_all_steps),
        ]:
            if cmd is None:
                ttk.Separator(btn_frame, orient="vertical").pack(side=tk.LEFT, fill=tk.Y, padx=4)
            else:
                ttk.Button(btn_frame, text=text, command=cmd).pack(side=tk.LEFT, padx=1)

    def _build_loop_record_ui(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)

        # 循环
        loop_frame = ttk.LabelFrame(frame, text="循环", padding="4")
        loop_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        ttk.Label(loop_frame, text="次数:").pack(side=tk.LEFT, padx=2)
        ttk.Entry(loop_frame, textvariable=self.loop_count, width=6).pack(side=tk.LEFT, padx=2)
        ttk.Checkbutton(loop_frame, text="无限循环", variable=self.loop_infinite,
                         command=self._on_infinite_toggle).pack(side=tk.LEFT, padx=8)

        # 录制
        rec_frame = ttk.LabelFrame(frame, text="录制", padding="4")
        rec_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.record_btn = ttk.Button(rec_frame, text="⏺ 录制", command=self.start_recording, style="Record.TButton")
        self.record_btn.pack(side=tk.LEFT, padx=2)
        self.record_pause_btn = ttk.Button(rec_frame, text="⏸ 暂停(F2)", command=self.toggle_record_pause, state=tk.DISABLED)
        self.record_pause_btn.pack(side=tk.LEFT, padx=2)
        self.record_stop_btn = ttk.Button(rec_frame, text="⏹ 停止(F10)", command=self.stop_recording, state=tk.DISABLED, style="RecordStop.TButton")
        self.record_stop_btn.pack(side=tk.LEFT, padx=2)
        self.record_status = ttk.Label(rec_frame, text="未录制", foreground=self._colors["dim"])
        self.record_status.pack(side=tk.LEFT, padx=8)

    def _build_window_ui(self, parent):
        frame = ttk.LabelFrame(parent, text="窗口绑定", padding="4")
        frame.pack(fill=tk.X, pady=2)

        row1 = ttk.Frame(frame)
        row1.pack(fill=tk.X, pady=2)
        self.window_combo = ttk.Combobox(row1, width=40, state="readonly")
        self.window_combo.pack(side=tk.LEFT, padx=2)
        self.window_combo.bind("<<ComboboxSelected>>", self._on_combo_select)

        for text, cmd in [
            ("确定选择", self.bind_selected_window),
            ("探测子窗口", self.find_child_windows),
            ("清除", self.clear_window_binding),
            ("刷新", self.list_all_windows),
        ]:
            ttk.Button(row1, text=text, command=cmd).pack(side=tk.LEFT, padx=2)

        # 绑定状态
        self.bind_status_label = ttk.Label(row1, text="❌ 未绑定", foreground=self._colors["danger"])
        self.bind_status_label.pack(side=tk.RIGHT, padx=8)

        row2 = ttk.Frame(frame)
        row2.pack(fill=tk.X, pady=2)
        ttk.Checkbutton(row2, text="启用窗口绑定", variable=self.bind_to_window).pack(side=tk.LEFT, padx=4)
        ttk.Separator(row2, orient="vertical").pack(side=tk.LEFT, fill=tk.Y, padx=6)
        ttk.Label(row2, text="点击方式:").pack(side=tk.LEFT, padx=2)
        for text, val in [("PostMessage", "postmessage"), ("SendInput", "sendinput")]:
            ttk.Radiobutton(row2, text=text, variable=self.click_method, value=val).pack(side=tk.LEFT, padx=3)
        ttk.Separator(row2, orient="vertical").pack(side=tk.LEFT, fill=tk.Y, padx=6)
        ttk.Checkbutton(row2, text="Game Mode", variable=self.use_game_mode,
                         command=self._on_game_mode_toggle).pack(side=tk.LEFT, padx=4)

        # 窗口信息
        self.window_info = ttk.Label(frame, text="未选择窗口", foreground=self._colors["dim"])
        self.window_info.pack(fill=tk.X, pady=2)

    def _build_options_ui(self, parent):
        frame = ttk.LabelFrame(parent, text="选项", padding="4")
        frame.pack(fill=tk.X, pady=2)

        row = ttk.Frame(frame)
        row.pack(fill=tk.X)
        ttk.Checkbutton(row, text="随机偏移", variable=self.random_offset_enabled).pack(side=tk.LEFT, padx=2)
        ttk.Entry(row, textvariable=self.random_offset_px, width=3).pack(side=tk.LEFT)
        ttk.Label(row, text="px").pack(side=tk.LEFT, padx=(0, 6))
        ttk.Separator(row, orient="vertical").pack(side=tk.LEFT, fill=tk.Y, padx=4)
        self.show_click_markers = tk.BooleanVar(value=True)
        ttk.Checkbutton(row, text="显示标记", variable=self.show_click_markers).pack(side=tk.LEFT, padx=2)
        ttk.Button(row, text="清除标记", command=self._clear_click_markers).pack(side=tk.LEFT, padx=2)
        ttk.Separator(row, orient="vertical").pack(side=tk.LEFT, fill=tk.Y, padx=4)
        ttk.Checkbutton(row, text="拟人模式", variable=self.human_mode).pack(side=tk.LEFT, padx=2)
        ttk.Label(row, text="波动±").pack(side=tk.LEFT)
        ttk.Entry(row, textvariable=self.wait_variance, width=3).pack(side=tk.LEFT)
        ttk.Label(row, text="%").pack(side=tk.LEFT, padx=(0, 6))
        ttk.Label(row, text="按压").pack(side=tk.LEFT)
        ttk.Entry(row, textvariable=self.press_duration_min, width=3).pack(side=tk.LEFT)
        ttk.Label(row, text="-").pack(side=tk.LEFT)
        ttk.Entry(row, textvariable=self.press_duration_max, width=3).pack(side=tk.LEFT)
        ttk.Label(row, text="ms").pack(side=tk.LEFT)

    def _build_status_ui(self, parent):
        frame = ttk.LabelFrame(parent, text="运行状态", padding="4")
        frame.pack(fill=tk.X, pady=2)
        self.status_label = ttk.Label(frame, text="状态: 已停止")
        self.status_label.pack(side=tk.LEFT, padx=8)
        self.step_label = ttk.Label(frame, text="步骤: -")
        self.step_label.pack(side=tk.LEFT, padx=8)
        self.loop_label = ttk.Label(frame, text="循环: 0")
        self.loop_label.pack(side=tk.LEFT, padx=8)
        self.time_label = ttk.Label(frame, text="用时: 00:00:00")
        self.time_label.pack(side=tk.LEFT, padx=8)
        self.progress_label = ttk.Label(frame, text="", foreground=self._colors["accent"])
        self.progress_label.pack(side=tk.RIGHT, padx=8)

    def _build_control_ui(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=4)
        self.start_btn = ttk.Button(frame, text="▶  开始 (F9)", command=self.start, style="Start.TButton")
        self.start_btn.pack(side=tk.LEFT, padx=6, fill=tk.X, expand=True)
        self.stop_btn = ttk.Button(frame, text="⏹  停止 (F10)", command=self.stop, state=tk.DISABLED, style="Stop.TButton")
        self.stop_btn.pack(side=tk.LEFT, padx=6, fill=tk.X, expand=True)

    def _build_config_ui(self, parent):
        frame = ttk.LabelFrame(parent, text="配置管理", padding="4")
        frame.pack(fill=tk.X, pady=2)
        self.config_name_var = tk.StringVar()
        ttk.Label(frame, text="名称:").pack(side=tk.LEFT, padx=2)
        ttk.Entry(frame, textvariable=self.config_name_var, width=14).pack(side=tk.LEFT, padx=2)
        for text, cmd in [("保存", self.save_config), ("加载", self.load_config),
                          ("删除", self.delete_config), ("列出", self.list_configs)]:
            ttk.Button(frame, text=text, command=cmd).pack(side=tk.LEFT, padx=2)

        ttk.Separator(frame, orient="vertical").pack(side=tk.LEFT, fill=tk.Y, padx=6)
        ttk.Button(frame, text="导出文件", command=self.export_to_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame, text="导入文件", command=self.import_from_file).pack(side=tk.LEFT, padx=2)

    def apply_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # ---- 色彩体系 ----
        BG = "#0D1117"        # 主背景（GitHub Dark）
        BG_CARD = "#161B22"   # 卡片/面板背景
        BG_INPUT = "#21262D"  # 输入框/控件背景
        BORDER = "#30363D"    # 边框
        TEXT = "#E6EDF3"      # 主文字
        TEXT_DIM = "#8B949E"  # 次要文字
        ACCENT = "#58A6FF"    # 强调色（蓝）
        SUCCESS = "#3FB950"   # 成功（绿）
        DANGER = "#F85149"    # 危险（红）
        WARN = "#D29922"      # 警告（黄）
        PURPLE = "#BC8CFF"    # 紫色

        self.root.configure(bg=BG)

        # ---- 全局字体 ----
        FONT = ("Microsoft YaHei UI", 9)
        FONT_BOLD = ("Microsoft YaHei UI", 9, "bold")
        FONT_TITLE = ("Microsoft YaHei UI", 10, "bold")
        FONT_MONO = ("Consolas", 9)

        # ---- Frame ----
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=TEXT, font=FONT)
        style.configure("TButton", background=BG_INPUT, foreground=TEXT, font=FONT,
                        borderwidth=1, relief="flat", padding=(10, 4))
        style.map("TButton",
                  background=[("active", BORDER), ("pressed", ACCENT)],
                  foreground=[("pressed", "#FFF")])

        # ---- LabelFrame ----
        style.configure("TLabelframe", background=BG_CARD, foreground=TEXT,
                        borderwidth=1, relief="flat", bordercolor=BORDER)
        style.configure("TLabelframe.Label", background=BG_CARD, foreground=ACCENT,
                        font=FONT_BOLD)

        # ---- Treeview（步骤列表）----
        style.configure("Treeview", background=BG_INPUT, foreground=TEXT,
                        fieldbackground=BG_INPUT, font=FONT, rowheight=26,
                        borderwidth=0, relief="flat")
        style.configure("Treeview.Heading", background=BG_CARD, foreground=TEXT_DIM,
                        font=FONT_BOLD, borderwidth=0, relief="flat")
        style.map("Treeview",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", "#FFF")])

        # ---- Radiobutton / Checkbutton ----
        style.configure("TRadiobutton", background=BG_CARD, foreground=TEXT, font=FONT)
        style.configure("TCheckbutton", background=BG_CARD, foreground=TEXT, font=FONT)

        # ---- Entry ----
        style.configure("TEntry", fieldbackground=BG_INPUT, foreground=TEXT,
                        borderwidth=1, relief="flat", bordercolor=BORDER, font=FONT)

        # ---- Combobox ----
        style.configure("TCombobox", fieldbackground=BG_INPUT, foreground=TEXT,
                        borderwidth=1, relief="flat", font=FONT)

        # ---- Separator ----
        style.configure("TSeparator", background=BORDER)

        # ---- 特殊按钮样式 ----
        style.configure("Start.TButton", background=SUCCESS, foreground="#FFF",
                        font=FONT_BOLD, padding=(16, 6))
        style.map("Start.TButton",
                  background=[("active", "#2EA043"), ("pressed", "#238636")])

        style.configure("Stop.TButton", background=DANGER, foreground="#FFF",
                        font=FONT_BOLD, padding=(16, 6))
        style.map("Stop.TButton",
                  background=[("active", "#DA3633"), ("pressed", "#B62324")])

        style.configure("Record.TButton", background="#F0883E", foreground="#FFF",
                        font=FONT_BOLD, padding=(10, 4))
        style.map("Record.TButton",
                  background=[("active", "#DB6D28"), ("pressed", "#BD561D")])

        style.configure("RecordStop.TButton", background=DANGER, foreground="#FFF",
                        font=FONT_BOLD, padding=(10, 4))

        # 保存颜色引用供其他方法使用
        self._colors = {
            "bg": BG, "card": BG_CARD, "input": BG_INPUT, "border": BORDER,
            "text": TEXT, "dim": TEXT_DIM, "accent": ACCENT, "success": SUCCESS,
            "danger": DANGER, "warn": WARN, "purple": PURPLE,
        }

    # ==================================================================
    #  热键
    # ==================================================================
    def start_hotkey_listener(self):
        if not PYNPUT_AVAILABLE:
            return

        def on_press(key):
            try:
                if key == kb_listener.Key.f2:
                    self.root.after(0, self.toggle_record_pause)
                elif key == kb_listener.Key.f9:
                    self.root.after(0, self.start)
                elif key == kb_listener.Key.f10:
                    if self.is_recording:
                        self.root.after(0, self.stop_recording)
                    else:
                        self.root.after(0, self.stop)
            except AttributeError:
                pass

        self.hotkey_listener = kb_listener.Listener(on_press=on_press)
        self.hotkey_listener.start()

    # ==================================================================
    #  循环控制
    # ==================================================================
    def _on_infinite_toggle(self):
        if self.loop_infinite.get():
            self.loop_count.set(0)

    # ---- 执行日志 ----

    def _log(self, msg, tag="info"):
        """向执行日志添加一行（线程安全）"""
        def _append():
            self.step_log.config(state=tk.NORMAL)
            self.step_log.insert(tk.END, msg + "\n", tag)
            self.step_log.see(tk.END)
            # 只保留最近 100 行
            lines = int(self.step_log.index("end-1c").split(".")[0])
            if lines > 100:
                self.step_log.delete("1.0", f"{lines - 100}.0")
            self.step_log.config(state=tk.DISABLED)
        self.root.after(0, _append)

    def _clear_log(self):
        def _clear():
            self.step_log.config(state=tk.NORMAL)
            self.step_log.delete("1.0", tk.END)
            self.step_log.config(state=tk.DISABLED)
        self.root.after(0, _clear)

    def _update_progress(self, text):
        """更新右侧进度显示（线程安全）"""
        self.root.after(0, lambda: self.progress_label.config(text=text))

    # ==================================================================
    #  点击标记
    # ==================================================================

    def _show_click_marker(self, x, y):
        """在屏幕坐标 (x, y) 显示带编号的圆圈标记（鼠标穿透，不影响图片识别）"""
        if not self.show_click_markers.get():
            return
        if not WIN32_AVAILABLE:
            return

        self._click_marker_counter += 1
        num = self._click_marker_counter

        r = 22
        size = r * 2 + 4
        ox, oy = x - r - 2, y - r - 2

        win = tk.Toplevel(self.root)
        win.overrideredirect(True)
        win.attributes("-topmost", True)
        win.attributes("-transparentcolor", "#010101")
        win.geometry(f"{size}x{size}+{ox}+{oy}")

        canvas = tk.Canvas(win, width=size, height=size, bg="#010101", highlightthickness=0)
        canvas.pack()

        cx, cy = size // 2, size // 2
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline="#00FF00", width=2)
        canvas.create_text(cx, cy, text=str(num), fill="#00FF00",
                           font=("Arial", 13, "bold"))

        # 设置鼠标穿透
        try:
            win.update_idletasks()
            hwnd = int(win.wm_frame(), 16)
            ex = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex | 0x00000020)
        except Exception:
            pass

        self._click_marker_overlays.append(win)

    def _clear_click_markers(self):
        """清除所有点击标记"""
        for w in self._click_marker_overlays:
            try:
                w.destroy()
            except Exception:
                pass
        self._click_marker_overlays.clear()
        self._click_marker_counter = 0

    # ==================================================================
    #  步骤管理
    # ==================================================================
    def _refresh_step_list(self):
        for item in self.step_tree.get_children():
            self.step_tree.delete(item)
        for i, step in enumerate(self.steps):
            self.step_tree.insert("", tk.END, values=(i + 1, step.action_label(), step.describe()))

    def _get_selected_idx(self):
        sel = self.step_tree.selection()
        if not sel:
            return -1
        return self.step_tree.index(sel[0])

    def add_click_step(self, click_type):
        action = "left_click" if click_type == "left" else "right_click"
        messagebox.showinfo("获取坐标", "3 秒后获取鼠标位置，请把鼠标移到目标位置...")
        self.root.after(3000, lambda: self._capture_and_add_click(action))

    def _capture_and_add_click(self, action):
        if PYAUTOGUI_AVAILABLE:
            x, y = pyautogui.position()
        else:
            x, y = 0, 0
        self.steps.append(MacroStep(action, {"x": x, "y": y}))
        self._refresh_step_list()
        self._show_click_marker(x, y)

    def add_wait_step(self):
        ms = simpledialog.askinteger("等待时间", "请输入等待毫秒数 (10-600000):", minvalue=10, maxvalue=600000)
        if ms:
            self.steps.append(MacroStep("wait", {"duration": ms}))
            self._refresh_step_list()

    def add_key_step(self):
        key = simpledialog.askstring("键盘按键", "请输入按键 (如 enter, space, ctrl+c):")
        if key:
            self.steps.append(MacroStep("key_press", {"key": key.strip()}))
            self._refresh_step_list()

    def add_image_step(self):
        if not CV2_AVAILABLE:
            messagebox.showwarning("警告", "需要安装 opencv-python: pip install opencv-python")
            return
        path = filedialog.askopenfilename(filetypes=[("图片", "*.png;*.jpg;*.jpeg")])
        if not path:
            return
        self._match_image_and_add_step(path)

    def add_conditional_branch(self):
        """添加条件分支步骤"""
        if not CV2_AVAILABLE:
            messagebox.showwarning("警告", "需要安装 opencv-python: pip install opencv-python")
            return
        path = filedialog.askopenfilename(title="选择条件图片", filetypes=[("图片", "*.png;*.jpg;*.jpeg")])
        if not path:
            return
        template = cv2_read_image(path)
        if template is None:
            messagebox.showerror("错误", f"无法读取图片: {path}")
            return

        timeout = simpledialog.askfloat("扫描超时",
                                        "快速扫描超时时间（秒）\n找不到则跳过此分支:",
                                        initialvalue=0.5, minvalue=0.1, maxvalue=5.0)
        if timeout is None:
            timeout = 0.5

        search_region = None
        set_region = messagebox.askyesno("搜索区域", "是否限定搜索区域？\n\n是 → 在屏幕上框选\n否 → 全屏搜索")
        if set_region:
            search_region = self._select_region_on_screen()

        sub_steps = self._collect_sub_steps_dialog()
        if sub_steps is None:
            return

        self.steps.append(MacroStep("conditional_branch", {
            "check_image": path,
            "timeout": timeout,
            "search_region": search_region,
            "sub_steps": sub_steps,
            "else_steps": [],
        }))
        self._refresh_step_list()
        sub_count = len(sub_steps)
        messagebox.showinfo("已添加",
                           f"条件分支步骤已添加\n\n"
                           f"条件图片: {os.path.basename(path)}\n"
                           f"扫描超时: {timeout}秒\n"
                           f"子步骤: {sub_count} 步\n\n"
                           f"执行时快速扫描图片，找到则执行子步骤，否则跳过。")

    def _collect_sub_steps_dialog(self):
        """弹出对话框收集条件分支的子步骤列表。返回 steps list 或 None（取消）。"""
        dialog = tk.Toplevel(self.root)
        dialog.title("编辑子步骤")
        dialog.geometry("460x380")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="条件满足时执行以下步骤:").pack(padx=8, pady=(8, 2))
        ttk.Label(dialog, text="match = 点击识别到的位置  |  也可以截图选点", foreground="gray").pack(padx=8)

        listbox = tk.Listbox(dialog, height=8)
        listbox.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        sub_steps = []

        def refresh_list():
            listbox.delete(0, tk.END)
            for i, s in enumerate(sub_steps):
                a = s["action"]
                p = s["params"]
                if a in ("left_click", "right_click"):
                    x, y = p.get('x', 0), p.get('y', 0)
                    label = f"{i+1}. {'左键' if a=='left_click' else '右键'} ({x},{y})"
                elif a == "wait":
                    label = f"{i+1}. 等待 {p.get('duration',0)}ms"
                elif a == "key_press":
                    label = f"{i+1}. 按键 [{p.get('key','')}]"
                elif a == "image_click":
                    name = os.path.basename(p.get("image", ""))
                    label = f"{i+1}. 识图点击 [{name}]"
                else:
                    label = f"{i+1}. {a}"
                listbox.insert(tk.END, label)

        def add_sub_wait():
            ms = simpledialog.askinteger("子步骤等待", "毫秒数:", initialvalue=1000,
                                         minvalue=10, maxvalue=600000, parent=dialog)
            if ms:
                sub_steps.append({"action": "wait", "params": {"duration": ms}})
                refresh_list()

        def add_sub_key():
            key = simpledialog.askstring("子步骤按键", "按键 (如 enter, space):", parent=dialog)
            if key:
                sub_steps.append({"action": "key_press", "params": {"key": key.strip()}})
                refresh_list()

        def del_sub():
            sel = listbox.curselection()
            if sel:
                sub_steps.pop(sel[0])
                refresh_list()

        def add_sub_click_screen(ctype):
            """截图选点添加点击子步骤"""
            dialog.grab_release()
            dialog.withdraw()
            pos = self._click_point_on_screen()
            dialog.deiconify()
            dialog.grab_set()
            if pos is None:
                return
            action = "left_click" if ctype == "left" else "right_click"
            if pos.get("relative"):
                sub_steps.append({"action": action, "params": {"x": pos["rel_x"], "y": pos["rel_y"], "relative": True}})
            else:
                sub_steps.append({"action": action, "params": {"x": pos["x"], "y": pos["y"]}})
            refresh_list()

        def add_sub_click_match(ctype):
            """match 坐标添加点击子步骤"""
            action = "left_click" if ctype == "left" else "right_click"
            sub_steps.append({"action": action, "params": {"x": "match", "y": "match"}})
            refresh_list()

        def add_sub_image_click():
            """添加识图点击子步骤"""
            if not CV2_AVAILABLE:
                messagebox.showwarning("警告", "需要 opencv-python", parent=dialog)
                return
            path = filedialog.askopenfilename(title="选择图片", filetypes=[("图片", "*.png;*.jpg;*.jpeg")])
            if not path:
                return
            timeout = simpledialog.askinteger("超时", "找不到时等待秒数:", initialvalue=5, minvalue=1, maxvalue=30, parent=dialog)
            if timeout is None:
                timeout = 5
            sub_steps.append({"action": "image_click", "params": {"image": path, "timeout": timeout}})
            refresh_list()

        btn_row = ttk.Frame(dialog)
        btn_row.pack(fill=tk.X, padx=8, pady=4)
        ttk.Button(btn_row, text="截图 左键", command=lambda: add_sub_click_screen("left")).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_row, text="截图 右键", command=lambda: add_sub_click_screen("right")).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_row, text="match 左键", command=lambda: add_sub_click_match("left")).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_row, text="match 右键", command=lambda: add_sub_click_match("right")).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_row, text="+ 等待", command=add_sub_wait).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_row, text="+ 按键", command=add_sub_key).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_row, text="+ 识图", command=add_sub_image_click).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_row, text="删除", command=del_sub).pack(side=tk.LEFT, padx=(12, 2))

        result = {"value": None}

        def on_ok():
            result["value"] = list(sub_steps)  # 空列表 = 自动点击识别位置
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        bottom = ttk.Frame(dialog)
        bottom.pack(fill=tk.X, padx=8, pady=8)
        ttk.Button(bottom, text="确定", command=on_ok).pack(side=tk.RIGHT, padx=4)
        ttk.Button(bottom, text="取消", command=on_cancel).pack(side=tk.RIGHT, padx=4)

        dialog.wait_window()
        return result["value"]

    def _match_image_and_add_step(self, path, scope=None):
        """添加识图点击步骤。scope 有值时直接用作搜索区域，不再询问。"""
        if not CV2_AVAILABLE:
            messagebox.showwarning("警告", "需要安装 opencv-python")
            return
        template = cv2_read_image(path)
        if template is None:
            messagebox.showerror("错误", f"无法读取图片: {path}")
            return

        timeout = simpledialog.askinteger("超时时间", "找不到图片时等待多久（秒）？", initialvalue=10, minvalue=1, maxvalue=120)
        if timeout is None:
            timeout = 10

        # 匹配精度
        confidence = simpledialog.askfloat("匹配精度",
                                           "匹配精度（0.5 ~ 0.99）\n\n"
                                           "0.95+ = 非常严格，几乎完全一致才匹配\n"
                                           "0.85  = 较严格，适合有汉字的图片\n"
                                           "0.70  = 宽松，允许一定差异",
                                           initialvalue=0.90, minvalue=0.50, maxvalue=0.99)
        if confidence is None:
            confidence = 0.90

        # 搜索区域：有 scope 直接用，没有才问
        search_region = None
        if scope:
            search_region = scope
        else:
            set_region = messagebox.askyesno("搜索区域", "是否限定搜索区域？\n\n是 → 在屏幕上框选一个区域\n否 → 全屏搜索")
            if set_region:
                search_region = self._select_region_on_screen()

        # 滚轮搜索配置
        scroll_cfg = self._ask_scroll_on_miss()

        params = {"image": path, "timeout": timeout, "confidence": confidence}
        if search_region:
            params["search_region"] = search_region
        if scroll_cfg:
            params["scroll_on_miss"] = scroll_cfg

        self.steps.append(MacroStep("image_click", params))
        self._refresh_step_list()

        region_info = ""
        if search_region:
            r = search_region
            if r.get("relative"):
                region_info = f"\n搜索区域: (相对 {r['rel_x']},{r['rel_y']}) {r['w']}x{r['h']}"
            else:
                region_info = f"\n搜索区域: ({r['x']},{r['y']}) {r['w']}x{r['h']}"
        scroll_info = ""
        if scroll_cfg:
            sr = scroll_cfg.get("scroll_region", scroll_cfg)
            if sr.get("relative"):
                scroll_info = f"\n滚轮搜索: (相对区域) {scroll_cfg['direction']} x{scroll_cfg['amount']} 最多{scroll_cfg['max_scrolls']}次"
            else:
                scroll_info = f"\n滚轮搜索: {scroll_cfg['direction']} x{scroll_cfg['amount']} 最多{scroll_cfg['max_scrolls']}次"
        messagebox.showinfo("已添加", f"识图点击步骤已添加\n\n图片: {os.path.basename(path)}\n超时: {timeout}秒{region_info}{scroll_info}")

    def _resolve_region(self, region):
        """将区域坐标转为绝对屏幕坐标。如果 region 有 relative=True，根据窗口当前位置计算。"""
        if not region:
            return None
        if not region.get("relative"):
            return region
        # 相对窗口坐标 → 绝对坐标
        hwnd = self.target_hwnd
        if not hwnd or not win32gui.IsWindow(hwnd):
            # 窗口不存在，返回原始坐标（兜底）
            return {"x": region.get("x", 0), "y": region.get("y", 0),
                    "w": region["w"], "h": region["h"]}
        rect = win32gui.GetWindowRect(hwnd)
        wx, wy = rect[0], rect[1]
        return {"x": wx + region["rel_x"], "y": wy + region["rel_y"],
                "w": region["w"], "h": region["h"]}

    def _select_region_on_screen(self):
        """全屏覆盖层，用户拖拽框选区域。
        如果已绑定窗口，自动存为相对窗口坐标（窗口移动时跟随）。
        返回 {x, y, w, h} 或 {rel_x, rel_y, w, h, relative=True} 或 None
        """
        # 先把绑定窗口弹到最前面
        if self._is_bound_window():
            try:
                win32gui.SetForegroundWindow(self.target_hwnd)
                time.sleep(0.2)
            except Exception:
                pass

        self.root.withdraw()
        time.sleep(0.3)

        result = {"region": None}

        overlay = tk.Toplevel()
        overlay.attributes("-fullscreen", True)
        overlay.attributes("-alpha", 0.3)
        overlay.attributes("-topmost", True)
        overlay.overrideredirect(True)
        overlay.configure(bg="gray")
        overlay.focus_force()

        # 判断是否绑定了窗口
        bound_hwnd = self.target_hwnd if self._is_bound_window() else None
        hint = "（跟随窗口移动）" if bound_hwnd else "（固定屏幕坐标）"

        canvas = tk.Canvas(overlay, bg="gray", highlightthickness=0, cursor="cross")
        canvas.pack(fill=tk.BOTH, expand=True)

        # 显示窗口边框提示
        if bound_hwnd:
            try:
                wr = win32gui.GetWindowRect(bound_hwnd)
                canvas.create_rectangle(wr[0], wr[1], wr[2], wr[3],
                                         outline="#FFD700", width=2, dash=(6, 3))
                canvas.create_text((wr[0] + wr[2]) // 2, wr[1] - 15,
                                    text="绑定窗口", fill="#FFD700", font=("Arial", 10))
            except Exception:
                pass

        canvas.create_text(
            overlay.winfo_screenwidth() // 2, 30,
            text=f"拖拽框选搜索区域  |  ESC 取消  {hint}",
            fill="white", font=("Arial", 14))

        state = {"sx": 0, "sy": 0, "rect": None}

        def on_press(e):
            state["sx"], state["sy"] = e.x, e.y
            if state["rect"]:
                canvas.delete(state["rect"])
            state["rect"] = canvas.create_rectangle(e.x, e.y, e.x, e.y,
                                                     outline="#00FF00", width=2, dash=(6, 3))

        def on_drag(e):
            if state["rect"]:
                canvas.coords(state["rect"], state["sx"], state["sy"], e.x, e.y)

        def on_release(e):
            x1, y1 = min(state["sx"], e.x), min(state["sy"], e.y)
            x2, y2 = max(state["sx"], e.x), max(state["sy"], e.y)
            if x2 - x1 < 10 or y2 - y1 < 10:
                overlay.destroy()
                self.root.deiconify()
                return
            w, h = x2 - x1, y2 - y1
            if bound_hwnd:
                # 存为相对窗口坐标
                wr = win32gui.GetWindowRect(bound_hwnd)
                result["region"] = {
                    "rel_x": x1 - wr[0], "rel_y": y1 - wr[1],
                    "w": w, "h": h, "relative": True,
                }
            else:
                result["region"] = {"x": x1, "y": y1, "w": w, "h": h}
            overlay.destroy()
            self.root.deiconify()

        def on_esc(e):
            overlay.destroy()
            self.root.deiconify()

        overlay.bind("<ButtonPress-1>", on_press)
        overlay.bind("<B1-Motion>", on_drag)
        overlay.bind("<ButtonRelease-1>", on_release)
        overlay.bind("<Escape>", on_esc)

        overlay.wait_window()
        return result["region"]

    def _click_point_on_screen(self):
        """全屏覆盖层，用户单击选点。
        绑定窗口时返回相对坐标 dict，否则返回绝对坐标 dict。
        返回 {x, y} 或 {rel_x, rel_y, relative=True} 或 None
        """
        self.root.withdraw()
        time.sleep(0.3)

        result = {"pos": None}

        bound_hwnd = self.target_hwnd if self._is_bound_window() else None
        hint = "（跟随窗口）" if bound_hwnd else ""

        overlay = tk.Toplevel()
        overlay.attributes("-fullscreen", True)
        overlay.attributes("-alpha", 0.3)
        overlay.attributes("-topmost", True)
        overlay.overrideredirect(True)
        overlay.configure(bg="gray")
        overlay.focus_force()

        canvas = tk.Canvas(overlay, bg="gray", highlightthickness=0, cursor="cross")
        canvas.pack(fill=tk.BOTH, expand=True)

        if bound_hwnd:
            try:
                wr = win32gui.GetWindowRect(bound_hwnd)
                canvas.create_rectangle(wr[0], wr[1], wr[2], wr[3],
                                         outline="#FFD700", width=2, dash=(6, 3))
            except Exception:
                pass

        canvas.create_text(
            overlay.winfo_screenwidth() // 2, 30,
            text=f"单击选择滚轮位置  |  ESC 取消  {hint}",
            fill="white", font=("Arial", 14))

        # 十字准星
        crosshair_h = canvas.create_line(0, 0, 0, 0, fill="#00FF00", width=1)
        crosshair_v = canvas.create_line(0, 0, 0, 0, fill="#00FF00", width=1)
        pos_text = canvas.create_text(0, 0, fill="#00FF00", font=("Arial", 10), anchor="nw")

        def on_motion(e):
            sw = overlay.winfo_screenwidth()
            sh = overlay.winfo_screenheight()
            canvas.coords(crosshair_h, 0, e.y, sw, e.y)
            canvas.coords(crosshair_v, e.x, 0, e.x, sh)
            canvas.coords(pos_text, e.x + 10, e.y + 10)
            canvas.itemconfig(pos_text, text=f"({e.x}, {e.y})")

        def on_click(e):
            if bound_hwnd:
                wr = win32gui.GetWindowRect(bound_hwnd)
                result["pos"] = {"rel_x": e.x - wr[0], "rel_y": e.y - wr[1], "relative": True}
            else:
                result["pos"] = {"x": e.x, "y": e.y}
            overlay.destroy()
            self.root.deiconify()

        def on_esc(e):
            overlay.destroy()
            self.root.deiconify()

        canvas.bind("<Motion>", on_motion)
        canvas.bind("<Button-1>", on_click)
        overlay.bind("<Escape>", on_esc)

        overlay.wait_window()
        return result["pos"]

    def _ask_scroll_on_miss(self):
        """询问滚轮搜索配置，返回 dict 或 None。
        流程：框选范围 → 倒计时3秒 → 录制滚轮 → 结束
        """
        enable = messagebox.askyesno("滚轮搜索", "找不到图片时，是否用滚轮滚动页面来搜索？\n\n适合列表/页面中需要滚动才能看到的目标。")
        if not enable:
            return None

        messagebox.showinfo("选择范围", "点击确定后，拖拽框选滚轮滚动的范围\n\n（通常是列表/页面的可滚动区域）")
        region = self._select_region_on_screen()
        if region is None:
            return None

        if not PYNPUT_AVAILABLE:
            messagebox.showwarning("警告", "需要 pynput 来录制滚轮")
            return None

        # 计算范围中心（用于倒计时窗口定位和鼠标初始位置）
        resolved = self._resolve_region(region) if region.get("relative") else region
        cx = resolved["x"] + resolved["w"] // 2
        cy = resolved["y"] + resolved["h"] // 2

        # 移动鼠标到范围中心
        ctypes.windll.user32.SetCursorPos(int(cx), int(cy))

        # 录制滚轮事件
        scroll_events = []

        def on_scroll(x, y, dx, dy):
            scroll_events.append(dy)

        listener = mouse_listener.Listener(on_scroll=on_scroll)
        listener.start()

        # 确保目标窗口在前台
        self._ensure_window_focus()
        time.sleep(0.3)

        # 小浮动倒计时窗口（不遮挡目标，鼠标穿透）
        count_win = tk.Toplevel(self.root)
        count_win.overrideredirect(True)
        count_win.attributes("-topmost", True)
        count_win.attributes("-transparentcolor", "#010101")
        count_win.configure(bg="#010101")

        win_w, win_h = 260, 120
        sx_pos = max(0, int(cx) - win_w // 2)
        sy_pos = max(0, int(cy) - win_h - 50)
        count_win.geometry(f"{win_w}x{win_h}+{sx_pos}+{sy_pos}")

        frame = tk.Frame(count_win, bg="#1a1a2e", bd=2, relief="ridge")
        frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(frame, text="滚轮录制", bg="#1a1a2e", fg="#FFD700",
                                font=("Microsoft YaHei UI", 10, "bold"))
        title_label.pack(pady=(6, 0))

        count_label = tk.Label(frame, text="3", bg="#1a1a2e", fg="#FFFFFF",
                                font=("Arial", 36, "bold"))
        count_label.pack()

        status_label = tk.Label(frame, text="准备...", bg="#1a1a2e", fg="#8B949E",
                                 font=("Microsoft YaHei UI", 9))
        status_label.pack()

        # 设置鼠标穿透
        count_win.update_idletasks()
        hwnd_count = int(count_win.wm_frame(), 16)
        ex = win32gui.GetWindowLong(hwnd_count, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd_count, win32con.GWL_EXSTYLE, ex | 0x00000020)

        # 倒计时 3-2-1
        for i in range(3, 0, -1):
            count_label.config(text=str(i), fg="#FFFFFF")
            status_label.config(text="准备滚动...")
            count_win.update()
            time.sleep(1)

        # 录制中
        count_label.config(text="GO!", fg="#3FB950")
        status_label.config(text="滚动鼠标滚轮！", fg="#3FB950")
        count_win.update()

        # 录制 3 秒
        record_start = time.time()
        while time.time() - record_start < 3:
            remaining = 3 - (time.time() - record_start)
            count = len(scroll_events)
            count_label.config(text=f"{remaining:.1f}s", fg="#FFFFFF")
            status_label.config(text=f"已检测 {count} 次滚动")
            count_win.update()
            time.sleep(0.05)

        count_win.destroy()

        listener.stop()

        if not scroll_events:
            messagebox.showwarning("未检测到", "3秒内未检测到滚轮操作，请重试")
            return None

        # 取最后一次滚动的幅度
        dy = scroll_events[-1]
        direction = "down" if dy < 0 else "up"
        amount = abs(dy)

        max_scrolls = simpledialog.askinteger("最大滚动次数",
                                              f"录制完成！\n\n"
                                              f"方向: {'向下' if direction == 'down' else '向上'}\n"
                                              f"幅度: {amount}\n"
                                              f"共检测到 {len(scroll_events)} 次滚动\n\n"
                                              f"最多滚动几次？",
                                              initialvalue=10, minvalue=1, maxvalue=50)
        if max_scrolls is None:
            max_scrolls = 10

        cfg = {
            "direction": direction,
            "amount": amount,
            "max_scrolls": max_scrolls,
            "scroll_region": region,  # 框选的滚动范围
        }
        return cfg

    def capture_and_match(self):
        """截图 → 保存 → 立即识别"""
        if not PYAUTOGUI_AVAILABLE:
            messagebox.showwarning("警告", "需要安装 pyautogui")
            return
        save_dir = os.path.join(SCRIPT_DIR, "screenshots")
        os.makedirs(save_dir, exist_ok=True)
        # 先问一次范围
        set_scope = messagebox.askyesno("框选范围", "是否先限定截图范围？\n\n是 → 先框选一个大范围\n否 → 全屏拖拽截图")
        scope = None
        if set_scope:
            scope = self._select_region_on_screen()
        messagebox.showinfo("截图", "点击确定后，3 秒内请准备好。\n\n"
                           "按住鼠标左键拖动选择区域，松开完成截图。")
        self.root.after(3000, lambda: self._do_capture(save_dir, scope))

    def add_capture_step(self):
        """截图选择区域 → 保存为文件 → 添加截图保存步骤"""
        if not PYAUTOGUI_AVAILABLE:
            messagebox.showwarning("警告", "需要安装 pyautogui")
            return
        save_dir = os.path.join(SCRIPT_DIR, "screenshots")
        os.makedirs(save_dir, exist_ok=True)
        # 先问一次范围
        set_scope = messagebox.askyesno("框选范围", "是否先限定截图范围？\n\n是 → 先框选一个大范围\n否 → 全屏拖拽截图")
        scope = None
        if set_scope:
            scope = self._select_region_on_screen()
        messagebox.showinfo("截图保存", "点击确定后，3 秒内请准备好。\n\n"
                           "按住鼠标拖动选择区域，松开后截图自动保存。")
        self.root.after(3000, lambda: self._do_capture_save(save_dir, scope))

    def _do_capture_save(self, save_dir, scope=None):
        """执行区域截图，保存并添加截图保存步骤。scope 为预选的搜索区域（可选）。"""
        # 解析为当前绝对坐标（用于界面绘制和约束）
        scope = self._resolve_region(scope) if scope else None

        # 在范围内精确截图
        self.root.withdraw()
        time.sleep(0.3)

        overlay = tk.Toplevel()
        overlay.attributes("-fullscreen", True)
        overlay.attributes("-alpha", 0.3)
        overlay.attributes("-topmost", True)
        overlay.overrideredirect(True)
        overlay.configure(bg="gray")
        overlay.focus_force()

        canvas = tk.Canvas(overlay, bg="gray", highlightthickness=0, cursor="cross")
        canvas.pack(fill=tk.BOTH, expand=True)

        # 显示范围边框
        if scope:
            sx, sy, sw, sh = scope["x"], scope["y"], scope["w"], scope["h"]
            canvas.create_rectangle(sx, sy, sx + sw, sy + sh,
                                     outline="#FFD700", width=3, dash=(8, 4))
            canvas.create_text(
                overlay.winfo_screenwidth() // 2, 30,
                text=f"在黄色范围内拖拽截图  |  ESC 取消",
                fill="white", font=("Arial", 14))
        else:
            canvas.create_text(
                overlay.winfo_screenwidth() // 2, 30,
                text="按住鼠标拖动选择区域  |  ESC 取消",
                fill="white", font=("Arial", 14))

        state = {"sx": 0, "sy": 0, "rect": None}

        def on_press(e):
            state["sx"], state["sy"] = e.x, e.y
            if state["rect"]:
                canvas.delete(state["rect"])
            state["rect"] = canvas.create_rectangle(e.x, e.y, e.x, e.y,
                                                     outline="#00FF00", width=2, dash=(6, 3))

        def on_drag(e):
            if state["rect"]:
                canvas.coords(state["rect"], state["sx"], state["sy"], e.x, e.y)

        def on_release(e):
            x1, y1 = min(state["sx"], e.x), min(state["sy"], e.y)
            x2, y2 = max(state["sx"], e.x), max(state["sy"], e.y)
            if x2 - x1 < 5 or y2 - y1 < 5:
                overlay.destroy()
                self.root.deiconify()
                return

            # 如果有范围限制，裁剪到范围内
            if scope:
                sx, sy, sw, sh = scope["x"], scope["y"], scope["w"], scope["h"]
                x1 = max(x1, sx)
                y1 = max(y1, sy)
                x2 = min(x2, sx + sw)
                y2 = min(y2, sy + sh)
                if x2 - x1 < 5 or y2 - y1 < 5:
                    overlay.destroy()
                    self.root.deiconify()
                    return

            overlay.destroy()

            shot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
            ts = time.strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(save_dir, f"capture_{ts}.png")
            shot.save(filepath)

            self.root.deiconify()
            self.steps.append(MacroStep("capture_save", {
                "path": filepath,
                "region": {"x": x1, "y": y1, "w": x2 - x1, "h": y2 - y1},
            }))
            self._refresh_step_list()
            messagebox.showinfo("截图保存", f"已保存: {filepath}\n"
                               f"区域: ({x1},{y1}) - ({x2},{y2})  {x2-x1}x{y2-y1}")

        def on_esc(e):
            overlay.destroy()
            self.root.deiconify()

        overlay.bind("<ButtonPress-1>", on_press)
        overlay.bind("<B1-Motion>", on_drag)
        overlay.bind("<ButtonRelease-1>", on_release)
        overlay.bind("<Escape>", on_esc)

    def _do_capture(self, save_dir, scope=None):
        """执行区域截图（截图+识别用）。scope 为预选的搜索区域（可选）。"""
        scope = self._resolve_region(scope) if scope else None

        # 精确截图
        self.root.withdraw()
        time.sleep(0.3)

        overlay = tk.Toplevel()
        overlay.attributes("-fullscreen", True)
        overlay.attributes("-alpha", 0.3)
        overlay.attributes("-topmost", True)
        overlay.overrideredirect(True)
        overlay.configure(bg="gray")
        overlay.focus_force()

        canvas = tk.Canvas(overlay, bg="gray", highlightthickness=0, cursor="cross")
        canvas.pack(fill=tk.BOTH, expand=True)

        if scope:
            sx, sy, sw, sh = scope["x"], scope["y"], scope["w"], scope["h"]
            canvas.create_rectangle(sx, sy, sx + sw, sy + sh,
                                     outline="#FFD700", width=3, dash=(8, 4))
            canvas.create_text(
                overlay.winfo_screenwidth() // 2, 30,
                text="在黄色范围内拖拽截图  |  ESC 取消",
                fill="white", font=("Arial", 14))
        else:
            canvas.create_text(
                overlay.winfo_screenwidth() // 2, 30,
                text="按住鼠标拖动选择区域  |  ESC 取消",
                fill="white", font=("Arial", 14))

        state = {"sx": 0, "sy": 0, "rect": None}

        def on_press(e):
            state["sx"], state["sy"] = e.x, e.y
            if state["rect"]:
                canvas.delete(state["rect"])
            state["rect"] = canvas.create_rectangle(e.x, e.y, e.x, e.y,
                                                     outline="#00FF00", width=2, dash=(6, 3))

        def on_drag(e):
            if state["rect"]:
                canvas.coords(state["rect"], state["sx"], state["sy"], e.x, e.y)

        def on_release(e):
            x1, y1 = min(state["sx"], e.x), min(state["sy"], e.y)
            x2, y2 = max(state["sx"], e.x), max(state["sy"], e.y)
            if x2 - x1 < 5 or y2 - y1 < 5:
                overlay.destroy()
                self.root.deiconify()
                return
            overlay.destroy()

            shot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
            ts = time.strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(save_dir, f"capture_{ts}.png")
            shot.save(filepath)

            self.root.deiconify()
            messagebox.showinfo("截图完成",
                               f"已保存: {filepath}\n"
                               f"区域: ({x1},{y1}) - ({x2},{y2})  {x2-x1}x{y2-y1}")
            self._match_image_and_add_step(filepath, scope)

        def on_esc(e):
            overlay.destroy()
            self.root.deiconify()

        overlay.bind("<ButtonPress-1>", on_press)
        overlay.bind("<B1-Motion>", on_drag)
        overlay.bind("<ButtonRelease-1>", on_release)
        overlay.bind("<Escape>", on_esc)

    def move_step_up(self):
        idx = self._get_selected_idx()
        if idx > 0:
            self.steps[idx], self.steps[idx - 1] = self.steps[idx - 1], self.steps[idx]
            self._refresh_step_list()
            self.step_tree.selection_set(self.step_tree.get_children()[idx - 1])

    def move_step_down(self):
        idx = self._get_selected_idx()
        if 0 <= idx < len(self.steps) - 1:
            self.steps[idx], self.steps[idx + 1] = self.steps[idx + 1], self.steps[idx]
            self._refresh_step_list()
            self.step_tree.selection_set(self.step_tree.get_children()[idx + 1])

    def delete_step(self):
        idx = self._get_selected_idx()
        if idx >= 0:
            self.steps.pop(idx)
            self._refresh_step_list()

    def clear_all_steps(self):
        if self.steps and messagebox.askyesno("确认", "清空所有步骤？"):
            self.steps.clear()
            self._refresh_step_list()

    # ---- 右键菜单 & 编辑 ----

    def _show_step_context_menu(self, event):
        idx = self._get_selected_idx()
        if idx < 0:
            return
        # 先选中右键点击的行
        item = self.step_tree.identify_row(event.y)
        if item:
            self.step_tree.selection_set(item)
            idx = self.step_tree.index(item)

        menu = tk.Menu(self.root, tearoff=0, bg="#2D2D2D", fg="#FFFFFF",
                       activebackground=self._colors["accent"], activeforeground="#FFFFFF")
        menu.add_command(label="编辑步骤", command=lambda: self._edit_step(idx))
        menu.add_separator()
        # run_once 快捷开关
        step = self.steps[idx]
        ro = step.params.get("run_once", False)
        ro_label = "☑ 仅首次执行（点击取消）" if ro else "☐ 设为仅首次执行"
        menu.add_command(label=ro_label, command=lambda: self._toggle_run_once(idx))
        # image_click 滚轮搜索快捷开关
        if step.action == "image_click":
            scroll_cfg = step.params.get("scroll_on_miss")
            if scroll_cfg:
                scroll_label = f"☑ 滚轮搜索（点击取消）"
                menu.add_command(label=scroll_label, command=lambda: self._toggle_scroll_on_miss(idx))
            else:
                menu.add_command(label="☐ 设置滚轮搜索", command=lambda: self._toggle_scroll_on_miss(idx))
        # 搜索区域快捷开关（image_click 和 conditional_branch）
        if step.action in ("image_click", "conditional_branch"):
            region = step.params.get("search_region")
            if region:
                if region.get("relative"):
                    r = region
                    menu.add_command(label=f"☑ 搜索区域 (相对 {r['rel_x']},{r['rel_y']}) {r['w']}x{r['h']}（点击取消）",
                                     command=lambda: self._toggle_search_region(idx))
                else:
                    r = region
                    menu.add_command(label=f"☑ 搜索区域 ({r['x']},{r['y']}) {r['w']}x{r['h']}（点击取消）",
                                     command=lambda: self._toggle_search_region(idx))
            else:
                menu.add_command(label="☐ 框选搜索区域", command=lambda: self._toggle_search_region(idx))
        menu.add_separator()
        menu.add_command(label="在前面插入等待", command=lambda: self._insert_wait(idx, before=True))
        menu.add_command(label="在后面插入等待", command=lambda: self._insert_wait(idx, before=False))
        menu.add_command(label="在前面插入按键", command=lambda: self._insert_key(idx, before=True))
        menu.add_command(label="在后面插入条件分支", command=lambda: self._insert_conditional_after(idx))
        # 执行后等待
        pd = step.params.get("post_delay", 0)
        if pd > 0:
            menu.add_command(label=f"☑ 执行后等待 {pd}ms（点击取消）",
                             command=lambda: self._set_post_delay(idx))
        else:
            menu.add_command(label="设置执行后等待",
                             command=lambda: self._set_post_delay(idx))
        menu.add_separator()
        menu.add_command(label="复制步骤", command=lambda: self._copy_step(idx))
        menu.add_command(label="删除步骤", command=lambda: self._delete_at(idx))
        menu.add_separator()
        menu.add_command(label="上移", command=lambda: (self.step_tree.selection_set(self.step_tree.get_children()[idx]), self.move_step_up()))
        menu.add_command(label="下移", command=lambda: (self.step_tree.selection_set(self.step_tree.get_children()[idx]), self.move_step_down()))
        menu.tk_popup(event.x_root, event.y_root)

    def _on_step_double_click(self, event):
        idx = self._get_selected_idx()
        if idx >= 0:
            self._edit_step(idx)

    def _edit_step(self, idx):
        """编辑步骤参数"""
        if idx < 0 or idx >= len(self.steps):
            return
        step = self.steps[idx]

        if step.action in ("left_click", "right_click"):
            x = simpledialog.askinteger("编辑坐标", "X:", initialvalue=step.params.get("x", 0))
            if x is None:
                return
            y = simpledialog.askinteger("编辑坐标", "Y:", initialvalue=step.params.get("y", 0))
            if y is None:
                return
            step.params["x"] = x
            step.params["y"] = y
            messagebox.showinfo("已修改", f"坐标已改为 ({x}, {y})")

        elif step.action == "wait":
            ms = simpledialog.askinteger("编辑等待", "毫秒数:", initialvalue=step.params.get("duration", 1000),
                                        minvalue=10, maxvalue=600000)
            if ms is None:
                return
            step.params["duration"] = ms
            messagebox.showinfo("已修改", f"等待时间已改为 {ms} ms")

        elif step.action == "key_press":
            key = simpledialog.askstring("编辑按键", "按键:", initialvalue=step.params.get("key", ""))
            if key is None:
                return
            step.params["key"] = key.strip()
            messagebox.showinfo("已修改", f"按键已改为 {step.params['key']}")

        elif step.action == "image_click":
            timeout = simpledialog.askinteger("编辑超时", "超时秒数:",
                                             initialvalue=step.params.get("timeout", 10),
                                             minvalue=1, maxvalue=120)
            if timeout is None:
                return
            step.params["timeout"] = timeout
            # 匹配精度
            conf = simpledialog.askfloat("匹配精度", "精度 (0.50~0.99):",
                                          initialvalue=step.params.get("confidence", 0.90),
                                          minvalue=0.50, maxvalue=0.99)
            if conf is not None:
                step.params["confidence"] = conf
            # 滚轮搜索配置
            has_scroll = step.params.get("scroll_on_miss") is not None
            if has_scroll:
                modify = messagebox.askyesno("滚轮搜索", "当前已启用滚轮搜索\n\n是否修改配置？\n（选否则取消滚轮搜索）")
                if modify:
                    cfg = self._ask_scroll_on_miss()
                    if cfg:
                        step.params["scroll_on_miss"] = cfg
                else:
                    step.params["scroll_on_miss"] = None
            else:
                cfg = self._ask_scroll_on_miss()
                if cfg:
                    step.params["scroll_on_miss"] = cfg
            messagebox.showinfo("已修改", f"超时已改为 {timeout} 秒")

        elif step.action == "capture_save":
            path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG 图片", "*.png"), ("所有文件", "*.*")],
                initialfile=os.path.basename(step.params.get("path", "capture.png")),
                title="修改保存路径")
            if path:
                step.params["path"] = path
                messagebox.showinfo("已修改", f"保存路径已改为:\n{path}")

        elif step.action == "conditional_branch":
            timeout = simpledialog.askfloat("编辑扫描超时", "超时秒数:",
                                            initialvalue=step.params.get("timeout", 0.5),
                                            minvalue=0.1, maxvalue=5.0)
            if timeout is None:
                return
            step.params["timeout"] = timeout
            messagebox.showinfo("已修改", f"扫描超时已改为 {timeout} 秒")

        self._refresh_step_list()

    def _insert_wait(self, idx, before=True):
        """在指定步骤前/后插入等待"""
        ms = simpledialog.askinteger("插入等待", "毫秒数:", initialvalue=1000, minvalue=10, maxvalue=600000)
        if ms is None:
            return
        pos = idx if before else idx + 1
        self.steps.insert(pos, MacroStep("wait", {"duration": ms}))
        self._refresh_step_list()

    def _insert_key(self, idx, before=True):
        """在指定步骤前插入按键"""
        key = simpledialog.askstring("插入按键", "按键 (如 enter, space, ctrl+c):")
        if key is None:
            return
        pos = idx if before else idx + 1
        self.steps.insert(pos, MacroStep("key_press", {"key": key.strip()}))
        self._refresh_step_list()

    def _copy_step(self, idx):
        """复制步骤"""
        if idx < 0 or idx >= len(self.steps):
            return
        src = self.steps[idx]
        self.steps.insert(idx + 1, MacroStep(src.action, dict(src.params)))
        self._refresh_step_list()

    def _delete_at(self, idx):
        """删除指定步骤"""
        if 0 <= idx < len(self.steps):
            self.steps.pop(idx)
            self._refresh_step_list()

    def _toggle_run_once(self, idx):
        """切换仅首次执行状态"""
        if 0 <= idx < len(self.steps):
            step = self.steps[idx]
            step.params["run_once"] = not step.params.get("run_once", False)
            self._refresh_step_list()

    def _toggle_scroll_on_miss(self, idx):
        """切换滚轮搜索配置"""
        if 0 <= idx < len(self.steps):
            step = self.steps[idx]
            if step.params.get("scroll_on_miss"):
                step.params["scroll_on_miss"] = None
            else:
                cfg = self._ask_scroll_on_miss()
                if cfg:
                    step.params["scroll_on_miss"] = cfg
            self._refresh_step_list()

    def _toggle_search_region(self, idx):
        """切换搜索区域"""
        if 0 <= idx < len(self.steps):
            step = self.steps[idx]
            if step.params.get("search_region"):
                step.params["search_region"] = None
            else:
                region = self._select_region_on_screen()
                if region:
                    step.params["search_region"] = region
            self._refresh_step_list()

    def _set_post_delay(self, idx):
        """设置/取消执行后等待"""
        if 0 <= idx < len(self.steps):
            step = self.steps[idx]
            current = step.params.get("post_delay", 0)
            if current > 0:
                step.params["post_delay"] = 0
            else:
                ms = simpledialog.askinteger("执行后等待", "步骤执行完后等待多久（毫秒）？\n\n设为 0 取消等待",
                                             initialvalue=1000, minvalue=0, maxvalue=600000)
                if ms and ms > 0:
                    step.params["post_delay"] = ms
            self._refresh_step_list()

    def _insert_conditional_after(self, idx):
        """在指定步骤后面插入条件分支"""
        if not CV2_AVAILABLE:
            messagebox.showwarning("警告", "需要安装 opencv-python: pip install opencv-python")
            return
        path = filedialog.askopenfilename(title="选择条件图片", filetypes=[("图片", "*.png;*.jpg;*.jpeg")])
        if not path:
            return
        template = cv2_read_image(path)
        if template is None:
            messagebox.showerror("错误", f"无法读取图片: {path}")
            return
        timeout = simpledialog.askfloat("扫描超时",
                                        "快速扫描超时时间（秒）\n找不到则跳过此分支:",
                                        initialvalue=0.5, minvalue=0.1, maxvalue=5.0)
        if timeout is None:
            timeout = 0.5
        search_region = None
        set_region = messagebox.askyesno("搜索区域", "是否限定搜索区域？\n\n是 → 在屏幕上框选\n否 → 全屏搜索")
        if set_region:
            search_region = self._select_region_on_screen()
        sub_steps = self._collect_sub_steps_dialog()
        if sub_steps is None:
            return
        self.steps.insert(idx + 1, MacroStep("conditional_branch", {
            "check_image": path,
            "timeout": timeout,
            "search_region": search_region,
            "sub_steps": sub_steps,
            "else_steps": [],
        }))
        self._refresh_step_list()

    # ==================================================================
    #  录制
    # ==================================================================
    def start_recording(self):
        if not PYNPUT_AVAILABLE:
            messagebox.showwarning("警告", "需要安装 pynput: pip install pynput")
            return
        if self.is_recording:
            return

        self.record_btn.config(state=tk.DISABLED)
        self._start_countdown(3)

    def _start_countdown(self, seconds):
        """录制前倒计时"""
        if seconds > 0:
            self.record_status.config(text=f"倒计时 {seconds} 秒...", foreground=self._colors["warn"])
            self.root.after(1000, lambda: self._start_countdown(seconds - 1))
            return

        # 倒计时结束，正式开始录制
        self.is_recording = True
        self.is_record_paused = False
        self._record_events = []
        self._record_pause_offset = 0
        self._record_start_time = time.time()
        self.record_status.config(text="● 录制中...", foreground=self._colors["danger"])
        self.record_btn.config(state=tk.DISABLED)
        self.record_pause_btn.config(state=tk.NORMAL)
        self.record_stop_btn.config(state=tk.NORMAL)

        def on_click(x, y, button, pressed):
            if not (pressed and self.is_recording):
                return
            if self.is_record_paused:
                return
            btn = "left" if button == mouse_listener.Button.left else "right"
            t = time.time() - self._record_start_time - self._record_pause_offset
            self._record_events.append({
                "type": "click", "x": x, "y": y, "button": btn, "time": t,
            })

        def on_press(key):
            if not self.is_recording:
                return
            # F2 和 F10 由主热键处理，这里跳过
            if key in (kb_listener.Key.f2, kb_listener.Key.f10):
                return
            if self.is_record_paused:
                return
            try:
                k = key.char if hasattr(key, "char") and key.char else str(key).replace("Key.", "")
            except AttributeError:
                k = str(key).replace("Key.", "")
            t = time.time() - self._record_start_time - self._record_pause_offset
            self._record_events.append({
                "type": "key", "key": k, "time": t,
            })

        self._mouse_listener = mouse_listener.Listener(on_click=on_click)
        self._mouse_listener.start()
        self._kb_listener_recorder = kb_listener.Listener(on_press=on_press)
        self._kb_listener_recorder.start()

    def toggle_record_pause(self):
        """F2 暂停/恢复录制"""
        if not self.is_recording:
            return
        if self.is_record_paused:
            # 恢复
            self._record_pause_offset += time.time() - self._record_pause_point
            self.is_record_paused = False
            self.record_status.config(text="● 录制中...", foreground=self._colors["danger"])
            self.record_pause_btn.config(text="⏸ 暂停(F2)")
        else:
            # 暂停
            self._record_pause_point = time.time()
            self.is_record_paused = True
            self.record_status.config(text="⏸ 已暂停", foreground=self._colors["warn"])
            self.record_pause_btn.config(text="▶ 恢复(F2)")

    def stop_recording(self):
        if not self.is_recording:
            return
        self.is_recording = False
        self.is_record_paused = False

        if self._mouse_listener:
            self._mouse_listener.stop()
        if self._kb_listener_recorder:
            self._kb_listener_recorder.stop()

        self.record_status.config(text="录制完成", foreground=self._colors["success"])
        self.record_btn.config(state=tk.NORMAL)
        self.record_pause_btn.config(state=tk.DISABLED, text="⏸ 暂停(F2)")
        self.record_stop_btn.config(state=tk.DISABLED)

        # 生成步骤
        if not self._record_events:
            messagebox.showinfo("录制", "未录制到任何操作")
            return

        new_steps = []
        prev_time = 0
        for evt in self._record_events:
            # 插入等待
            gap = int((evt["time"] - prev_time) * 1000)
            if gap > 50:  # 小于 50ms 的不加等待
                new_steps.append(MacroStep("wait", {"duration": gap}))

            if evt["type"] == "click":
                action = "left_click" if evt["button"] == "left" else "right_click"
                new_steps.append(MacroStep(action, {"x": evt["x"], "y": evt["y"]}))
            elif evt["type"] == "key":
                new_steps.append(MacroStep("key_press", {"key": evt["key"]}))

            prev_time = evt["time"]

        self.steps.extend(new_steps)
        self._refresh_step_list()

        # 显示录制点击位置的标记
        for step in new_steps:
            if step.action in ("left_click", "right_click"):
                self._show_click_marker(step.params.get("x", 0), step.params.get("y", 0))

        messagebox.showinfo("录制完成", f"录制了 {len(self._record_events)} 个操作，"
                           f"生成 {len(new_steps)} 个步骤")

    # ==================================================================
    #  窗口绑定
    # ==================================================================
    def list_all_windows(self):
        if not WIN32_AVAILABLE:
            return
        self._window_map.clear()
        windows = []

        def enum_handler(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    display = f"{title[:55]}  (hwnd={hwnd})"
                    self._window_map[display] = hwnd
                    windows.append(display)

        win32gui.EnumWindows(enum_handler, None)
        windows.sort()
        self.window_combo["values"] = windows

    def _on_combo_select(self, event=None):
        display = self.window_combo.get()
        hwnd = self._window_map.get(display)
        if hwnd:
            self.pending_hwnd = hwnd
            self._show_window_info(hwnd, "待确认")

    def bind_selected_window(self):
        hwnd = self.pending_hwnd
        if not hwnd:
            # 尝试从下拉框获取
            display = self.window_combo.get()
            hwnd = self._window_map.get(display)
        if not hwnd:
            messagebox.showwarning("警告", "请先选择一个窗口")
            return
        if not win32gui.IsWindow(hwnd):
            messagebox.showwarning("警告", "窗口已不存在")
            return

        self.target_hwnd = hwnd
        self.pending_hwnd = hwnd
        title = win32gui.GetWindowText(hwnd)
        self.bind_status_label.config(text=f"✅ 已绑定: {title[:30]}", foreground=self._colors["success"])
        self._show_window_info(hwnd, "已绑定")
        self._highlight_rect(hwnd)

    def find_child_windows(self):
        if not WIN32_AVAILABLE:
            return
        parent = self.pending_hwnd or self.target_hwnd
        if not parent:
            messagebox.showwarning("警告", "请先选择一个窗口")
            return

        children = []
        child = win32gui.FindWindowEx(parent, 0, None, None)
        while child:
            title = win32gui.GetWindowText(child)
            cls = win32gui.GetClassName(child)
            rect = win32gui.GetWindowRect(child)
            visible = win32gui.IsWindowVisible(child)
            children.append({"hwnd": child, "title": title, "class": cls,
                           "size": (rect[2] - rect[0], rect[3] - rect[1]), "visible": visible})
            child = win32gui.FindWindowEx(parent, child, None, None)

        if not children:
            messagebox.showinfo("结果", "未找到子窗口（模拟器可能是单窗口渲染）")
            return

        # 让用户选择子窗口
        items = []
        for c in children:
            vis = "✓" if c["visible"] else "✗"
            items.append(f"[{vis}] {c['class'][:20]} {c['size'][0]}x{c['size'][1]} (hwnd={c['hwnd']})")

        choice = simpledialog.askstring("选择子窗口",
                                        f"找到 {len(children)} 个子窗口，请输入编号:\n\n" +
                                        "\n".join(f"  {i}: {item}" for i, item in enumerate(items)))
        if choice is not None:
            try:
                idx = int(choice.strip())
                if 0 <= idx < len(children):
                    self.target_hwnd = children[idx]["hwnd"]
                    self.bind_status_label.config(
                        text=f"✅ 子窗口: {children[idx]['class'][:20]}",
                        foreground=self._colors["success"])
            except (ValueError, IndexError):
                pass

    def _show_window_info(self, hwnd, status):
        try:
            title = win32gui.GetWindowText(hwnd)
            cls = win32gui.GetClassName(hwnd)
            rect = win32gui.GetWindowRect(hwnd)
            w, h = rect[2] - rect[0], rect[3] - rect[1]
            self.window_info.config(
                text=f"[{status}] {title[:40]}  class={cls}  {w}x{h}  hwnd={hwnd}")
        except Exception:
            pass

    def _highlight_rect(self, hwnd):
        try:
            rect = win32gui.GetWindowRect(hwnd)
            x1, y1, x2, y2 = rect
            border = 6  # 边框厚度

            # 创建一个只覆盖目标窗口边框的透明窗口（不是全屏）
            hl = tk.Toplevel(self.root)
            hl.geometry(f"{x2 - x1 + border * 2}x{y2 - y1 + border * 2}+{x1 - border}+{y1 - border}")
            hl.attributes("-topmost", True)
            hl.attributes("-transparentcolor", "white")
            hl.overrideredirect(True)
            hl.configure(bg="white")

            canvas = tk.Canvas(hl, bg="white", highlightthickness=0,
                              width=x2 - x1 + border * 2, height=y2 - y1 + border * 2)
            canvas.pack()
            # 画绿色虚线边框
            canvas.create_rectangle(border, border,
                                   x2 - x1 + border, y2 - y1 + border,
                                   outline="#00FF00", width=3, dash=(8, 4))

            # 设置 WS_EX_TRANSPARENT 让鼠标穿透
            hl.update_idletasks()
            hwnd_hl = int(hl.wm_frame(), 16)
            ex_style = win32gui.GetWindowLong(hwnd_hl, win32con.GWL_EXSTYLE)
            win32gui.SetWindowLong(hwnd_hl, win32con.GWL_EXSTYLE,
                                   ex_style | 0x00000020)  # WS_EX_TRANSPARENT

            self.highlight_rect = hl
            hl.after(3000, lambda: (hl.destroy(), setattr(self, "highlight_rect", None)))
        except Exception:
            pass

    def clear_window_binding(self):
        self.target_hwnd = None
        self.pending_hwnd = None
        self.bind_status_label.config(text="❌ 未绑定", foreground=self._colors["danger"])
        self.window_info.config(text="未选择窗口")

    def _on_game_mode_toggle(self):
        if self.use_game_mode.get() and not INTERCEPTION_AVAILABLE:
            messagebox.showinfo("Game Mode",
                               "Interception 驱动未安装，将使用 SendInput 回退。\n\n"
                               "如需更好的游戏兼容性，安装 Interception 驱动:\n"
                               "https://github.com/oblitum/interception")

    # ==================================================================
    #  点击执行
    # ==================================================================

    def _human_move_to(self, target_x, target_y):
        """拟人鼠标移动：贝塞尔弧线从当前位置滑到目标"""
        if not PYAUTOGUI_AVAILABLE:
            return
        cur_x, cur_y = pyautogui.position()
        dist = ((target_x - cur_x) ** 2 + (target_y - cur_y) ** 2) ** 0.5
        if dist < 5:
            return  # 距离太近不需要轨迹

        # 随机控制点（在中点附近偏移，形成弧线）
        mid_x = (cur_x + target_x) / 2 + random.randint(-int(dist * 0.3), int(dist * 0.3))
        mid_y = (cur_y + target_y) / 2 + random.randint(-int(dist * 0.3), int(dist * 0.3))

        # 步数根据距离调整
        steps = max(10, min(30, int(dist / 20)))

        for i in range(1, steps + 1):
            t = i / steps
            # 二次贝塞尔曲线
            px = (1 - t) ** 2 * cur_x + 2 * (1 - t) * t * mid_x + t ** 2 * target_x
            py = (1 - t) ** 2 * cur_y + 2 * (1 - t) * t * mid_y + t ** 2 * target_y
            ctypes.windll.user32.SetCursorPos(int(px), int(py))
            # 速度：中间快、两头慢
            speed = 0.008 + 0.012 * abs(t - 0.5)
            time.sleep(speed + random.uniform(0, 0.005))

    def _random_press_duration(self):
        """拟人按压时长：随机 30-120ms"""
        lo = max(10, self.press_duration_min.get())
        hi = max(lo + 10, self.press_duration_max.get())
        return random.randint(lo, hi) / 1000.0

    def _is_bound_window(self):
        """是否绑定了有效窗口"""
        return (self.bind_to_window.get() and self.target_hwnd
                and win32gui.IsWindow(self.target_hwnd))

    def _resolve_scroll_point(self, scroll_cfg):
        """解析滚轮配置中的坐标，返回绝对 (sx, sy)。"""
        scroll_region = scroll_cfg.get("scroll_region")
        if scroll_region:
            sr = self._resolve_region(scroll_region) if scroll_region.get("relative") else scroll_region
            return sr["x"] + sr["w"] // 2, sr["y"] + sr["h"] // 2
        if scroll_cfg.get("relative"):
            hwnd = self.target_hwnd
            if hwnd and win32gui.IsWindow(hwnd):
                wr = win32gui.GetWindowRect(hwnd)
                return wr[0] + scroll_cfg.get("rel_x", 0), wr[1] + scroll_cfg.get("rel_y", 0)
            return scroll_cfg.get("rel_x", 0), scroll_cfg.get("rel_y", 0)
        return scroll_cfg.get("x", 0), scroll_cfg.get("y", 0)

    def _random_click_in_match(self, match_x, match_y, tpl_w, tpl_h):
        """在匹配区域内随机取点（留20%边距），并应用随机偏移。返回 (ax, ay)。"""
        margin_x = max(2, int(tpl_w * 0.2))
        margin_y = max(2, int(tpl_h * 0.2))
        cx = match_x + random.randint(margin_x, tpl_w - margin_x)
        cy = match_y + random.randint(margin_y, tpl_h - margin_y)
        if self.random_offset_enabled.get():
            offset = self.random_offset_px.get()
            cx += random.randint(-offset, offset)
            cy += random.randint(-offset, offset)
        return cx, cy

    def _ensure_window_focus(self):
        """确保目标窗口在前台"""
        if self.bind_to_window.get() and self.target_hwnd:
            if not win32gui.IsWindow(self.target_hwnd):
                return False
            try:
                # 检查是否已在前台
                fg = win32gui.GetForegroundWindow()
                if fg != self.target_hwnd:
                    win32gui.SetForegroundWindow(self.target_hwnd)
                    time.sleep(0.05)
            except Exception:
                pass
        return True

    def _perform_click(self, x, y, click_type, retry=2):
        # 确保窗口在前台
        if not self._ensure_window_focus():
            return

        # 拟人鼠标轨迹（仅非 PostMessage 方式）
        if self.human_mode.get() and self.click_method.get() != "postmessage":
            self._human_move_to(x, y)

        # 执行点击
        if self.use_game_mode.get():
            self._game_click(x, y, click_type)
        elif self.click_method.get() == "sendinput":
            self._send_input_click(x, y, click_type)
        else:
            self._postmessage_click(x, y, click_type)

    def _game_click(self, x, y, click_type):
        """Game Mode: Interception → mouse_event → SendInput → pyautogui"""
        if INTERCEPTION_AVAILABLE:
            try:
                self._interception_click(x, y, click_type)
                return
            except Exception:
                pass
        # mouse_event 回退
        try:
            user32 = ctypes.windll.user32
            w = user32.GetSystemMetrics(0)
            h = user32.GetSystemMetrics(1)
            dx = int((x / w) * 65535)
            dy = int((y / h) * 65535)
            user32.mouse_event(MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, dx, dy, 0, 0)
            time.sleep(0.02)
            if click_type in ("left", "double"):
                user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                time.sleep(0.01)
                user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                if click_type == "double":
                    time.sleep(0.05)
                    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                    time.sleep(0.01)
                    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            elif click_type == "right":
                user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                time.sleep(0.01)
                user32.mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
            return
        except Exception:
            pass
        self._send_input_click(x, y, click_type)

    def _interception_click(self, x, y, click_type):
        ctx = interception.lib.interception_create_context()
        interception.lib.interception_set_filter(ctx, interception.is_mouse,
                                                  interception.INTERCEPTION_FILTER_MOUSE_ALL)
        dev = interception.lib.interception_wait(ctx)
        user32 = ctypes.windll.user32
        w = user32.GetSystemMetrics(0)
        h = user32.GetSystemMetrics(1)
        ix = int((x / w) * 65535)
        iy = int((y / h) * 65535)

        stroke = interception.MouseStroke()
        stroke.state = interception.INTERCEPTION_MOUSE_MOVE
        stroke.x, stroke.y = ix, iy
        interception.lib.interception_send(ctx, dev, ctypes.byref(stroke), 1)
        time.sleep(random.uniform(0.003, 0.01))

        if click_type in ("left", "double"):
            stroke.state = interception.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
            interception.lib.interception_send(ctx, dev, ctypes.byref(stroke), 1)
            time.sleep(random.uniform(0.03, 0.08))
            stroke.state = interception.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
            interception.lib.interception_send(ctx, dev, ctypes.byref(stroke), 1)
            if click_type == "double":
                time.sleep(0.05)
                stroke.state = interception.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
                interception.lib.interception_send(ctx, dev, ctypes.byref(stroke), 1)
                time.sleep(0.02)
                stroke.state = interception.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
                interception.lib.interception_send(ctx, dev, ctypes.byref(stroke), 1)
        elif click_type == "right":
            stroke.state = interception.INTERCEPTION_MOUSE_RIGHT_BUTTON_DOWN
            interception.lib.interception_send(ctx, dev, ctypes.byref(stroke), 1)
            time.sleep(0.02)
            stroke.state = interception.INTERCEPTION_MOUSE_RIGHT_BUTTON_UP
            interception.lib.interception_send(ctx, dev, ctypes.byref(stroke), 1)

        interception.lib.interception_destroy_context(ctx)

    def _send_input_click(self, x, y, click_type):
        if self.bind_to_window.get() and self.target_hwnd:
            if not win32gui.IsWindow(self.target_hwnd):
                return
            win32gui.SetForegroundWindow(self.target_hwnd)
            time.sleep(0.02)

        if self.human_mode.get():
            # 拟人模式：分开发送按下和松开，中间加随机延迟
            _send_input_array([_make_move_input(x, y)])
            flags = {
                "left": (MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP),
                "right": (MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP),
            }
            down_f, up_f = flags.get(click_type, flags["left"])
            down = SENDINPUT()
            down.type = INPUT_MOUSE
            down.mi.dwFlags = down_f
            _send_input_array([down])
            time.sleep(self._random_press_duration())
            up = SENDINPUT()
            up.type = INPUT_MOUSE
            up.mi.dwFlags = up_f
            _send_input_array([up])
        else:
            inputs = [_make_move_input(x, y)]
            inputs.extend(_make_button_inputs(click_type))
            _send_input_array(inputs)

    def _postmessage_click(self, x, y, click_type):
        if not self.bind_to_window.get() or not self.target_hwnd:
            self._fallback_click(x, y, click_type)
            return
        if not win32gui.IsWindow(self.target_hwnd):
            return

        rect = win32gui.GetWindowRect(self.target_hwnd)
        cx, cy = x - rect[0], y - rect[1]
        if cx < 0 or cy < 0:
            self._fallback_click(x, y, click_type)
            return

        lParam = win32api.MAKELONG(cx, cy)
        if click_type in ("left", "double"):
            win32api.PostMessage(self.target_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
            time.sleep(0.01)
            win32api.PostMessage(self.target_hwnd, win32con.WM_LBUTTONUP, 0, lParam)
            if click_type == "double":
                time.sleep(0.05)
                win32api.PostMessage(self.target_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
                time.sleep(0.01)
                win32api.PostMessage(self.target_hwnd, win32con.WM_LBUTTONUP, 0, lParam)
        elif click_type == "right":
            win32api.PostMessage(self.target_hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lParam)
            time.sleep(0.01)
            win32api.PostMessage(self.target_hwnd, win32con.WM_RBUTTONUP, 0, lParam)

    def _fallback_click(self, x, y, click_type):
        if PYAUTOGUI_AVAILABLE:
            if click_type == "double":
                pyautogui.doubleClick(x, y)
            elif click_type == "right":
                pyautogui.click(x, y, button="right")
            else:
                pyautogui.click(x, y)

    # ==================================================================
    #  Worker 线程
    # ==================================================================
    def _match_template(self, template, search_region=None, confidence=0.8):
        """在屏幕（或指定区域）上查找模板图片。

        Returns: (found, match_x, match_y) — 找到时返回匹配区域左上角的全屏坐标。
        """
        try:
            resolved = self._resolve_region(search_region) if search_region else None
            if resolved:
                rx, ry = resolved["x"], resolved["y"]
                rw, rh = resolved["w"], resolved["h"]
                screenshot = pyautogui.screenshot(region=(rx, ry, rw, rh))
                screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(result)
                if max_val >= confidence:
                    return True, rx + max_loc[0], ry + max_loc[1]
            else:
                screenshot = pyautogui.screenshot()
                screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(result)
                if max_val >= confidence:
                    return True, max_loc[0], max_loc[1]
        except Exception:
            pass
        return False, 0, 0

    def _execute_image_click(self, step, step_num, total):
        """识图点击：循环查找图片 → 找不到时滚轮搜索 → 找到后点击 → 等待生效 → 进入下一步"""
        if not CV2_AVAILABLE or not PYAUTOGUI_AVAILABLE:
            self._log(f"  步骤{step_num}: 缺少 opencv/pyautogui，跳过", "fail")
            return
        image_path = step.params.get("image", "")
        timeout = step.params.get("timeout", 10)
        search_region = step.params.get("search_region")
        scroll_cfg = step.params.get("scroll_on_miss")
        confidence = step.params.get("confidence", 0.90)
        name = os.path.basename(image_path)
        template = cv2_read_image(image_path)
        if template is None:
            self._log(f"  步骤{step_num}: 无法读取图片 {name}", "fail")
            return

        tpl_h, tpl_w = template.shape[:2]
        # 预解析搜索区域（避免循环内重复解析）
        resolved_region = self._resolve_region(search_region) if search_region else None
        deadline = time.time() + timeout
        start_time = time.time()
        attempt = 0
        scrolled = False
        max_scrolls = scroll_cfg.get("max_scrolls", 10) if scroll_cfg else 0

        self._log(f"  步骤{step_num}: 识别中 [{name}] 精度{confidence:.0%}...", "running")

        while not self.stop_event.is_set() and time.time() < deadline:
            attempt += 1
            elapsed = time.time() - start_time
            self._update_progress(f"识别中: {elapsed:.1f}s / {timeout}s (第{attempt}次)")

            found, match_x, match_y = self._match_template(template, resolved_region, confidence)
            if not found:
                # 找不到 → 滚轮搜索（连续滚完所有次数，再截图检测）
                if scroll_cfg and not scrolled:
                    scrolled = True
                    amount = scroll_cfg.get("amount", 3)
                    direction = scroll_cfg.get("direction", "down")
                    clicks = amount if direction == "up" else -amount
                    sx, sy = self._resolve_scroll_point(scroll_cfg)

                    self._ensure_window_focus()
                    ctypes.windll.user32.SetCursorPos(int(sx), int(sy))
                    time.sleep(0.3)

                    # 连续滚动 max_scrolls 次
                    wheel_delta = clicks * 120
                    inp = SENDINPUT()
                    inp.type = INPUT_MOUSE
                    inp.mi.dwFlags = MOUSEEVENTF_WHEEL
                    inp.mi.mouseData = ctypes.c_ulong(wheel_delta & 0xFFFFFFFF)
                    for s in range(max_scrolls):
                        if self.stop_event.is_set():
                            break
                        self._log(f"  步骤{step_num}: 滚轮搜索 ({sx},{sy}) {direction} x{amount} [{s+1}/{max_scrolls}]", "warn")
                        _send_input_array([inp])
                        time.sleep(0.3)

                    # 滚完，移走鼠标，等一下让页面稳定
                    ctypes.windll.user32.SetCursorPos(0, 0)
                    time.sleep(0.5)
                    self._log(f"  步骤{step_num}: 滚轮搜索完成，重新识别...", "running")
                else:
                    time.sleep(0.5)
                continue

            # 在匹配区域内随机取点并点击
            cx, cy = self._random_click_in_match(match_x, match_y, tpl_w, tpl_h)
            self._update_progress("")
            self._log(f"  步骤{step_num}: 识别到! {elapsed:.1f}s 第{attempt}次", "success")

            # 二次确认：等 0.3s 后再截图验证图片还在
            time.sleep(0.3)
            found2, _, _ = self._match_template(template, resolved_region, confidence)
            if not found2:
                self._log(f"  步骤{step_num}: 图片已消失（界面切换中），重新识别...", "warn")
                continue

            # 二次确认通过，执行点击
            self._ensure_window_focus()
            # 计算随机偏移
            ax, ay = cx, cy
            if self.random_offset_enabled.get():
                offset = self.random_offset_px.get()
                ax = cx + random.randint(-offset, offset)
                ay = cy + random.randint(-offset, offset)
                self._log(f"  步骤{step_num}: 点击 识别({cx},{cy}) → 实际({ax},{ay})", "running")
            else:
                self._log(f"  步骤{step_num}: 点击 ({cx},{cy})...", "running")
            self._perform_click(ax, ay, "left")

            # 等待点击生效：检测图片是否消失
            click_confirmed = False
            for wait_i in range(6):  # 最多等 3 秒
                time.sleep(0.5)
                found3, _, _ = self._match_template(template, resolved_region, confidence)
                if not found3:
                    click_confirmed = True
                    break

            if click_confirmed:
                self._log(f"  步骤{step_num}: 点击成功 ✓ 界面已响应", "success")
            else:
                self._log(f"  步骤{step_num}: 点击已发送（图片仍在，可能需等待）", "warn")

            self._update_progress("")
            self._log(f"  步骤{step_num}: 执行下一步 →", "info")
            return

        elapsed = time.time() - start_time
        self._update_progress("")
        self._log(f"  步骤{step_num}: 未识别 ({elapsed:.1f}s {attempt}次尝试)", "fail")
        self._log(f"  步骤{step_num}: 执行下一步 →", "info")

    def _execute_conditional_branch(self, step, step_num, total):
        """条件分支：快速扫描图片 → 找到则执行子步骤 → 否则跳过"""
        if not CV2_AVAILABLE or not PYAUTOGUI_AVAILABLE:
            self._log(f"  步骤{step_num}: 缺少 opencv/pyautogui，跳过条件分支", "fail")
            return

        check_image = step.params.get("check_image", "")
        timeout = step.params.get("timeout", 0.5)
        search_region = step.params.get("search_region")
        sub_steps = step.params.get("sub_steps", [])
        confidence = step.params.get("confidence", 0.80)
        name = os.path.basename(check_image)

        template = cv2_read_image(check_image)
        if template is None:
            self._log(f"  步骤{step_num}: 条件分支 无法读取图片 [{name}]", "fail")
            return

        tpl_h, tpl_w = template.shape[:2]
        self._log(f"  步骤{step_num}: 条件检查 [{name}]...", "running")

        found, match_x, match_y = False, 0, 0
        deadline = time.time() + timeout
        while not self.stop_event.is_set() and time.time() < deadline:
            found, match_x, match_y = self._match_template(template, search_region, confidence)
            if found:
                break
            time.sleep(0.1)

        if not found:
            self._log(f"  步骤{step_num}: 条件不满足 [{name}] → 跳过", "info")
            self._log(f"  步骤{step_num}: 执行下一步 →", "info")
            return

        # 计算识别位置中心（全屏坐标）
        match_cx = match_x + tpl_w // 2
        match_cy = match_y + tpl_h // 2
        self._log(f"  步骤{step_num}: 条件满足 [{name}] → 执行子步骤", "success")

        # 没配子步骤时，自动点击识别位置
        if not sub_steps:
            cx, cy = self._random_click_in_match(match_x, match_y, tpl_w, tpl_h)
            self._ensure_window_focus()
            self._perform_click(cx, cy, "left")
            self._log(f"  步骤{step_num}: 点击识别位置 ({cx},{cy}) ✓", "success")
            self._log(f"  步骤{step_num}: 条件分支执行完成 →", "info")
            return

        for sub_idx, sub in enumerate(sub_steps):
            if self.stop_event.is_set():
                break
            sub_action = sub.get("action", "")
            sub_params = sub.get("params", {})
            sub_label = sub_idx + 1

            # 解析坐标：match / 相对窗口 / 绝对
            sx = sub_params.get("x", 0)
            sy = sub_params.get("y", 0)
            if sub_params.get("relative"):
                hwnd = self.target_hwnd
                if hwnd and win32gui.IsWindow(hwnd):
                    wr = win32gui.GetWindowRect(hwnd)
                    sx = wr[0] + sx
                    sy = wr[1] + sy
            if sx == "match":
                sx = match_cx
            if sy == "match":
                sy = match_cy

            self._log(f"  步骤{step_num}.{sub_label}: {sub_action}", "running")

            if sub_action in ("left_click", "right_click"):
                click_type = "left" if sub_action == "left_click" else "right"
                ax, ay = sx, sy
                if self.random_offset_enabled.get():
                    offset = self.random_offset_px.get()
                    ax = sx + random.randint(-offset, offset)
                    ay = sy + random.randint(-offset, offset)
                self._ensure_window_focus()
                self._perform_click(ax, ay, click_type)
                self._log(f"  步骤{step_num}.{sub_label}: 点击 ({sx},{sy}) ✓", "success")

            elif sub_action == "wait":
                duration = sub_params.get("duration", 0)
                if self.human_mode.get():
                    variance = self.wait_variance.get() / 100.0
                    lo = int(duration * (1 - variance))
                    hi = int(duration * (1 + variance))
                    duration = random.randint(max(10, lo), max(20, hi))
                self._log(f"  步骤{step_num}.{sub_label}: 等待 {duration}ms", "warn")
                wait_deadline = time.time() + duration / 1000.0
                while time.time() < wait_deadline and not self.stop_event.is_set():
                    time.sleep(0.1)
                self._log(f"  步骤{step_num}.{sub_label}: 等待完成 ✓", "success")

            elif sub_action == "key_press":
                key_str = sub_params.get("key", "")
                if self.use_game_mode.get():
                    self._send_key_scancode(key_str)
                else:
                    parts = key_str.split("+")
                    if len(parts) > 1 and PYAUTOGUI_AVAILABLE:
                        pyautogui.hotkey(*parts)
                    elif PYAUTOGUI_AVAILABLE:
                        pyautogui.press(key_str)
                self._log(f"  步骤{step_num}.{sub_label}: 按键 [{key_str}] ✓", "success")

            elif sub_action == "image_click":
                # 子步骤识图点击
                sub_step = MacroStep("image_click", sub_params)
                self._execute_image_click(sub_step, f"{step_num}.{sub_label}", total)

        self._log(f"  步骤{step_num}: 条件分支执行完成 →", "info")

    def _execute_step(self, step, step_num, total):
        if step.action in ("left_click", "right_click"):
            x = step.params.get("x", 0)
            y = step.params.get("y", 0)
            click_type = "left" if step.action == "left_click" else "right"
            label = "左键点击" if click_type == "left" else "右键点击"

            # 计算随机偏移并显示实际坐标
            ax, ay = x, y
            if self.random_offset_enabled.get():
                offset = self.random_offset_px.get()
                ax = x + random.randint(-offset, offset)
                ay = y + random.randint(-offset, offset)
                self._log(f"  步骤{step_num}: {label} 配置({x},{y}) → 实际({ax},{ay})", "running")
            else:
                self._log(f"  步骤{step_num}: {label} ({x},{y})", "running")

            self._perform_click(ax, ay, click_type)
            self._log(f"  步骤{step_num}: 点击成功 ✓", "success")
            self._log(f"  步骤{step_num}: 执行下一步 →", "info")

        elif step.action == "image_click":
            self._execute_image_click(step, step_num, total)

        elif step.action == "capture_save":
            if not PYAUTOGUI_AVAILABLE:
                self._log(f"  步骤{step_num}: 缺少 pyautogui，跳过截图", "fail")
            else:
                region = step.params.get("region", {})
                rx, ry = region.get("x", 0), region.get("y", 0)
                rw, rh = region.get("w", 0), region.get("h", 0)
                save_path = step.params.get("path", "")
                self._log(f"  步骤{step_num}: 截图保存 ({rx},{ry}) {rw}x{rh}", "running")
                try:
                    shot = pyautogui.screenshot(region=(rx, ry, rw, rh))
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    shot.save(save_path)
                    self._log(f"  步骤{step_num}: 已保存 {os.path.basename(save_path)} ✓", "success")
                except Exception as ex:
                    self._log(f"  步骤{step_num}: 截图失败 {ex}", "fail")
            self._log(f"  步骤{step_num}: 执行下一步 →", "info")

        elif step.action == "wait":
            duration = step.params.get("duration", 0)
            if self.human_mode.get():
                variance = self.wait_variance.get() / 100.0
                lo = int(duration * (1 - variance))
                hi = int(duration * (1 + variance))
                duration = random.randint(max(10, lo), max(20, hi))
            self._log(f"  步骤{step_num}: 等待中 {duration}ms", "warn")
            total_sec = duration / 1000.0
            deadline = time.time() + total_sec
            while time.time() < deadline and not self.stop_event.is_set():
                elapsed = total_sec - (deadline - time.time())
                remaining = max(0, deadline - time.time())
                self._update_progress(f"等待中: {elapsed:.1f}s / {total_sec:.1f}s")
                time.sleep(0.1)
            self._update_progress("")
            self._log(f"  步骤{step_num}: 等待完成 {total_sec:.1f}s ✓", "success")
            self._log(f"  步骤{step_num}: 执行下一步 →", "info")

        elif step.action == "key_press":
            key_str = step.params.get("key", "")
            self._log(f"  步骤{step_num}: 按键 [{key_str}]", "running")
            if self.bind_to_window.get() and self.target_hwnd:
                if win32gui.IsWindow(self.target_hwnd):
                    win32gui.SetForegroundWindow(self.target_hwnd)
                    time.sleep(0.03)
            if self.use_game_mode.get():
                self._send_key_scancode(key_str)
            else:
                parts = key_str.split("+")
                if len(parts) > 1 and PYAUTOGUI_AVAILABLE:
                    pyautogui.hotkey(*parts)
                elif PYAUTOGUI_AVAILABLE:
                    pyautogui.press(key_str)
            self._log(f"  步骤{step_num}: 按键完成 ✓", "success")
            self._log(f"  步骤{step_num}: 执行下一步 →", "info")

        elif step.action == "conditional_branch":
            self._execute_conditional_branch(step, step_num, total)

    def _send_key_scancode(self, key_str):
        user32 = ctypes.windll.user32
        parts = key_str.lower().split("+")
        scancodes = []
        for p in parts:
            sc = _VK_TO_SCANCODE.get(p.strip())
            if sc:
                scancodes.append(sc)
        if not scancodes:
            if PYAUTOGUI_AVAILABLE:
                pyautogui.press(key_str)
            return
        for sc in scancodes:
            user32.keybd_event(0, sc, KEYEVENTF_SCANCODE, 0)
            time.sleep(random.uniform(0.01, 0.03))
        for sc in reversed(scancodes):
            user32.keybd_event(0, sc, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0)
            time.sleep(random.uniform(0.005, 0.02))

    def _worker(self):
        try:
            snapshot = list(self.steps)
            total = len(snapshot)
            loop_limit = self.loop_count.get()
            infinite = self.loop_infinite.get()
            loop_idx = 0

            self._clear_log()
            self._log(f"开始执行 ({total} 个步骤)", "info")

            while not self.stop_event.is_set():
                if not infinite and loop_idx >= loop_limit:
                    break

                with self._lock:
                    self.current_loop = loop_idx
                self.root.after(0, lambda v=loop_idx: self.loop_label.config(text=f"循环: {v + 1}"))

                if infinite or loop_limit > 1:
                    self._log(f"━━━ 第 {loop_idx + 1} 轮 ━━━", "warn")

                for i, step in enumerate(snapshot):
                    if self.stop_event.is_set():
                        break
                    # run_once: 第二轮及之后跳过
                    if loop_idx > 0 and step.params.get("run_once"):
                        self._log(f"  步骤{i + 1}: 跳过（仅首次执行）", "info")
                        continue
                    with self._lock:
                        self.current_step_idx = i
                    self.root.after(0, lambda v=i: self.step_label.config(text=f"步骤: {v + 1}/{total}"))
                    self._execute_step(step, i + 1, total)
                    # 执行后等待
                    post_delay = step.params.get("post_delay", 0)
                    if post_delay > 0:
                        self._log(f"  步骤{i + 1}: 等待 {post_delay}ms", "warn")
                        deadline = time.time() + post_delay / 1000.0
                        while time.time() < deadline and not self.stop_event.is_set():
                            time.sleep(0.1)

                loop_idx += 1

            self._log("执行完成", "success")

            self.root.after(0, self._on_finished)
        except Exception as e:
            self.root.after(0, lambda e=e: self._on_error(str(e)))

    def _on_finished(self):
        self._reset_ui()

    def _on_error(self, msg):
        messagebox.showerror("错误", f"执行出错: {msg}")
        self._reset_ui()

    def _reset_ui(self):
        self.is_running = False
        self.status_label.config(text="状态: 已停止")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def start(self):
        if self.is_running:
            return
        if not self.steps:
            messagebox.showwarning("警告", "请先添加步骤")
            return

        self._clear_click_markers()
        self.is_running = True
        self.start_time = time.time()
        self.stop_event.clear()
        self.status_label.config(text="● 运行中")
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)

        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
        self._update_timer()

    def stop(self):
        if not self.is_running:
            return
        self.is_running = False
        self.stop_event.set()
        if self.worker_thread:
            self.worker_thread.join(timeout=1)
        self._reset_ui()

    def _update_timer(self):
        if self.is_running and self.start_time:
            elapsed = int(time.time() - self.start_time)
            h, m, s = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
            self.time_label.config(text=f"用时: {h:02d}:{m:02d}:{s:02d}")
            self.root.after(1000, self._update_timer)

    # ==================================================================
    #  配置管理
    # ==================================================================
    def load_all_configs(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self.configs = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.configs = {}

    def save_all_configs(self):
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.configs, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {e}")
            return False

    def get_current_config(self):
        return {
            "loop_count": self.loop_count.get(),
            "loop_infinite": self.loop_infinite.get(),
            "random_offset": self.random_offset_enabled.get(),
            "random_offset_px": self.random_offset_px.get(),
            "human_mode": self.human_mode.get(),
            "wait_variance": self.wait_variance.get(),
            "press_duration_min": self.press_duration_min.get(),
            "press_duration_max": self.press_duration_max.get(),
            "steps": [s.to_dict() for s in self.steps],
        }

    def set_config(self, cfg):
        self.loop_count.set(cfg.get("loop_count", 1))
        self.loop_infinite.set(cfg.get("loop_infinite", False))
        self.random_offset_enabled.set(cfg.get("random_offset", False))
        self.random_offset_px.set(cfg.get("random_offset_px", 3))
        self.human_mode.set(cfg.get("human_mode", False))
        self.wait_variance.set(cfg.get("wait_variance", 30))
        self.press_duration_min.set(cfg.get("press_duration_min", 30))
        self.press_duration_max.set(cfg.get("press_duration_max", 120))
        self.steps = [MacroStep.from_dict(d) for d in cfg.get("steps", [])]
        self._refresh_step_list()

    def save_config(self):
        name = self.config_name_var.get().strip()
        if not name:
            messagebox.showwarning("警告", "请输入配置名称")
            return
        self.configs[name] = self.get_current_config()
        if self.save_all_configs():
            messagebox.showinfo("成功", f"配置 '{name}' 已保存")

    def load_config(self):
        name = self.config_name_var.get().strip()
        if not name:
            messagebox.showwarning("警告", "请输入配置名称")
            return
        if name in self.configs:
            self._fix_image_paths(self.configs[name])
            self.set_config(self.configs[name])
            messagebox.showinfo("成功", f"配置 '{name}' 已加载")
        else:
            messagebox.showwarning("警告", f"配置 '{name}' 不存在")

    def delete_config(self):
        name = self.config_name_var.get().strip()
        if name in self.configs:
            del self.configs[name]
            self.save_all_configs()
            messagebox.showinfo("成功", f"配置 '{name}' 已删除")

    def list_configs(self):
        if not self.configs:
            messagebox.showinfo("配置列表", "暂无保存的配置")
            return
        lines = []
        for name, cfg in self.configs.items():
            step_count = len(cfg.get("steps", []))
            loop = "无限" if cfg.get("loop_infinite") else cfg.get("loop_count", 1)
            lines.append(f"  {name}: {step_count} 步骤, {loop} 循环")
        messagebox.showinfo("配置列表", "\n".join(lines))

    # ---- 文件导入/导出 ----

    def export_to_file(self):
        """导出当前步骤到文件"""
        if not self.steps:
            messagebox.showwarning("警告", "没有步骤可导出")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")],
            initialfile="我的宏步骤.json",
            title="导出步骤"
        )
        if not path:
            return
        data = self.get_current_config()
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("导出成功",
                               f"已保存到:\n{path}\n\n"
                               f"步骤数: {len(self.steps)}\n"
                               f"循环: {'无限' if data['loop_infinite'] else data['loop_count']} 次")
        except Exception as e:
            messagebox.showerror("导出失败", str(e))

    def _fix_image_paths(self, data):
        """修复导入配置中的图片路径（文件存在但路径不匹配时自动修正）"""
        screenshots_dir = os.path.join(SCRIPT_DIR, "screenshots")
        for step_data in data.get("steps", []):
            params = step_data.get("params", {})
            self._fix_single_path(params, "image", screenshots_dir)
            self._fix_single_path(params, "check_image", screenshots_dir)
            # 子步骤里的图片路径
            for sub in params.get("sub_steps", []):
                self._fix_single_path(sub.get("params", {}), "image", screenshots_dir)

    def _fix_single_path(self, params, key, screenshots_dir):
        """修复单个图片路径字段"""
        old_path = params.get(key, "")
        if not old_path or not old_path.lower().endswith((".png", ".jpg", ".jpeg")):
            return
        # 原路径存在，不用修
        if os.path.exists(old_path):
            return
        filename = os.path.basename(old_path)
        # 尝试1: screenshots 目录下
        candidate = os.path.join(screenshots_dir, filename)
        if os.path.exists(candidate):
            params[key] = candidate
            return
        # 尝试2: 脚本目录下
        candidate = os.path.join(SCRIPT_DIR, filename)
        if os.path.exists(candidate):
            params[key] = candidate

    def import_from_file(self):
        """从文件导入步骤"""
        path = filedialog.askopenfilename(
            filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")],
            title="导入步骤"
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # 修复图片路径
            self._fix_image_paths(data)
            self.set_config(data)
            step_count = len(data.get("steps", []))
            messagebox.showinfo("导入成功",
                               f"已从文件加载:\n{path}\n\n"
                               f"步骤数: {step_count}\n"
                               f"循环: {'无限' if data.get('loop_infinite') else data.get('loop_count', 1)} 次")
        except json.JSONDecodeError:
            messagebox.showerror("导入失败", "文件格式错误，不是有效的 JSON")
        except Exception as e:
            messagebox.showerror("导入失败", str(e))


# ===========================================================================
# 入口
# ===========================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)

    def on_closing():
        app.stop()
        if app.hotkey_listener:
            app.hotkey_listener.stop()
        if app.is_recording:
            app.stop_recording()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
