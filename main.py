import sys
from PyQt6.QtWidgets import QApplication, QMessageBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QLineEdit, QComboBox, QLabel, QTableWidgetItem, QMenu
from qt_gui import AddressBookQt
from qt_constants import COLORS

def handle_exception(_, exc_value, __):
    """處理未捕獲的異常"""
    error_msg = f"發生錯誤：\n{str(exc_value)}"
    QMessageBox.critical(None, "錯誤", error_msg)
    sys.exit(1)

def main():
    # 設定異常處理
    sys.excepthook = handle_exception

    app = QApplication(sys.argv)
    window = AddressBookQt()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

def delete_contact(self):
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
        QMessageBox.information(self, "結果", message)

def show_context_menu(self, position):
    menu = QMenu(self)
    edit_action = menu.addAction("編輯")
    delete_action = menu.addAction("刪除")

    action = menu.exec(self.table.viewport().mapToGlobal(position))

    if action == edit_action:
        self.show_edit_contact_dialog()
    elif action == delete_action:
        self.delete_contact()

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

    # 設定項目對齊方式
    for col, item in enumerate(items):
        item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.table.setItem(row, col, item)

def create_left_panel(self):
    panel = QWidget()
    layout = QVBoxLayout(panel)
    layout.setContentsMargins(20, 20, 20, 20)  # 設定左右邊距
    layout.setSpacing(15)  # 增加元件之間的間距

    # 新增聯絡人按鈕
    add_button = QPushButton("新增聯絡人")
    add_button.setFixedWidth(200)  # 設定固定寬度
    add_button.setMinimumHeight(40)  # 設定最小高度
    add_button.clicked.connect(self.show_add_contact_dialog)
    layout.addWidget(add_button)

    # 搜尋區域
    search_frame = QWidget()
    search_layout = QVBoxLayout(search_frame)
    search_layout.setSpacing(10)  # 搜尋區域內的間距

    # 搜尋類型
    search_type_label = QLabel("搜尋類型：")
    self.search_type = QComboBox()
    self.search_type.setFixedWidth(200)  # 設定固定寬度
    self.search_type.addItems(["姓名", "電話", "電子郵件", "地址", "全欄位"])

    # 搜尋輸入框
    search_input_label = QLabel("搜尋關鍵字：")
    self.search_input = QLineEdit()
    self.search_input.setFixedWidth(200)  # 設定固定寬度
    self.search_input.setPlaceholderText("請輸入搜尋關鍵字...")
    self.search_input.textChanged.connect(self.on_search)

    # 排序狀態顯示
    self.sort_status_label = QLabel("目前排序方式：預設")
    self.sort_status_label.setFixedWidth(200)  # 設定固定寬度
    self.sort_status_label.setStyleSheet(f"color: {COLORS['text_gray']};")

    # 重置排序按鈕
    reset_sort_button = QPushButton("重置排序")
    reset_sort_button.setFixedWidth(200)  # 設定固定寬度
    reset_sort_button.setMinimumHeight(40)  # 設定最小高度
    reset_sort_button.clicked.connect(self.reset_sort)

    # 添加所有元件到搜尋區域
    search_layout.addWidget(search_type_label)
    search_layout.addWidget(self.search_type)
    search_layout.addWidget(search_input_label)
    search_layout.addWidget(self.search_input)
    search_layout.addWidget(self.sort_status_label)
    search_layout.addWidget(reset_sort_button)

    layout.addWidget(search_frame)
    layout.addStretch()  # 添加彈性空間

    return panel
