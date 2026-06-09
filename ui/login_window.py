import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QMessageBox,
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon

from database.db_manager import authenticate_user

RESOURCES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources")


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Магазин — Вход в систему")
        self.setFixedSize(460, 520)
        self._set_icon()
        self._build_ui()

    def _set_icon(self):
        icon_path = os.path.join(RESOURCES_DIR, "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet("background-color: #ECF0F1;")

        outer = QVBoxLayout(central)
        outer.setAlignment(Qt.AlignCenter)
        outer.setContentsMargins(30, 30, 30, 30)

        card = QFrame()
        card.setObjectName("frame_login_card")
        card.setStyleSheet("""
            QFrame#frame_login_card {
                background-color: white;
                border-radius: 14px;
                border: 1px solid #D5D8DC;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(36, 32, 36, 32)
        card_layout.setSpacing(16)

        logo_path = os.path.join(RESOURCES_DIR, "logo.png")
        if os.path.exists(logo_path):
            logo_lbl = QLabel()
            pix = QPixmap(logo_path).scaled(
                120, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            logo_lbl.setPixmap(pix)
            logo_lbl.setAlignment(Qt.AlignCenter)
            card_layout.addWidget(logo_lbl)

        title = QLabel("Вход в систему")
        title.setObjectName("lbl_title")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #2C3E50;")
        card_layout.addWidget(title)

        subtitle = QLabel("Введите логин и пароль для входа")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #7F8C8D; font-size: 12px;")
        card_layout.addWidget(subtitle)

        card_layout.addSpacing(8)

        lbl_login = QLabel("Логин")
        lbl_login.setStyleSheet("font-weight: bold; color: #2C3E50;")
        card_layout.addWidget(lbl_login)

        self.input_login = QLineEdit()
        self.input_login.setPlaceholderText("Введите логин")
        self.input_login.setMinimumHeight(40)
        card_layout.addWidget(self.input_login)

        lbl_password = QLabel("Пароль")
        lbl_password.setStyleSheet("font-weight: bold; color: #2C3E50;")
        card_layout.addWidget(lbl_password)

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Введите пароль")
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setMinimumHeight(40)
        self.input_password.returnPressed.connect(self._on_login)
        card_layout.addWidget(self.input_password)

        card_layout.addSpacing(8)

        btn_login = QPushButton("Войти")
        btn_login.setMinimumHeight(44)
        btn_login.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2980B9; }
            QPushButton:pressed { background-color: #1F618D; }
        """)
        btn_login.clicked.connect(self._on_login)
        card_layout.addWidget(btn_login)

        divider = QLabel("— или —")
        divider.setAlignment(Qt.AlignCenter)
        divider.setStyleSheet("color: #BDC3C7; font-size: 12px;")
        card_layout.addWidget(divider)

        btn_guest = QPushButton("Продолжить как гость")
        btn_guest.setMinimumHeight(40)
        btn_guest.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #3498DB;
                border: 2px solid #3498DB;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #EBF5FB; }
        """)
        btn_guest.clicked.connect(self._on_guest)
        card_layout.addWidget(btn_guest)

        self.lbl_error = QLabel("")
        self.lbl_error.setAlignment(Qt.AlignCenter)
        self.lbl_error.setStyleSheet("color: #E74C3C; font-size: 12px;")
        card_layout.addWidget(self.lbl_error)

        outer.addWidget(card)

        hint = QLabel("Тестовые аккаунты: admin/admin123 · manager/manager123 · client/client123")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("color: #95A5A6; font-size: 11px;")
        outer.addWidget(hint)

    def _on_login(self):
        login = self.input_login.text().strip()
        password = self.input_password.text()

        if not login or not password:
            self.lbl_error.setText("Заполните все поля")
            return

        user = authenticate_user(login, password)
        if user is None:
            self.lbl_error.setText("Неверный логин или пароль")
            self.input_password.clear()
            return

        self.lbl_error.setText("")
        self._open_main_window(user)

    def _on_guest(self):
        user = {"id": None, "full_name": "Гость", "role": "guest"}
        self._open_main_window(user)

    def _open_main_window(self, user):
        from ui.main_window import MainWindow
        self.main_win = MainWindow(user, self)
        self.main_win.show()
        self.hide()
