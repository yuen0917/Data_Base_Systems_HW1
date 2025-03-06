# Qt 顏色主題設定
COLORS = {
    'bg_dark': '#1B2838',     # 深藍黑色背景
    'bg_medium': '#2A475E',   # 中度藍色
    'bg_light': '#415A77',    # 較亮的藍色
    'text': '#E0E1DD',        # 文字顏色
    'text_gray': '#C1DBEE',   # 次要文字顏色
    'accent': '#66C0F4',      # 強調色
    'accent_hover': '#A4D7F5', # 懸停顏色
    'warning': '#FF6B6B',     # 警告色
    'success': '#4CAF50',     # 成功色
    'border': '#2A475E',      # 邊框顏色
}

# 樣式表
STYLESHEET = """
QMainWindow {
    background-color: """ + COLORS['bg_dark'] + """;
}

QLabel {
    color: """ + COLORS['text'] + """;
    font-family: "Microsoft JhengHei UI", "PingFang TC", sans-serif;
}

QPushButton {
    background-color: """ + COLORS['bg_light'] + """;
    color: """ + COLORS['text'] + """;
    border: none;
    border-radius: 5px;
    padding: 8px 15px;
    font-family: "Microsoft JhengHei UI", "PingFang TC", sans-serif;
}

QPushButton:hover {
    background-color: """ + COLORS['accent'] + """;
}

QTableWidget {
    background-color: """ + COLORS['bg_dark'] + """;
    color: """ + COLORS['text'] + """;
    gridline-color: """ + COLORS['bg_medium'] + """;
    border: none;
    selection-background-color: """ + COLORS['bg_dark'] + """;
    selection-color: """ + COLORS['text'] + """;
}

QTableWidget::item {
    padding: 5px;
    border: none;
}

QTableWidget::item:selected {
    background-color: """ + COLORS['bg_dark'] + """;
    color: """ + COLORS['text'] + """;
}

QHeaderView::section {
    background-color: """ + COLORS['bg_medium'] + """;
    color: """ + COLORS['text'] + """;
    padding: 5px;
    border: none;
    font-weight: bold;
}

QHeaderView::section:hover {
    background-color: """ + COLORS['accent'] + """;
}

QLineEdit {
    background-color: """ + COLORS['bg_medium'] + """;
    color: """ + COLORS['text'] + """;
    border: none;
    border-radius: 5px;
    padding: 5px;
    font-family: "Microsoft JhengHei UI", "PingFang TC", sans-serif;
}

QComboBox {
    background-color: """ + COLORS['bg_medium'] + """;
    color: """ + COLORS['text'] + """;
    border: none;
    border-radius: 5px;
    padding: 5px;
    font-family: "Microsoft JhengHei UI", "PingFang TC", sans-serif;
}

QComboBox::drop-down {
    border: none;
}

QComboBox::down-arrow {
    image: none;
    border: none;
}

QComboBox QAbstractItemView {
    background-color: """ + COLORS['bg_medium'] + """;
    color: """ + COLORS['text'] + """;
    selection-background-color: """ + COLORS['accent'] + """;
}
"""