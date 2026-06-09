from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QFormLayout, QLineEdit, QComboBox,
    QLabel, QMessageBox,
)
from PyQt5.QtCore import Qt

from database.db_manager import get_all_users, get_roles, add_user, delete_user

ROLE_DISPLAY = {
    "admin":   "Администратор",
    "manager": "Менеджер",
    "client":  "Клиент",
    "guest":   "Гость",
}


class AdminTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        btn_row = QHBoxLayout()
        self.btn_add = QPushButton("Добавить пользователя")
        self.btn_add.setStyleSheet(
            "QPushButton{background:#2ECC71;color:white;border-radius:6px;padding:7px 16px;font-weight:bold;}"
            "QPushButton:hover{background:#27AE60;}"
        )
        self.btn_delete = QPushButton("Удалить пользователя")
        self.btn_delete.setStyleSheet(
            "QPushButton{background:#E74C3C;color:white;border-radius:6px;padding:7px 16px;font-weight:bold;}"
            "QPushButton:hover{background:#C0392B;}"
        )
        self.btn_add.clicked.connect(self._on_add)
        self.btn_delete.clicked.connect(self._on_delete)

        btn_row.addWidget(self.btn_add)
        btn_row.addWidget(self.btn_delete)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        self.table = QTableWidget()
        cols = ["ID", "Логин", "ФИО", "Роль"]
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

    def _load_data(self):
        users = get_all_users()
        self.table.setRowCount(len(users))
        for row_idx, (user_id, login, full_name, role) in enumerate(users):
            vals = [str(user_id), login, full_name, ROLE_DISPLAY.get(role, role)]
            for col, val in enumerate(vals):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, col, item)

    def _selected_user_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 0)
        return int(item.text()) if item else None

    def _on_add(self):
        dlg = UserDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            data = dlg.get_data()
            try:
                add_user(**data)
                self._load_data()
            except Exception as exc:
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить: {exc}")

    def _on_delete(self):
        user_id = self._selected_user_id()
        if user_id is None:
            QMessageBox.warning(self, "Внимание", "Выберите пользователя.")
            return
        reply = QMessageBox.question(
            self, "Подтверждение",
            "Удалить выбранного пользователя?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            delete_user(user_id)
            self._load_data()


class UserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Новый пользователь")
        self.setMinimumWidth(380)
        self._build_ui()

    def _build_ui(self):
        layout = QFormLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        self.inp_login = QLineEdit()
        self.inp_password = QLineEdit()
        self.inp_password.setEchoMode(QLineEdit.Password)
        self.inp_full_name = QLineEdit()
        self.cbo_role = QComboBox()
        for role_id, role_name in get_roles():
            self.cbo_role.addItem(ROLE_DISPLAY.get(role_name, role_name), role_id)

        layout.addRow("Логин *",    self.inp_login)
        layout.addRow("Пароль *",   self.inp_password)
        layout.addRow("ФИО *",      self.inp_full_name)
        layout.addRow("Роль",       self.cbo_role)

        btn_row = QHBoxLayout()
        btn_ok = QPushButton("Создать")
        btn_ok.setStyleSheet(
            "QPushButton{background:#3498DB;color:white;border-radius:6px;padding:8px 20px;font-weight:bold;}"
            "QPushButton:hover{background:#2980B9;}"
        )
        btn_cancel = QPushButton("Отмена")
        btn_cancel.setStyleSheet(
            "QPushButton{background:#7F8C8D;color:white;border-radius:6px;padding:8px 20px;}"
            "QPushButton:hover{background:#626567;}"
        )
        btn_ok.clicked.connect(self._on_save)
        btn_cancel.clicked.connect(self.reject)
        btn_row.addWidget(btn_ok)
        btn_row.addWidget(btn_cancel)
        layout.addRow(btn_row)

    def _on_save(self):
        if not self.inp_login.text().strip():
            QMessageBox.warning(self, "Ошибка", "Укажите логин.")
            return
        if not self.inp_password.text():
            QMessageBox.warning(self, "Ошибка", "Укажите пароль.")
            return
        if not self.inp_full_name.text().strip():
            QMessageBox.warning(self, "Ошибка", "Укажите ФИО.")
            return
        self.accept()

    def get_data(self):
        return {
            "login":     self.inp_login.text().strip(),
            "password":  self.inp_password.text(),
            "full_name": self.inp_full_name.text().strip(),
            "role_id":   self.cbo_role.currentData(),
        }
