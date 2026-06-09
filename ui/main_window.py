import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QTabWidget,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon

from ui.products_widget import ProductsWidget

RESOURCES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources")

ROLE_TITLES = {
    "guest":   "Гость",
    "client":  "Клиент",
    "manager": "Менеджер",
    "admin":   "Администратор",
}


class MainWindow(QMainWindow):
    def __init__(self, user: dict, login_window):
        super().__init__()
        self.user = user
        self.login_window = login_window
        role = user.get("role", "guest")

        self.setWindowTitle(f"Магазин — {ROLE_TITLES.get(role, role)}")
        self.resize(1200, 750)
        self._set_icon()
        self._build_ui(role)

    def _set_icon(self):
        icon_path = os.path.join(RESOURCES_DIR, "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def _build_ui(self, role):
        root = QWidget()
        self.setCentralWidget(root)
        root.setStyleSheet("background-color: #ECF0F1;")
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        header = self._build_header(role)
        root_layout.addWidget(header)

        content = QWidget()
        content.setStyleSheet("background-color: #ECF0F1;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(16, 16, 16, 16)

        tabs = self._build_tabs(role)
        content_layout.addWidget(tabs)

        root_layout.addWidget(content, 1)

    def _build_header(self, role):
        header = QFrame()
        header.setObjectName("frame_header")
        header.setStyleSheet("background-color: #2C3E50;")
        header.setFixedHeight(64)

        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(20, 0, 20, 0)

        logo_path = os.path.join(RESOURCES_DIR, "logo.png")
        if os.path.exists(logo_path):
            logo_lbl = QLabel()
            pix = QPixmap(logo_path).scaled(
                100, 44, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            logo_lbl.setPixmap(pix)
            h_layout.addWidget(logo_lbl)

        app_name = QLabel("Система управления магазином")
        app_name.setStyleSheet(
            "color: white; font-size: 16px; font-weight: bold; background: transparent;"
        )
        h_layout.addWidget(app_name)
        h_layout.addStretch()

        role_badge = QLabel(ROLE_TITLES.get(role, role))
        role_badge.setStyleSheet(
            "color: #F39C12; font-size: 12px; font-weight: bold; background: transparent;"
        )
        h_layout.addWidget(role_badge)
        h_layout.addSpacing(12)

        user_lbl = QLabel(self.user.get("full_name", ""))
        user_lbl.setObjectName("lbl_user_info")
        user_lbl.setStyleSheet(
            "color: white; font-size: 13px; font-weight: bold; background: transparent;"
        )
        h_layout.addWidget(user_lbl)
        h_layout.addSpacing(16)

        btn_logout = QPushButton("Выйти")
        btn_logout.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border-radius: 6px;
                padding: 6px 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #C0392B; }
        """)
        btn_logout.clicked.connect(self._on_logout)
        h_layout.addWidget(btn_logout)

        return header

    def _build_tabs(self, role):
        tabs = QTabWidget()

        tabs.addTab(ProductsWidget(), "Список товаров")

        if role == "client":
            from ui.client_tab import ClientTab
            tabs.addTab(ClientTab(self.user), "Мой профиль")

        elif role == "manager":
            from ui.manager_tab import ManagerTab
            tabs.addTab(ManagerTab(), "Управление товарами")

        elif role == "admin":
            from ui.manager_tab import ManagerTab
            from ui.admin_tab import AdminTab
            tabs.addTab(ManagerTab(), "Управление товарами")
            tabs.addTab(AdminTab(), "Управление пользователями")

        return tabs

    def _on_logout(self):
        self.close()
        self.login_window.input_login.clear()
        self.login_window.input_password.clear()
        self.login_window.lbl_error.setText("")
        self.login_window.show()
