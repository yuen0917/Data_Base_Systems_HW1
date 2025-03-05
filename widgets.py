import tkinter as tk
from tkinter import messagebox
from constants import COLORS

class RoundedEntry(tk.Canvas):
    def __init__(self, master=None, width=200, height=35, radius=10, validate_phone=False, **kwargs):
        # 設定背景色與主視窗相同
        super().__init__(master, width=width, height=height,
                        highlightthickness=0,  # 移除邊框
                        bg=COLORS['bg_dark'],  # 設定與主背景相同的顏色
                        **kwargs)

        self.radius = radius
        self.validate_phone = validate_phone

        # 創建圓角矩形背景
        self.rect = self.create_rounded_rect(0, 0, width, height, radius,
                                           fill=COLORS['bg_medium'],  # 使用較深的背景色
                                           outline=COLORS['bg_medium'])  # outline 設定與 fill 相同

        # 創建輸入框
        vcmd = (self.register(self._validate_phone), '%P') if validate_phone else None
        self.entry = tk.Entry(self,
                            bg=COLORS['bg_medium'],  # 使用較深的背景色
                            fg=COLORS['text'],
                            font=('Microsoft JhengHei UI', 10),
                            bd=0,
                            highlightthickness=0,
                            validate='key',
                            validatecommand=vcmd,
                            readonlybackground=COLORS['bg_medium'])  # 設定唯讀時的背景色

        # 放置輸入框
        self.entry_window = self.create_window(width/2, height/2,
                                             window=self.entry,
                                             width=width-20)

        # 綁定事件
        self.entry.bind('<FocusIn>', self.on_focus_in)
        self.entry.bind('<FocusOut>', self.on_focus_out)

    def create_rounded_rect(self, x1, y1, x2, y2, radius, fill, outline):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, fill=fill, outline=outline)

    def _validate_phone(self, new_value):
        if new_value == "":  # 允許空值
            return True
        # 只允許數字
        if all(c in '0123456789' for c in new_value):
            return True
        messagebox.showwarning("警告", "電話號碼只能包含數字！")
        return False

    def on_focus_in(self, e):
        if self.entry['state'] != 'readonly':  # 只在非唯讀狀態時改變外框
            self.itemconfig(self.rect, outline=COLORS['accent'])

    def on_focus_out(self, e):
        self.itemconfig(self.rect, outline=COLORS['bg_medium'])  # 改回與填充色相同

    def get(self):
        return self.entry.get()

    def set(self, value):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)

class RoundedButton(tk.Canvas):
    def __init__(self, master=None, text="", command=None, radius=10,
                 btnforeground=COLORS['text'],
                 btnbackground=COLORS['bg_light'],
                 hover_color=COLORS['accent'],
                 width=120, height=35, **kwargs):
        # 設定背景色與主視窗相同
        super().__init__(master, width=width, height=height,
                        highlightthickness=0,  # 移除邊框
                        bg=COLORS['bg_dark'],  # 設定與主背景相同的顏色
                        **kwargs)

        self.radius = radius
        self.btnbackground = btnbackground
        self.hover_color = hover_color
        self.command = command

        # 創建圓角矩形
        self.rect = self.create_rounded_rect(0, 0, width, height, radius,
                                           fill=btnbackground,
                                           outline=btnbackground)  # outline 設定與 fill 相同

        # 創建文字
        self.text = self.create_text(width/2, height/2, text=text,
                                   fill=btnforeground,
                                   font=('Microsoft JhengHei UI', 10))

        # 綁定事件
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_click)
        self.bind('<ButtonRelease-1>', self.on_release)

    def create_rounded_rect(self, x1, y1, x2, y2, radius, fill, outline):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, fill=fill, outline=outline)

    def on_enter(self, e):
        self.itemconfig(self.rect, fill=self.hover_color)

    def on_leave(self, e):
        self.itemconfig(self.rect, fill=self.btnbackground)

    def on_click(self, e):
        self.itemconfig(self.rect, fill=COLORS['bg_dark'])

    def on_release(self, e):
        self.itemconfig(self.rect, fill=self.btnbackground)
        if self.command:
            self.command()