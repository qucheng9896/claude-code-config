import ctypes
import time

# 测试 SendInput 点击
def test_sendinput_click(x, y):
    user32 = ctypes.windll.user32
    
    INPUT_MOUSE = 0
    MOUSEEVENTF_ABSOLUTE = 0x8000
    MOUSEEVENTF_MOVE = 0x0001
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    
    dx = int((x / screen_width) * 65535)
    dy = int((y / screen_height) * 65535)
    
    class MOUSEINPUT(ctypes.Structure):
        _fields_ = [
            ("dx", ctypes.c_long),
            ("dy", ctypes.c_long),
            ("mouseData", ctypes.c_ulong),
            ("dwFlags", ctypes.c_ulong),
            ("time", ctypes.c_ulong),
            ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
        ]
    
    class INPUT(ctypes.Structure):
        class _INPUT_UNION(ctypes.Union):
            _fields_ = [
                ("mi", MOUSEINPUT),
                ("ki", ctypes.c_ulong * 6),
                ("hi", ctypes.c_ulong * 2)
            ]
        _anonymous_ = ("u",)
        _fields_ = [
            ("type", ctypes.c_uint),
            ("u", _INPUT_UNION)
        ]
    
    inputs = []
    
    # 移动
    move_input = INPUT()
    move_input.type = INPUT_MOUSE
    move_input.u.mi.dx = dx
    move_input.u.mi.dy = dy
    move_input.u.mi.mouseData = 0
    move_input.u.mi.dwFlags = MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE
    move_input.u.mi.time = 0
    move_input.u.mi.dwExtraInfo = None
    inputs.append(move_input)
    
    # 按下
    down_input = INPUT()
    down_input.type = INPUT_MOUSE
    down_input.u.mi.dwFlags = MOUSEEVENTF_LEFTDOWN
    inputs.append(down_input)
    
    # 释放
    up_input = INPUT()
    up_input.type = INPUT_MOUSE
    up_input.u.mi.dwFlags = MOUSEEVENTF_LEFTUP
    inputs.append(up_input)
    
    input_array = (INPUT * len(inputs))(*inputs)
    result = user32.SendInput(len(inputs), ctypes.byref(input_array), ctypes.sizeof(INPUT))
    print(f"SendInput 结果: {result}")

if __name__ == "__main__":
    print("3秒后点击坐标 (500, 500)...")
    time.sleep(3)
    test_sendinput_click(500, 500)
    print("点击完成")