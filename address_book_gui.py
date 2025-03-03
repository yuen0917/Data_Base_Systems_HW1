import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from typing import Dict, List

# 顏色主題
COLORS = {
    'bg_dark': '#0D1B2A',     # 最深的藍色作為背景
    'bg_medium': '#1B263B',   # 深靛藍作為次要背景
    'bg_light': '#415A77',    # 中藍色作為亮一點的元素
    'text': '#E0E1DD',        # 淺灰色作為主要文字
    'text_gray': '#778DA9',   # 淺藍色作為次要文字
    'accent': '#415A77',      # 使用中藍色作為強調色
    'accent_hover': '#778DA9', # 使用淺藍色作為懸停效果
    'warning': '#FF6B6B',     # 保持原有的警告色
    'success': '#4CAF50',     # 保持原有的成功色
    'border': '#1B263B',      # 使用深靛藍作為邊框
    'label_highlight': '#778DA9'  # 使用淺藍色作為標籤高亮
}

class RoundedButton(tk.Canvas):
    def __init__(self, master=None, text="", command=None, radius=10, btnforeground=COLORS['text'],
                 btnbackground=COLORS['accent'], hover_color=COLORS['accent_hover'],
                 width=120, height=35, **kwargs):
        super().__init__(master, width=width, height=height, highlightthickness=0, bg=COLORS['bg_dark'], **kwargs)
        self.radius = radius
        self.btnbackground = btnbackground
        self.hover_color = hover_color
        self.command = command

        # 創建圓角矩形
        self.rect = self.create_rounded_rect(0, 0, width, height, radius, fill=btnbackground)

        # 創建文字
        self.text = self.create_text(width/2, height/2, text=text, fill=btnforeground,
                                   font=('Microsoft JhengHei UI', 10))

        # 綁定事件
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_click)
        self.bind('<ButtonRelease-1>', self.on_release)

    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
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
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_enter(self, e):
        self.itemconfig(self.rect, fill=self.hover_color)

    def on_leave(self, e):
        self.itemconfig(self.rect, fill=self.btnbackground)

    def on_click(self, e):
        self.itemconfig(self.rect, fill=self.btnbackground)

    def on_release(self, e):
        self.itemconfig(self.rect, fill=self.hover_color)
        if self.command:
            self.command()

class RoundedEntry(tk.Canvas):
    def __init__(self, master=None, width=200, height=35, radius=10, validate_phone=False, **kwargs):
        super().__init__(master, width=width, height=height, highlightthickness=0, bg=COLORS['bg_dark'])
        self.radius = radius
        self.validate_phone = validate_phone

        # 創建圓角矩形背景
        self.rect = self.create_rounded_rect(0, 0, width, height, radius,
                                           fill=COLORS['bg_light'],
                                           outline=COLORS['border'])

        # 創建輸入框
        vcmd = (self.register(self._validate_phone), '%P') if validate_phone else None
        self.entry = tk.Entry(self,
                            bg=COLORS['bg_light'],
                            fg=COLORS['text'],
                            font=('Microsoft JhengHei UI', 10),
                            bd=0,
                            highlightthickness=0,
                            validate='key',
                            validatecommand=vcmd)

        # 放置輸入框
        self.entry_window = self.create_window(width/2, height/2,
                                             window=self.entry,
                                             width=width-20)

        # 綁定事件
        self.entry.bind('<FocusIn>', self.on_focus_in)
        self.entry.bind('<FocusOut>', self.on_focus_out)

    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
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
        return self.create_polygon(points, smooth=True, **kwargs)

    def _validate_phone(self, new_value):
        if new_value == "":  # 允許空值
            return True
        # 只允許數字
        if all(c in '0123456789' for c in new_value):
            return True
        messagebox.showwarning("警告", "電話號碼只能包含數字！")
        return False

    def on_focus_in(self, e):
        self.itemconfig(self.rect, outline=COLORS['accent'])

    def on_focus_out(self, e):
        self.itemconfig(self.rect, outline=COLORS['border'])

    def get(self):
        return self.entry.get()

    def set(self, value):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)

class ModernEntry(ttk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<FocusIn>', self.on_focus_in)
        self.bind('<FocusOut>', self.on_focus_out)

    def on_focus_in(self, e):
        self['style'] = 'Focus.Custom.TEntry'

    def on_focus_out(self, e):
        self['style'] = 'Custom.TEntry'

class Contact:
    MAX_NAME_LENGTH = 10
    MAX_PHONE_LENGTH = 15
    MAX_EMAIL_LENGTH = 20
    MAX_ADDRESS_LENGTH = 50

    def __init__(self, name: str, phone: str, email: str, address: str):
        self.name = name[:self.MAX_NAME_LENGTH]
        self.phone = phone[:self.MAX_PHONE_LENGTH]
        self.email = email[:self.MAX_EMAIL_LENGTH]
        self.address = address[:self.MAX_ADDRESS_LENGTH]

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address
        }

class AddressBook:
    def __init__(self, filename: str = "contacts.json"):
        self.filename = filename
        self.contacts: List[Contact] = []
        self.load_contacts()

        # 如果沒有資料，則初始化測試資料
        if not self.contacts:
            self.initialize_test_data()

    def initialize_test_data(self):
        test_contacts = [
            {"name": "張小明", "phone": "0912-345-678", "email": "ming@example.com", "address": "台北市信義區信義路100號"},
            {"name": "李美麗", "phone": "0923-456-789", "email": "mei@example.com", "address": "台北市大安區和平東路200號"},
            {"name": "王大華", "phone": "0934-567-890", "email": "hua@example.com", "address": "新北市板橋區中山路300號"},
            {"name": "陳志明", "phone": "0945-678-901", "email": "zhi@example.com", "address": "台中市西區民生路400號"},
            {"name": "林小芳", "phone": "0956-789-012", "email": "fang@example.com", "address": "高雄市前金區中正路500號"},
            {"name": "黃建國", "phone": "0967-890-123", "email": "guo@example.com", "address": "台南市東區長榮路600號"},
            {"name": "吳美玲", "phone": "0978-901-234", "email": "ling@example.com", "address": "桃園市中壢區環中東路700號"},
            {"name": "蔡志豪", "phone": "0989-012-345", "email": "hao@example.com", "address": "新竹市東區光復路800號"},
            {"name": "楊雅婷", "phone": "0990-123-456", "email": "ting@example.com", "address": "嘉義市西區民生路900號"},
            {"name": "謝俊宏", "phone": "0901-234-567", "email": "hong@example.com", "address": "花蓮市國聯路1000號"},
            {"name": "周雅文", "phone": "0912-111-222", "email": "wen@example.com", "address": "台北市中山區中山北路50號"},
            {"name": "劉建宏", "phone": "0933-222-333", "email": "hong@example.com", "address": "新北市三重區重新路150號"},
            {"name": "許雅琪", "phone": "0955-333-444", "email": "chi@example.com", "address": "桃園市桃園區中正路250號"},
            {"name": "鄭博文", "phone": "0977-444-555", "email": "wen@example.com", "address": "台中市北區三民路350號"},
            {"name": "朱家豪", "phone": "0988-555-666", "email": "hao@example.com", "address": "台南市北區公園路450號"},
            {"name": "宋佳穎", "phone": "0910-666-777", "email": "ying@example.com", "address": "高雄市苓雅區五福路550號"},
            {"name": "何志偉", "phone": "0922-777-888", "email": "wei@example.com", "address": "新竹市北區經國路650號"},
            {"name": "馮淑芬", "phone": "0944-888-999", "email": "fen@example.com", "address": "嘉義市東區民族路750號"},
            {"name": "趙明宏", "phone": "0966-999-000", "email": "hong@example.com", "address": "屏東市民生路850號"},
            {"name": "沈雅婷", "phone": "0999-000-111", "email": "ting@example.com", "address": "宜蘭市中山路950號"},
            {"name": "范智傑", "phone": "0911-121-212", "email": "jie@example.com", "address": "基隆市仁愛區仁一路60號"},
            {"name": "龔雅雯", "phone": "0932-232-323", "email": "wen@example.com", "address": "新北市新店區北新路160號"},
            {"name": "唐文豪", "phone": "0954-343-434", "email": "hao@example.com", "address": "桃園市龜山區文化一路260號"},
            {"name": "彭俊傑", "phone": "0976-454-545", "email": "jie@example.com", "address": "新竹縣竹北市光明路360號"},
            {"name": "董雅芳", "phone": "0987-565-656", "email": "fang@example.com", "address": "苗栗市中正路460號"},
            {"name": "潘建志", "phone": "0909-676-767", "email": "zhi@example.com", "address": "南投市中興路560號"},
            {"name": "藍雅琳", "phone": "0921-787-878", "email": "lin@example.com", "address": "彰化市中山路660號"},
            {"name": "江志豪", "phone": "0943-898-989", "email": "hao@example.com", "address": "雲林市中正路760號"},
            {"name": "盧佳怡", "phone": "0965-909-090", "email": "yi@example.com", "address": "台東市中華路860號"},
            {"name": "梁雅惠", "phone": "0998-010-101", "email": "hui@example.com", "address": "澎湖縣馬公市中正路960號"}
        ]

        # 清空現有聯絡人
        self.contacts = []

        # 新增測試資料
        for contact_data in test_contacts:
            self.add_contact(**contact_data)

        print("已成功初始化30筆測試資料！")

    def load_contacts(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.contacts = [Contact(**contact) for contact in data]

    def save_contacts(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([contact.to_dict() for contact in self.contacts], f, ensure_ascii=False, indent=2)

    def add_contact(self, name: str, phone: str, email: str, address: str) -> bool:
        # 檢查所有欄位是否為空
        empty_fields = []
        if not name or len(name.strip()) == 0:
            empty_fields.append("姓名")
        if not phone or len(phone.strip()) == 0:
            empty_fields.append("電話")
        if not email or len(email.strip()) == 0:
            empty_fields.append("電子郵件")
        if not address or len(address.strip()) == 0:
            empty_fields.append("地址")

        if empty_fields:
            return False, f"以下欄位為必填：{', '.join(empty_fields)}"

        if any(contact.name == name for contact in self.contacts):
            return False, "已存在相同姓名的聯絡人！"

        if len(name) > Contact.MAX_NAME_LENGTH:
            return False, f"姓名長度不能超過{Contact.MAX_NAME_LENGTH}個字！"
        if len(phone) > Contact.MAX_PHONE_LENGTH:
            return False, f"電話長度不能超過{Contact.MAX_PHONE_LENGTH}個字！"
        if len(email) > Contact.MAX_EMAIL_LENGTH:
            return False, f"電子郵件長度不能超過{Contact.MAX_EMAIL_LENGTH}個字！"
        if len(address) > Contact.MAX_ADDRESS_LENGTH:
            return False, f"地址長度不能超過{Contact.MAX_ADDRESS_LENGTH}個字！"

        contact = Contact(name, phone, email, address)
        self.contacts.append(contact)
        self.save_contacts()
        return True, "聯絡人新增成功！"

    def update_contact(self, name: str, phone: str = None, email: str = None, address: str = None) -> bool:
        for contact in self.contacts:
            if contact.name == name:
                if phone is not None:
                    contact.phone = phone[:Contact.MAX_PHONE_LENGTH]
                if email is not None:
                    contact.email = email[:Contact.MAX_EMAIL_LENGTH]
                if address is not None:
                    contact.address = address[:Contact.MAX_ADDRESS_LENGTH]
                self.save_contacts()
                return True, "聯絡人更新成功！"
        return False, f"找不到名為 {name} 的聯絡人！"

    def delete_contact(self, name: str) -> bool:
        # 確保name是字串類型
        name = str(name).strip()
        # 使用列表推導式找出要刪除的聯絡人索引
        indices = [i for i, contact in enumerate(self.contacts) if str(contact.name).strip() == name]

        if indices:
            # 刪除找到的第一個匹配聯絡人
            del self.contacts[indices[0]]
            self.save_contacts()
            return True, "聯絡人刪除成功！"
        return False, f"找不到名為 {name} 的聯絡人！"

    def search_contacts(self, query: str, search_type: str) -> List[Contact]:
        if not query:
            return []

        query = query.lower()
        found_contacts = []

        for contact in self.contacts:
            if search_type == "姓名" and query in contact.name.lower():
                found_contacts.append(contact)
            elif search_type == "電話" and query in contact.phone.lower():
                found_contacts.append(contact)
            elif search_type == "電子郵件" and query in contact.email.lower():
                found_contacts.append(contact)
            elif search_type == "地址" and query in contact.address.lower():
                found_contacts.append(contact)
            elif search_type == "全欄位" and (
                query in contact.name.lower() or
                query in contact.phone.lower() or
                query in contact.email.lower() or
                query in contact.address.lower()
            ):
                found_contacts.append(contact)

        return found_contacts

class AddressBookGUI:
    def __init__(self, root):
        self.root = root
        self.address_book = AddressBook()
        self.setup_gui()

    def setup_gui(self):
        self.root.title("通訊錄管理系統")
        self.root.geometry("1000x600")
        self.root.configure(bg=COLORS['bg_dark'])

        # 設定樣式
        style = ttk.Style()
        style.theme_use('default')

        # 配置按鈕樣式
        style.configure('Custom.TButton',
                       background=COLORS['accent'],
                       foreground=COLORS['text'],
                       padding=(15, 8),
                       font=('Microsoft JhengHei UI', 10),
                       borderwidth=0)

        style.configure('Hover.Custom.TButton',
                       background=COLORS['accent_hover'],
                       foreground=COLORS['text'],
                       padding=(15, 8),
                       font=('Microsoft JhengHei UI', 10),
                       borderwidth=0)

        # 配置輸入框樣式
        style.configure('Custom.TEntry',
                       fieldbackground=COLORS['bg_light'],
                       foreground=COLORS['text'],
                       borderwidth=1,
                       bordercolor=COLORS['border'],
                       padding=5,
                       font=('Microsoft JhengHei UI', 10))

        style.configure('Focus.Custom.TEntry',
                       fieldbackground=COLORS['bg_light'],
                       foreground=COLORS['text'],
                       borderwidth=2,
                       bordercolor=COLORS['accent'],
                       padding=5,
                       font=('Microsoft JhengHei UI', 10))

        # 配置標籤樣式
        style.configure('Custom.TLabel',
                       background=COLORS['bg_dark'],
                       foreground=COLORS['text'],
                       font=('Microsoft JhengHei UI', 10))

        # 配置搜尋區域標籤樣式
        style.configure('Search.TLabel',
                       background=COLORS['bg_dark'],
                       foreground=COLORS['label_highlight'],
                       font=('Microsoft JhengHei UI', 11, 'bold'))

        # 配置框架樣式
        style.configure('Custom.TFrame',
                       background=COLORS['bg_dark'])

        # 配置表格樣式
        style.configure('Custom.Treeview',
                       background=COLORS['bg_medium'],
                       foreground=COLORS['text'],
                       fieldbackground=COLORS['bg_medium'],
                       font=('Microsoft JhengHei UI', 10),
                       rowheight=30)

        style.configure('Custom.Treeview.Heading',
                       background=COLORS['bg_light'],
                       foreground=COLORS['text'],
                       font=('Microsoft JhengHei UI', 10, 'bold'),
                       padding=5)

        style.map('Custom.Treeview',
                 background=[('selected', COLORS['accent'])],
                 foreground=[('selected', COLORS['text'])])

        # 配置下拉選單樣式
        style.configure('Custom.TCombobox',
                       background=COLORS['bg_light'],
                       foreground='black',
                       fieldbackground='white',
                       selectbackground=COLORS['accent'],
                       selectforeground='white',
                       padding=5,
                       font=('Microsoft JhengHei UI', 10, 'bold'))

        # 主框架
        self.main_frame = ttk.Frame(self.root, style='Custom.TFrame')
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # 標題標籤
        title_label = ttk.Label(self.main_frame,
                              text="通訊錄",
                              style='Custom.TLabel',
                              font=('Microsoft JhengHei UI', 24, 'bold'))
        title_label.pack(pady=(0, 20))

        # 左側按鈕區
        self.button_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        self.button_frame.pack(side='left', fill='y', padx=(0, 20))

        # 新增聯絡人按鈕（使用新的圓角按鈕）
        add_button = RoundedButton(self.button_frame, text="新增聯絡人",
                                 command=self.show_add_contact_dialog,
                                 width=150)
        add_button.pack(fill='x', pady=5)

        # 搜尋框架
        self.search_frame = ttk.Frame(self.button_frame, style='Custom.TFrame')
        self.search_frame.pack(fill='x', pady=15)

        # 搜尋類型標籤
        ttk.Label(self.search_frame, text="搜尋類型：",
                 style='Search.TLabel').pack(fill='x', pady=(0, 5))

        # 搜尋類型下拉選單
        self.search_type = tk.StringVar(value="全欄位")
        self.search_type_combo = ttk.Combobox(self.search_frame,
                                            textvariable=self.search_type,
                                            values=["姓名", "電話", "電子郵件", "地址", "全欄位"],
                                            state="readonly",
                                            style='Custom.TCombobox')
        self.search_type_combo.pack(fill='x', pady=2)

        # 設定下拉選單的顏色
        self.root.option_add('*TCombobox*Listbox.background', 'white')
        self.root.option_add('*TCombobox*Listbox.foreground', 'black')
        self.root.option_add('*TCombobox*Listbox.selectBackground', COLORS['accent'])
        self.root.option_add('*TCombobox*Listbox.selectForeground', 'white')

        # 搜尋輸入框標籤
        ttk.Label(self.search_frame, text="搜尋關鍵字：",
                 style='Search.TLabel').pack(fill='x', pady=(10, 5))

        # 搜尋輸入框
        self.search_var = tk.StringVar()
        self.search_entry = RoundedEntry(self.search_frame, width=200, height=35)
        self.search_entry.pack(fill='x', pady=2)
        self.search_entry.entry.config(textvariable=self.search_var)
        self.search_var.trace('w', self.on_search)

        # 右側聯絡人列表
        self.list_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        self.list_frame.pack(side='left', expand=True, fill='both')

        # 聯絡人列表（表格）
        columns = ('姓名', '電話', '電子郵件', '地址')
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show='headings',
                                style='Custom.Treeview')

        # 設定欄位寬度和標題
        self.tree.heading('姓名', text='姓名')
        self.tree.heading('電話', text='電話')
        self.tree.heading('電子郵件', text='電子郵件')
        self.tree.heading('地址', text='地址')

        self.tree.column('姓名', width=120)
        self.tree.column('電話', width=150)
        self.tree.column('電子郵件', width=200)
        self.tree.column('地址', width=300)

        # 添加滾動條
        scrollbar = ttk.Scrollbar(self.list_frame, orient='vertical',
                                command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')

        # 右鍵選單
        self.context_menu = tk.Menu(self.root, tearoff=0, bg=COLORS['bg_medium'],
                                  fg=COLORS['text'],
                                  activebackground=COLORS['accent'],
                                  activeforeground=COLORS['text'],
                                  font=('Microsoft JhengHei UI', 10))
        self.context_menu.add_command(label="編輯", command=self.show_edit_contact_dialog)
        self.context_menu.add_command(label="刪除", command=self.delete_contact)

        self.tree.bind("<Button-3>", self.show_context_menu)

        # 載入聯絡人列表
        self.refresh_contact_list()

    def show_dialog(self, title, is_edit=False):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x350")
        dialog.configure(bg=COLORS['bg_dark'])

        # 讓對話框永遠在主視窗上方
        dialog.transient(self.root)
        dialog.grab_set()

        # 設定對話框的最小尺寸
        dialog.minsize(400, 350)

        # 輸入框架
        frame = ttk.Frame(dialog, style='Custom.TFrame')
        frame.pack(padx=30, pady=30, fill='both', expand=True)

        return dialog, frame

    def format_phone_number(self, phone: str) -> str:
        # 移除所有非數字字符
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) == 10:  # 如果是10位數字（例如：0912345678）
            return f"{digits[:4]}-{digits[4:7]}-{digits[7:]}"
        return digits  # 如果不是10位數字，則返回原始數字

    def show_add_contact_dialog(self):
        dialog, frame = self.show_dialog("新增聯絡人")

        # 姓名輸入
        ttk.Label(frame, text="姓名:", style='Custom.TLabel').grid(row=0, column=0, sticky='w', pady=10)
        name_var = tk.StringVar()
        name_entry = RoundedEntry(frame, width=250, height=35)
        name_entry.grid(row=0, column=1, sticky='ew', padx=(10, 0))
        name_entry.entry.config(textvariable=name_var)

        # 電話輸入（添加驗證）
        ttk.Label(frame, text="電話:", style='Custom.TLabel').grid(row=1, column=0, sticky='w', pady=10)
        phone_var = tk.StringVar()
        phone_entry = RoundedEntry(frame, width=250, height=35, validate_phone=True)
        phone_entry.grid(row=1, column=1, sticky='ew', padx=(10, 0))
        phone_entry.entry.config(textvariable=phone_var)

        # 電子郵件輸入
        ttk.Label(frame, text="電子郵件:", style='Custom.TLabel').grid(row=2, column=0, sticky='w', pady=10)
        email_var = tk.StringVar()
        email_entry = RoundedEntry(frame, width=250, height=35)
        email_entry.grid(row=2, column=1, sticky='ew', padx=(10, 0))
        email_entry.entry.config(textvariable=email_var)

        # 地址輸入
        ttk.Label(frame, text="地址:", style='Custom.TLabel').grid(row=3, column=0, sticky='w', pady=10)
        address_var = tk.StringVar()
        address_entry = RoundedEntry(frame, width=250, height=35)
        address_entry.grid(row=3, column=1, sticky='ew', padx=(10, 0))
        address_entry.entry.config(textvariable=address_var)

        def save_contact():
            # 格式化電話號碼
            formatted_phone = self.format_phone_number(phone_var.get())
            success, message = self.address_book.add_contact(
                name_var.get(),
                formatted_phone,
                email_var.get(),
                address_var.get()
            )

            if success:
                self.refresh_contact_list()
                dialog.destroy()
            messagebox.showinfo("結果", message)

        # 按鈕框架
        button_frame = ttk.Frame(frame, style='Custom.TFrame')
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        # 使用新的圓角按鈕
        save_button = RoundedButton(button_frame, text="儲存",
                                  command=save_contact,
                                  width=80)
        save_button.pack(side='left', padx=5)

        cancel_button = RoundedButton(button_frame, text="取消",
                                    command=dialog.destroy,
                                    width=80)
        cancel_button.pack(side='left', padx=5)

        # 設定欄位的權重
        frame.columnconfigure(1, weight=1)

    def show_edit_contact_dialog(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("警告", "請先選擇要編輯的聯絡人！")
            return

        values = self.tree.item(selected_item)['values']
        dialog, frame = self.show_dialog("編輯聯絡人", True)

        # 姓名（唯讀）
        ttk.Label(frame, text="姓名:", style='Custom.TLabel').grid(row=0, column=0, sticky='w', pady=10)
        name_var = tk.StringVar(value=values[0])
        name_entry = RoundedEntry(frame, width=250, height=35)
        name_entry.grid(row=0, column=1, sticky='ew', padx=(10, 0))
        name_entry.entry.config(textvariable=name_var)

        # 電話（添加驗證，去除連字符號顯示）
        ttk.Label(frame, text="電話:", style='Custom.TLabel').grid(row=1, column=0, sticky='w', pady=10)
        phone_var = tk.StringVar(value=''.join(filter(str.isdigit, values[1])))
        phone_entry = RoundedEntry(frame, width=250, height=35, validate_phone=True)
        phone_entry.grid(row=1, column=1, sticky='ew', padx=(10, 0))
        phone_entry.entry.config(textvariable=phone_var)

        # 電子郵件
        ttk.Label(frame, text="電子郵件:", style='Custom.TLabel').grid(row=2, column=0, sticky='w', pady=10)
        email_var = tk.StringVar(value=values[2])
        email_entry = RoundedEntry(frame, width=250, height=35)
        email_entry.grid(row=2, column=1, sticky='ew', padx=(10, 0))
        email_entry.entry.config(textvariable=email_var)

        # 地址
        ttk.Label(frame, text="地址:", style='Custom.TLabel').grid(row=3, column=0, sticky='w', pady=10)
        address_var = tk.StringVar(value=values[3])
        address_entry = RoundedEntry(frame, width=250, height=35)
        address_entry.grid(row=3, column=1, sticky='ew', padx=(10, 0))
        address_entry.entry.config(textvariable=address_var)

        def update_contact():
            # 格式化電話號碼
            formatted_phone = self.format_phone_number(phone_var.get())
            success, message = self.address_book.update_contact(
                name_var.get(),
                formatted_phone,
                email_var.get(),
                address_var.get()
            )

            if success:
                self.refresh_contact_list()
                dialog.destroy()
            messagebox.showinfo("結果", message)

        # 按鈕框架
        button_frame = ttk.Frame(frame, style='Custom.TFrame')
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        # 使用新的圓角按鈕
        update_button = RoundedButton(button_frame, text="更新",
                                    command=update_contact,
                                    width=80)
        update_button.pack(side='left', padx=5)

        cancel_button = RoundedButton(button_frame, text="取消",
                                    command=dialog.destroy,
                                    width=80)
        cancel_button.pack(side='left', padx=5)

        # 設定欄位的權重
        frame.columnconfigure(1, weight=1)

    def delete_contact(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("警告", "請先選擇要刪除的聯絡人！")
            return

        name = self.tree.item(selected_item)['values'][0]
        if messagebox.askyesno("確認", f"確定要刪除 {name} 的聯絡資料嗎？"):
            # 先確保contacts.json檔案是最新的
            self.address_book.load_contacts()
            success, message = self.address_book.delete_contact(name)
            if success:
                self.refresh_contact_list()
            messagebox.showinfo("結果", message)

    def on_search(self, *args):
        query = self.search_var.get()
        search_type = self.search_type.get()

        # 清空現有列表
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 如果搜尋框為空，顯示所有聯絡人
        if not query:
            self.refresh_contact_list()
            return

        # 搜尋並顯示結果
        found_contacts = self.address_book.search_contacts(query, search_type)
        for contact in found_contacts:
            self.tree.insert('', 'end', values=(
                contact.name,
                contact.phone,
                contact.email,
                contact.address
            ))

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def refresh_contact_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for contact in self.address_book.contacts:
            self.tree.insert('', 'end', values=(
                contact.name,
                contact.phone,
                contact.email,
                contact.address
            ))

def main():
    root = tk.Tk()
    app = AddressBookGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()