from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                           QLineEdit, QPushButton, QMessageBox)
from qt_constants import COLORS

class ContactDialog(QDialog):
    def __init__(self, parent=None, contact=None):
        super().__init__(parent)
        self.contact = contact
        self.is_edit_mode = contact is not None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("編輯聯絡人" if self.is_edit_mode else "新增聯絡人")
        self.setMinimumWidth(400)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS['bg_dark']};
            }}
            QLabel {{
                color: {COLORS['text']};
            }}
            QLineEdit {{
                background-color: {COLORS['bg_medium']};
                color: {COLORS['text']};
                border: none;
                border-radius: 5px;
                padding: 8px;
                margin: 2px;
            }}
            QPushButton {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text']};
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                margin: 5px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent']};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # 姓名輸入
        name_label = QLabel("姓名:")
        self.name_input = QLineEdit()
        if self.is_edit_mode:
            self.name_input.setText(self.contact.name)
            self.name_input.setReadOnly(True)
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)

        # 電話輸入
        phone_label = QLabel("電話:")
        self.phone_input = QLineEdit()
        if self.is_edit_mode:
            self.phone_input.setText(self.contact.phone)
        self.phone_input.textChanged.connect(self.validate_phone)
        layout.addWidget(phone_label)
        layout.addWidget(self.phone_input)

        # 電子郵件輸入
        email_label = QLabel("電子郵件:")
        self.email_input = QLineEdit()
        if self.is_edit_mode:
            self.email_input.setText(self.contact.email)
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)

        # 地址輸入
        address_label = QLabel("地址:")
        self.address_input = QLineEdit()
        if self.is_edit_mode:
            self.address_input.setText(self.contact.address)
        layout.addWidget(address_label)
        layout.addWidget(self.address_input)

        # 按鈕
        button_layout = QHBoxLayout()
        save_button = QPushButton("儲存")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

    def validate_phone(self, text):
        # 只允許數字
        filtered_text = ''.join(filter(str.isdigit, text))
        if filtered_text != text:
            self.phone_input.setText(filtered_text)

    def get_contact_data(self):
        return {
            'name': self.name_input.text().strip(),
            'phone': self.phone_input.text().strip(),
            'email': self.email_input.text().strip(),
            'address': self.address_input.text().strip()
        }

    def validate_inputs(self):
        data = self.get_contact_data()
        empty_fields = []

        if not data['name']: empty_fields.append("姓名")
        if not data['phone']: empty_fields.append("電話")
        if not data['email']: empty_fields.append("電子郵件")
        if not data['address']: empty_fields.append("地址")

        if empty_fields:
            QMessageBox.warning(
                self,
                "警告",
                f"以下欄位為必填：{', '.join(empty_fields)}",
                QMessageBox.StandardButton.Ok
            )
            return False

        # 驗證欄位長度
        if len(data['name']) > 10:
            QMessageBox.warning(self, "警告", "姓名不能超過10個字元")
            return False
        if len(data['phone']) > 15:
            QMessageBox.warning(self, "警告", "電話不能超過15個字元")
            return False
        if len(data['email']) > 20:
            QMessageBox.warning(self, "警告", "電子郵件不能超過20個字元")
            return False
        if len(data['address']) > 50:
            QMessageBox.warning(self, "警告", "地址不能超過50個字元")
            return False

        return True

    def accept(self):
        if self.validate_inputs():
            super().accept()