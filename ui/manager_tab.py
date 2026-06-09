from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QFormLayout, QLineEdit, QDoubleSpinBox,
    QSpinBox, QComboBox, QTextEdit, QLabel, QMessageBox,
)
from PyQt5.QtCore import Qt

from database.db_manager import (
    get_all_products, get_categories, add_product,
    update_product, delete_product,
)


class ManagerTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        btn_row = QHBoxLayout()
        self.btn_add = QPushButton("Добавить товар")
        self.btn_add.setObjectName("btn_success")
        self.btn_add.setStyleSheet(
            "QPushButton{background:#2ECC71;color:white;border-radius:6px;padding:7px 16px;font-weight:bold;}"
            "QPushButton:hover{background:#27AE60;}"
        )
        self.btn_edit = QPushButton("Редактировать")
        self.btn_delete = QPushButton("Удалить")
        self.btn_delete.setStyleSheet(
            "QPushButton{background:#E74C3C;color:white;border-radius:6px;padding:7px 16px;font-weight:bold;}"
            "QPushButton:hover{background:#C0392B;}"
        )

        self.btn_add.clicked.connect(self._on_add)
        self.btn_edit.clicked.connect(self._on_edit)
        self.btn_delete.clicked.connect(self._on_delete)

        btn_row.addWidget(self.btn_add)
        btn_row.addWidget(self.btn_edit)
        btn_row.addWidget(self.btn_delete)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        self.table = QTableWidget()
        cols = ["ID", "Наименование", "Категория", "Цена", "Кол-во", "Скидка %"]
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

    def _load_data(self):
        products = get_all_products()
        self.table.setRowCount(len(products))
        for row_idx, prod in enumerate(products):
            (prod_id, name, category, description, manufacturer,
             supplier, price, unit, quantity, discount, image_path) = prod
            vals = [str(prod_id), name or "", category or "",
                    f"{price:.2f}", str(quantity or 0), f"{discount or 0:.0f}%"]
            for col, val in enumerate(vals):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, col, item)

    def _selected_product_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 0)
        return int(item.text()) if item else None

    def _on_add(self):
        dlg = ProductDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            data = dlg.get_data()
            add_product(**data)
            self._load_data()

    def _on_edit(self):
        prod_id = self._selected_product_id()
        if prod_id is None:
            QMessageBox.warning(self, "Внимание", "Выберите товар для редактирования.")
            return
        products = get_all_products()
        prod = next((p for p in products if p[0] == prod_id), None)
        if not prod:
            return
        dlg = ProductDialog(self, prod)
        if dlg.exec_() == QDialog.Accepted:
            data = dlg.get_data()
            update_product(
                prod_id,
                data["name"], data["category_id"], data["description"],
                data["manufacturer"], data["supplier"], data["price"],
                data["unit"], data["quantity"], data["discount"],
            )
            self._load_data()

    def _on_delete(self):
        prod_id = self._selected_product_id()
        if prod_id is None:
            QMessageBox.warning(self, "Внимание", "Выберите товар для удаления.")
            return
        reply = QMessageBox.question(
            self, "Подтверждение",
            "Вы уверены, что хотите удалить этот товар?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            delete_product(prod_id)
            self._load_data()


class ProductDialog(QDialog):
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.product = product
        self.setWindowTitle("Товар" if product is None else "Редактировать товар")
        self.setMinimumWidth(460)
        self._build_ui()
        if product:
            self._fill_fields(product)

    def _build_ui(self):
        layout = QFormLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        self.inp_name = QLineEdit()
        self.cbo_category = QComboBox()
        for cat_id, cat_name in get_categories():
            self.cbo_category.addItem(cat_name, cat_id)
        self.inp_description = QTextEdit()
        self.inp_description.setFixedHeight(70)
        self.inp_manufacturer = QLineEdit()
        self.inp_supplier = QLineEdit()
        self.spn_price = QDoubleSpinBox()
        self.spn_price.setRange(0, 9_999_999)
        self.spn_price.setDecimals(2)
        self.inp_unit = QLineEdit()
        self.spn_qty = QSpinBox()
        self.spn_qty.setRange(0, 999_999)
        self.spn_discount = QDoubleSpinBox()
        self.spn_discount.setRange(0, 100)
        self.spn_discount.setDecimals(1)

        layout.addRow("Наименование *",  self.inp_name)
        layout.addRow("Категория",        self.cbo_category)
        layout.addRow("Описание",         self.inp_description)
        layout.addRow("Производитель",    self.inp_manufacturer)
        layout.addRow("Поставщик",        self.inp_supplier)
        layout.addRow("Цена *",           self.spn_price)
        layout.addRow("Ед. изм.",         self.inp_unit)
        layout.addRow("Количество",       self.spn_qty)
        layout.addRow("Скидка %",         self.spn_discount)

        btn_row = QHBoxLayout()
        btn_ok = QPushButton("Сохранить")
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

    def _fill_fields(self, prod):
        (prod_id, name, category, description, manufacturer,
         supplier, price, unit, quantity, discount, image_path) = prod
        self.inp_name.setText(name or "")
        if category:
            idx = self.cbo_category.findText(category)
            if idx >= 0:
                self.cbo_category.setCurrentIndex(idx)
        self.inp_description.setPlainText(description or "")
        self.inp_manufacturer.setText(manufacturer or "")
        self.inp_supplier.setText(supplier or "")
        self.spn_price.setValue(price or 0)
        self.inp_unit.setText(unit or "")
        self.spn_qty.setValue(quantity or 0)
        self.spn_discount.setValue(discount or 0)

    def _on_save(self):
        if not self.inp_name.text().strip():
            QMessageBox.warning(self, "Ошибка", "Укажите наименование товара.")
            return
        self.accept()

    def get_data(self):
        return {
            "name":         self.inp_name.text().strip(),
            "category_id":  self.cbo_category.currentData(),
            "description":  self.inp_description.toPlainText().strip(),
            "manufacturer": self.inp_manufacturer.text().strip(),
            "supplier":     self.inp_supplier.text().strip(),
            "price":        self.spn_price.value(),
            "unit":         self.inp_unit.text().strip(),
            "quantity":     self.spn_qty.value(),
            "discount":     self.spn_discount.value(),
            "image_path":   None,
        }
