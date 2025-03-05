import tkinter as tk
from models import AddressBook
from gui import AddressBookGUI
from constants import COLORS

def main():
    root = tk.Tk()
    root.geometry("1000x600")  # 設定視窗大小
    root.configure(bg=COLORS['bg_dark'])  # 設定主視窗背景色

    address_book = AddressBook()
    gui = AddressBookGUI(root)
    gui.set_address_book(address_book)  # 這會觸發 setup_gui

    root.mainloop()

if __name__ == "__main__":
    main()