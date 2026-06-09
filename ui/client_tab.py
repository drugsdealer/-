from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QGroupBox,
)
from PyQt5.QtCore import Qt


class ClientTab(QWidget):
    def __init__(self, user: dict, parent=None):
        super().__init__(parent)
        self.user = user
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignTop)

        group = QGroupBox("Информация о профиле")
        group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        form = QFormLayout(group)
        form.setSpacing(12)

        full_name_lbl = QLabel(self.user.get("full_name", "—"))
        full_name_lbl.setStyleSheet("font-size: 14px;")

        role_map = {
            "client": "Клиент",
            "manager": "Менеджер",
            "admin": "Администратор",
            "guest": "Гость",
        }
        role_lbl = QLabel(role_map.get(self.user.get("role", ""), "—"))
        role_lbl.setStyleSheet("font-size: 14px;")

        form.addRow("ФИО:", full_name_lbl)
        form.addRow("Роль:", role_lbl)

        layout.addWidget(group)
        layout.addStretch()
