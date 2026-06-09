PRIMARY_COLOR = "#2C3E50"
ACCENT_COLOR = "#3498DB"
LIGHT_BG = "#ECF0F1"
WHITE = "#FFFFFF"
DANGER_COLOR = "#E74C3C"
SUCCESS_COLOR = "#2ECC71"
WARNING_COLOR = "#F39C12"

DISCOUNT_HIGH_BG = "#F4A460"
OUT_OF_STOCK_BG = "#ADD8E6"

APP_STYLE = """
QMainWindow, QDialog {
    background-color: #ECF0F1;
}

QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
    color: #2C3E50;
}

QPushButton {
    background-color: #3498DB;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 18px;
    font-size: 13px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #2980B9;
}

QPushButton:pressed {
    background-color: #1F618D;
}

QPushButton#btn_danger {
    background-color: #E74C3C;
}

QPushButton#btn_danger:hover {
    background-color: #C0392B;
}

QPushButton#btn_success {
    background-color: #2ECC71;
}

QPushButton#btn_success:hover {
    background-color: #27AE60;
}

QPushButton#btn_secondary {
    background-color: #7F8C8D;
}

QPushButton#btn_secondary:hover {
    background-color: #626567;
}

QLineEdit {
    border: 2px solid #BDC3C7;
    border-radius: 6px;
    padding: 7px 12px;
    font-size: 13px;
    background-color: white;
}

QLineEdit:focus {
    border-color: #3498DB;
}

QLabel#lbl_title {
    font-size: 22px;
    font-weight: bold;
    color: #2C3E50;
}

QLabel#lbl_subtitle {
    font-size: 15px;
    color: #7F8C8D;
}

QLabel#lbl_user_info {
    font-size: 13px;
    font-weight: bold;
    color: white;
    padding: 4px 10px;
}

QFrame#frame_header {
    background-color: #2C3E50;
    border-radius: 0px;
}

QFrame#frame_login_card {
    background-color: white;
    border-radius: 12px;
}

QTableWidget {
    border: 1px solid #BDC3C7;
    border-radius: 6px;
    gridline-color: #D5D8DC;
    background-color: white;
    alternate-background-color: #F8F9FA;
    selection-background-color: #3498DB;
    selection-color: white;
}

QTableWidget::item {
    padding: 6px;
}

QHeaderView::section {
    background-color: #2C3E50;
    color: white;
    padding: 8px;
    font-weight: bold;
    border: none;
    border-right: 1px solid #4A6278;
}

QTabWidget::pane {
    border: 1px solid #BDC3C7;
    border-radius: 6px;
    background-color: white;
}

QTabBar::tab {
    background-color: #BDC3C7;
    color: #2C3E50;
    padding: 8px 18px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-weight: bold;
}

QTabBar::tab:selected {
    background-color: #3498DB;
    color: white;
}

QComboBox {
    border: 2px solid #BDC3C7;
    border-radius: 6px;
    padding: 6px 10px;
    background-color: white;
}

QComboBox:focus {
    border-color: #3498DB;
}

QSpinBox, QDoubleSpinBox {
    border: 2px solid #BDC3C7;
    border-radius: 6px;
    padding: 6px 10px;
    background-color: white;
}

QSpinBox:focus, QDoubleSpinBox:focus {
    border-color: #3498DB;
}

QTextEdit {
    border: 2px solid #BDC3C7;
    border-radius: 6px;
    padding: 6px;
    background-color: white;
}

QTextEdit:focus {
    border-color: #3498DB;
}

QMessageBox {
    background-color: #ECF0F1;
}

QScrollBar:vertical {
    border: none;
    background: #F0F0F0;
    width: 10px;
}

QScrollBar::handle:vertical {
    background: #BDC3C7;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #95A5A6;
}
"""
