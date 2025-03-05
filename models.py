import json
import os
from typing import List, Dict, Tuple

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

    def load_contacts(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.contacts = [Contact(**contact) for contact in data]

    def save_contacts(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([contact.to_dict() for contact in self.contacts], f, ensure_ascii=False, indent=2)

    def add_contact(self, name: str, phone: str, email: str, address: str) -> Tuple[bool, str]:
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

    def update_contact(self, name: str, phone: str = None, email: str = None, address: str = None) -> Tuple[bool, str]:
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

    def delete_contact(self, name: str) -> Tuple[bool, str]:
        # 確保name是字串類型
        name = str(name).strip()
        # 使用列表推導式找出要刪除的聯絡人索引
        indices = [i for i, contact in enumerate(self.contacts) if str(contact.name).strip() == name]

        if indices:
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