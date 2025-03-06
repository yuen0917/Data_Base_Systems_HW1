from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QTableWidget, QLineEdit, QComboBox,
                           QLabel, QTableWidgetItem, QMenu, QMessageBox)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, pyqtSlot
from qt_constants import STYLESHEET, COLORS
from qt_dialogs import ContactDialog
from models import AddressBook, Contact

class AddressBookQt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.address_book = AddressBook()
        self.current_sort_column = None
        self.sort_order = Qt.SortOrder.AscendingOrder
        self.init_ui()
        self.setup_context_menu()
        self.refresh_contact_list()

    def init_ui(self):
        # 設定主視窗
        self.setWindowTitle("通訊錄管理系統")
        self.setMinimumSize(1200, 700)
        self.setStyleSheet(STYLESHEET)

        # 主要容器
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 標題
        title_label = QLabel("通訊錄管理系統")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin: 20px 0;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # 內容區域
        content_layout = QHBoxLayout()

        # 左側控制面板
        left_panel = self.create_left_panel()
        content_layout.addWidget(left_panel)

        # 右側表格
        self.table = self.create_table()
        content_layout.addWidget(self.table)

        # 設定左側面板和表格的比例
        content_layout.setStretch(0, 1)  # 左側面板佔 1
        content_layout.setStretch(1, 4)  # 表格佔 4

        main_layout.addLayout(content_layout)

    def create_left_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)  # 設定左右邊距
        layout.setSpacing(15)  # 增加元件之間的間距
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # 整體置中對齊

        # 新增聯絡人按鈕
        add_button = QPushButton("新增聯絡人")
        add_button.setFixedWidth(200)  # 設定固定寬度
        add_button.setMinimumHeight(40)  # 設定最小高度
        add_button.clicked.connect(self.show_add_contact_dialog)
        layout.addWidget(add_button, 0, Qt.AlignmentFlag.AlignHCenter)  # 水平置中

        # 搜尋區域
        search_frame = QWidget()
        search_layout = QVBoxLayout(search_frame)
        search_layout.setSpacing(10)  # 搜尋區域內的間距
        search_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # 搜尋區域內容置中

        # 搜尋類型
        search_type_label = QLabel("搜尋類型：")
        search_type_label.setAlignment(Qt.AlignmentFlag.AlignLeft)  # 文字靠左對齊
        self.search_type = QComboBox()
        self.search_type.setFixedWidth(200)
        self.search_type.addItems(["姓名", "電話", "電子郵件", "地址", "全欄位"])

        # 搜尋輸入框
        search_input_label = QLabel("搜尋關鍵字：")
        search_input_label.setAlignment(Qt.AlignmentFlag.AlignLeft)  # 文字靠左對齊
        self.search_input = QLineEdit()
        self.search_input.setFixedWidth(200)
        self.search_input.setPlaceholderText("請輸入搜尋關鍵字...")
        self.search_input.textChanged.connect(self.on_search)

        # 排序狀態顯示
        self.sort_status_label = QLabel("目前排序方式：預設")
        self.sort_status_label.setFixedWidth(200)
        self.sort_status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)  # 文字靠左對齊
        self.sort_status_label.setStyleSheet(f"color: {COLORS['text_gray']};")

        # 重置排序按鈕
        reset_sort_button = QPushButton("重置排序")
        reset_sort_button.setFixedWidth(200)
        reset_sort_button.setMinimumHeight(40)
        reset_sort_button.clicked.connect(self.reset_sort)

        # 添加所有元件到搜尋區域
        for widget in [search_type_label, self.search_type,
                      search_input_label, self.search_input,
                      self.sort_status_label, reset_sort_button]:
            search_layout.addWidget(widget, 0, Qt.AlignmentFlag.AlignHCenter)  # 每個元件都水平置中

        layout.addWidget(search_frame)
        layout.addStretch()  # 添加彈性空間

        return panel

    def create_table(self):
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["姓名", "電話", "電子郵件", "地址"])

        # 設定表格列寬
        header = table.horizontalHeader()
        header.setStretchLastSection(True)
        table.setColumnWidth(0, 150)  # 姓名
        table.setColumnWidth(1, 150)  # 電話
        table.setColumnWidth(2, 200)  # 電子郵件

        # 設定表格標題點擊事件
        header.sectionClicked.connect(self.on_header_clicked)

        return table

    def show_add_contact_dialog(self):
        dialog = ContactDialog(self)
        if dialog.exec() == ContactDialog.DialogCode.Accepted:
            contact_data = dialog.get_contact_data()
            success, message = self.address_book.add_contact(**contact_data)

            if success:
                self.refresh_contact_list()
                QMessageBox.information(self, "成功", message)
            else:
                QMessageBox.warning(self, "錯誤", message)

    def show_edit_contact_dialog(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "請先選擇要編輯的聯絡人！")
            return

        row = selected_items[0].row()
        name = self.table.item(row, 0).text()

        # 找到對應的聯絡人
        contact = next((c for c in self.address_book.contacts if c.name == name), None)
        if contact:
            dialog = ContactDialog(self, contact)
            if dialog.exec() == ContactDialog.DialogCode.Accepted:
                contact_data = dialog.get_contact_data()
                success, message = self.address_book.update_contact(**contact_data)

                if success:
                    self.refresh_contact_list()
                    QMessageBox.information(self, "成功", message)
                else:
                    QMessageBox.warning(self, "錯誤", message)

    def setup_context_menu(self):
        """設定右鍵選單"""
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        """顯示右鍵選單"""
        menu = QMenu(self)
        edit_action = menu.addAction("編輯")
        delete_action = menu.addAction("刪除")

        action = menu.exec(self.table.viewport().mapToGlobal(position))

        if action == edit_action:
            self.show_edit_contact_dialog()
        elif action == delete_action:
            self.delete_contact()

    @pyqtSlot(str)
    def on_search(self, text):
        """處理搜尋"""
        search_type = self.search_type.currentText()

        # 清空表格
        self.table.setRowCount(0)

        if not text:
            self.refresh_contact_list()
            return

        # 搜尋聯絡人
        found_contacts = self.address_book.search_contacts(text, search_type)

        # 顯示搜尋結果
        for contact in found_contacts:
            self.add_contact_to_table(contact)

    def on_header_clicked(self, logical_index):
        """處理表格標題點擊排序"""
        if self.current_sort_column == logical_index:
            # 切換排序順序
            self.sort_order = Qt.SortOrder.DescendingOrder if self.sort_order == Qt.SortOrder.AscendingOrder else Qt.SortOrder.AscendingOrder
        else:
            self.current_sort_column = logical_index
            self.sort_order = Qt.SortOrder.AscendingOrder

        # 執行排序
        self.table.sortItems(logical_index, self.sort_order)

        # 更新排序狀態顯示
        column_name = self.table.horizontalHeaderItem(logical_index).text()
        direction = "降序" if self.sort_order == Qt.SortOrder.DescendingOrder else "升序"
        self.sort_status_label.setText(f"目前排序方式：{column_name} ({direction})")

    def reset_sort(self):
        """重置排序"""
        self.current_sort_column = None
        self.sort_order = Qt.SortOrder.AscendingOrder
        self.sort_status_label.setText("目前排序方式：預設")
        self.refresh_contact_list()

    def refresh_contact_list(self):
        """刷新聯絡人列表"""
        self.table.setRowCount(0)
        for contact in self.address_book.contacts:
            self.add_contact_to_table(contact)

    def add_contact_to_table(self, contact):
        """將聯絡人添加到表格中"""
        row = self.table.rowCount()
        self.table.insertRow(row)

        # 設定每個欄位的值
        items = [
            QTableWidgetItem(contact.name),
            QTableWidgetItem(contact.phone),
            QTableWidgetItem(contact.email),
            QTableWidgetItem(contact.address)
        ]

        # 設定項目對齊方式和顏色
        for col, item in enumerate(items):
            item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.table.setItem(row, col, item)

        # 設定交替行顏色
        if row % 2:
            for col in range(self.table.columnCount()):
                self.table.item(row, col).setBackground(QColor(COLORS['bg_medium']))

    def delete_contact(self):
        """刪除聯絡人"""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "請先選擇要刪除的聯絡人！")
            return

        row = selected_items[0].row()
        name = self.table.item(row, 0).text()

        reply = QMessageBox.question(
            self,
            "確認刪除",
            f"確定要刪除聯絡人 {name} 嗎？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.address_book.delete_contact(name)
            if success:
                self.refresh_contact_list()
                QMessageBox.information(self, "成功", message)
            else:
                QMessageBox.warning(self, "錯誤", message)