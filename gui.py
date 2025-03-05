import tkinter as tk
from tkinter import ttk, messagebox
from widgets import RoundedEntry, RoundedButton
from constants import COLORS

class AddressBookGUI:
    def __init__(self, root):
        self.root = root
        self.address_book = None
        # 初始化所有需要的變數
        self.main_frame = None
        self.list_frame = None
        self.tree = None
        self.search_var = None
        self.search_type = None
        self.button_frame = None
        self.search_frame = None
        # 初始化排序相關變數
        self.current_sort = "預設"  # 改為預設狀態
        self.sort_reverse = False
        self.original_order = []  # 儲存原始順序

        # 直接設置基本的 GUI 框架
        self.setup_base_gui()

    def setup_base_gui(self):
        """設置基本的 GUI 框架"""
        self.root.title("通訊錄管理系統")
        self.root.minsize(1200, 700)
        self.root.geometry("1200x700")
        self.root.configure(bg=COLORS['bg_dark'])

        # 設定樣式
        style = ttk.Style()
        style.theme_use('default')

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

        # 配置下拉選單樣式
        style.configure('Custom.TCombobox',
                       background=COLORS['bg_light'],
                       foreground=COLORS['text'],
                       fieldbackground=COLORS['bg_light'],
                       selectbackground=COLORS['accent'],
                       selectforeground=COLORS['text'])

        # 配置表格樣式
        style.configure('Custom.Treeview',
                       background=COLORS['treeview_bg'],
                       foreground=COLORS['text'],
                       fieldbackground=COLORS['treeview_bg'],
                       font=('Microsoft JhengHei UI', 11),
                       rowheight=40)

        style.configure('Custom.Treeview.Heading',
                       background=COLORS['bg_medium'],
                       foreground=COLORS['text'],
                       font=('Microsoft JhengHei UI', 11, 'bold'),
                       padding=10)

        style.map('Custom.Treeview',
                 background=[('selected', COLORS['treeview_selected'])],
                 foreground=[('selected', COLORS['text'])])

        # 創建標題框架
        title_frame = ttk.Frame(self.root, style='Custom.TFrame')
        title_frame.pack(fill='x', pady=(20, 30))  # 增加上下間距

        # 標題標籤
        title_label = ttk.Label(title_frame,
                               text="通訊錄管理系統",
                               style='Custom.TLabel',
                               font=('Microsoft JhengHei UI', 24, 'bold'))
        title_label.pack(expand=True)  # 讓標題置中

        # 在標題下方添加排序狀態顯示和重置按鈕
        self.sort_status_frame = ttk.Frame(self.root, style='Custom.TFrame')
        self.sort_status_frame.pack(fill='x', pady=(0, 10))

        # 添加重置排序按鈕
        self.reset_sort_button = RoundedButton(
            self.sort_status_frame,
            text="重置排序",
            command=self.reset_sort,
            width=80,
            height=30
        )
        self.reset_sort_button.pack(side='right', padx=(0, 20))

        # 排序狀態標籤
        self.sort_label = ttk.Label(
            self.sort_status_frame,
            text="目前排序方式：預設",
            style='Custom.TLabel',
            font=('Microsoft JhengHei UI', 10)
        )
        self.sort_label.pack(side='right', padx=20)

        # 主框架
        self.main_frame = ttk.Frame(self.root, style='Custom.TFrame')
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=10)

        # 列表框架 - 加入 padding 並調整大小
        self.list_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        self.list_frame.pack(side='right', expand=True, fill='both', padx=10, pady=10)

        # 創建樹狀視圖
        columns = ('姓名', '電話', '電子郵件', '地址')
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show='headings',
                                style='Custom.Treeview', height=15)

        # 設定欄位和點擊事件
        for col in columns:
            self.tree.heading(col, text=col,
                            command=lambda c=col: self.sort_contacts(c))

        # 調整欄位寬度 - 縮小總寬度
        total_width = 800  # 縮小總寬度
        self.tree.column('姓名', width=int(total_width * 0.15))    # 120px
        self.tree.column('電話', width=int(total_width * 0.20))    # 160px
        self.tree.column('電子郵件', width=int(total_width * 0.25))  # 200px
        self.tree.column('地址', width=int(total_width * 0.40))    # 320px

        # 調整表格樣式
        style = ttk.Style()
        style.configure('Custom.Treeview',
                       rowheight=35,  # 稍微減少行高
                       font=('Microsoft JhengHei UI', 10))  # 稍微減小字體

        style.configure('Custom.Treeview.Heading',
                       font=('Microsoft JhengHei UI', 10, 'bold'),
                       padding=8)  # 減少表頭padding

        # 添加滾動條
        scrollbar = ttk.Scrollbar(self.list_frame, orient='vertical',
                                command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # 打包樹狀視圖和滾動條
        self.tree.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')

        # 設定交替行顏色
        self.tree.tag_configure('oddrow', background=COLORS['treeview_alternate'])

    def set_address_book(self, address_book):
        """設置通訊錄並完成剩餘的 GUI 設置"""
        self.address_book = address_book
        self.setup_gui()  # 設置其餘的 GUI 元素

    def setup_gui(self):
        """設置其餘的 GUI 元素"""
        # 左側控制區域
        control_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        control_frame.pack(side='left', fill='y', padx=(0, 20))

        # 新增聯絡人按鈕
        add_button = RoundedButton(control_frame, text="新增聯絡人",
                                 command=self.show_add_contact_dialog,
                                 width=150, height=40)
        add_button.pack(fill='x', pady=5)

        # 搜尋框架
        search_frame = ttk.Frame(control_frame, style='Custom.TFrame')
        search_frame.pack(fill='x', pady=15)

        # 搜尋類型標籤
        ttk.Label(search_frame, text="搜尋類型：",
                 style='Search.TLabel').pack(fill='x', pady=(0, 5))

        # 搜尋類型下拉選單
        self.search_type = tk.StringVar(value="全欄位")
        search_type_combo = ttk.Combobox(search_frame,
                                       textvariable=self.search_type,
                                       values=["姓名", "電話", "電子郵件", "地址", "全欄位"],
                                       state="readonly",
                                       style='Custom.TCombobox')
        search_type_combo.pack(fill='x', pady=2)

        # 搜尋輸入框標籤
        ttk.Label(search_frame, text="搜尋關鍵字：",
                 style='Search.TLabel').pack(fill='x', pady=(10, 5))

        # 搜尋輸入框
        self.search_var = tk.StringVar()
        search_entry = RoundedEntry(search_frame, width=150, height=35)
        search_entry.pack(fill='x', pady=2)
        search_entry.entry.config(textvariable=self.search_var)
        self.search_var.trace('w', self.on_search)

        # 右鍵選單
        self.context_menu = tk.Menu(self.root, tearoff=0, bg=COLORS['bg_medium'],
                                  fg=COLORS['text'],
                                  activebackground=COLORS['accent'],
                                  activeforeground=COLORS['text'],
                                  font=('Microsoft JhengHei UI', 10))
        self.context_menu.add_command(label="編輯", command=self.show_edit_contact_dialog)
        self.context_menu.add_command(label="刪除", command=self.delete_contact)

        # 綁定右鍵選單
        self.tree.bind("<Button-3>", self.show_context_menu)

        # 刷新聯絡人列表
        self.refresh_contact_list()

    def refresh_contact_list(self):
        """刷新聯絡人列表"""
        # 清空現有列表
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 插入聯絡人
        contacts_to_display = self.address_book.contacts

        for i, contact in enumerate(contacts_to_display):
            tag = 'oddrow' if i % 2 else ''
            self.tree.insert('', 'end', values=(
                contact.name,
                contact.phone,
                contact.email,
                contact.address
            ), tags=(tag,))

        # 如果有現有的排序且不是預設排序，則重新應用排序
        if self.current_sort != "預設":
            self.sort_contacts(self.current_sort)

    def show_add_contact_dialog(self):
        dialog, frame = self.show_dialog("新增聯絡人")

        # 姓名輸入
        ttk.Label(frame, text="姓名:", style='Custom.TLabel').grid(row=0, column=0, sticky='w', pady=10)
        name_var = tk.StringVar()
        name_entry = RoundedEntry(frame, width=250, height=35)
        name_entry.grid(row=0, column=1, sticky='ew', padx=(10, 0))
        name_entry.entry.config(textvariable=name_var)

        # 電話輸入
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

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def show_edit_contact_dialog(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("警告", "請先選擇要編輯的聯絡人！")
            return

        values = self.tree.item(selected_item)['values']
        dialog, frame = self.show_dialog("編輯聯絡人")

        # 姓名（唯讀）
        ttk.Label(frame, text="姓名:", style='Custom.TLabel').grid(row=0, column=0, sticky='w', pady=10)
        name_var = tk.StringVar(value=str(values[0]))
        name_entry = RoundedEntry(frame, width=250, height=35)
        name_entry.grid(row=0, column=1, sticky='ew', padx=(10, 0))
        name_entry.entry.config(textvariable=name_var,
                              state='readonly',
                              readonlybackground=COLORS['bg_medium'],
                              fg=COLORS['text'])

        # 電話
        ttk.Label(frame, text="電話:", style='Custom.TLabel').grid(row=1, column=0, sticky='w', pady=10)
        phone_str = str(values[1])
        phone_var = tk.StringVar(value=''.join(c for c in phone_str if c.isdigit()))
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
        # 確保 address_book 已經設定
        if not self.address_book:
            return

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

    def reset_sort(self):
        """重置為預設排序"""
        self.current_sort = "預設"
        self.sort_reverse = False
        self.sort_label.config(text="目前排序方式：預設")

        # 清空並重新插入項目，保持原始順序
        self.refresh_contact_list()

    def sort_contacts(self, column):
        """排序聯絡人列表"""
        if column == self.current_sort:
            self.sort_reverse = not self.sort_reverse
        else:
            self.current_sort = column
            self.sort_reverse = False

        # 更新排序狀態顯示
        direction = "降序" if self.sort_reverse else "升序"
        self.sort_label.config(text=f"目前排序方式：{column} ({direction})")

        # 獲取所有項目
        items = [(self.tree.set(item, column), item) for item in self.tree.get_children('')]

        # 排序
        items.sort(reverse=self.sort_reverse)

        # 重新排列項目
        for index, (_, item) in enumerate(items):
            self.tree.move(item, '', index)
            # 更新交替行顏色
            tags = ('oddrow',) if index % 2 else ()
            self.tree.item(item, tags=tags)

    def current_sort_key(self, column):
        """將欄位名稱轉換為對應的屬性名稱"""
        column_map = {
            '姓名': 'name',
            '電話': 'phone',
            '電子郵件': 'email',
            '地址': 'address'
        }
        return column_map.get(column, 'name')