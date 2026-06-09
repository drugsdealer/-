import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QHeaderView, QPushButton, QLineEdit, QComboBox, QMessageBox,
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QColor, QFont, QBrush

from database.db_manager import get_all_products, get_categories
from ui.styles import DISCOUNT_HIGH_BG, OUT_OF_STOCK_BG

RESOURCES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources")
PLACEHOLDER_IMAGE = os.path.join(RESOURCES_DIR, "picture.png")

COLUMNS = [
    "Фото", "Наименование", "Категория", "Описание",
    "Производитель", "Поставщик", "Цена", "Ед. изм.",
    "Кол-во", "Скидка %",
]
COL_PHOTO        = 0
COL_NAME         = 1
COL_CATEGORY     = 2
COL_DESCRIPTION  = 3
COL_MANUFACTURER = 4
COL_SUPPLIER     = 5
COL_PRICE        = 6
COL_UNIT         = 7
COL_QTY          = 8
COL_DISCOUNT     = 9


class ProductsWidget(QWidget):
    def __init__(self, parent=None, show_actions=False):
        super().__init__(parent)
        self.show_actions = show_actions
        self._build_ui()
        self.load_products()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        filter_row = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по наименованию...")
        self.search_input.textChanged.connect(self._apply_filter)

        self.category_filter = QComboBox()
        self.category_filter.addItem("Все категории", None)
        for cat_id, cat_name in get_categories():
            self.category_filter.addItem(cat_name, cat_id)
        self.category_filter.currentIndexChanged.connect(self._apply_filter)

        btn_refresh = QPushButton("Обновить")
        btn_refresh.setFixedWidth(100)
        btn_refresh.clicked.connect(self.load_products)

        filter_row.addWidget(QLabel("Поиск:"))
        filter_row.addWidget(self.search_input, 3)
        filter_row.addWidget(QLabel("Категория:"))
        filter_row.addWidget(self.category_filter, 2)
        filter_row.addWidget(btn_refresh)
        layout.addLayout(filter_row)

        legend_row = QHBoxLayout()
        for color, text in [
            (DISCOUNT_HIGH_BG, "Скидка > 12%"),
            (OUT_OF_STOCK_BG,  "Нет на складе"),
        ]:
            lbl_box = QLabel("  ")
            lbl_box.setFixedWidth(22)
            lbl_box.setStyleSheet(f"background-color: {color}; border: 1px solid #999;")
            lbl_text = QLabel(text)
            legend_row.addWidget(lbl_box)
            legend_row.addWidget(lbl_text)
            legend_row.addSpacing(16)
        legend_row.addStretch()
        layout.addLayout(legend_row)

        self.table = QTableWidget()
        self.table.setColumnCount(len(COLUMNS))
        self.table.setHorizontalHeaderLabels(COLUMNS)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setDefaultSectionSize(70)
        self.table.setShowGrid(True)

        col_widths = [80, 180, 120, 200, 120, 120, 100, 70, 70, 80]
        for i, w in enumerate(col_widths):
            self.table.setColumnWidth(i, w)

        layout.addWidget(self.table)

    def load_products(self):
        self._all_products = get_all_products()
        self._apply_filter()

    def _apply_filter(self):
        search_text = self.search_input.text().strip().lower()
        selected_cat_id = self.category_filter.currentData()

        filtered = []
        for row in self._all_products:
            prod_name = (row[1] or "").lower()
            cat_name  = (row[2] or "")
            cat_id    = None
            if selected_cat_id is not None:
                cats = get_categories()
                for cid, cname in cats:
                    if cname == cat_name:
                        cat_id = cid
                        break
            if search_text and search_text not in prod_name:
                continue
            if selected_cat_id is not None and cat_id != selected_cat_id:
                continue
            filtered.append(row)

        self._fill_table(filtered)

    def _fill_table(self, products):
        self.table.setRowCount(len(products))

        placeholder_pixmap = self._load_placeholder()

        for row_idx, prod in enumerate(products):
            (prod_id, name, category, description, manufacturer,
             supplier, price, unit, quantity, discount, image_path) = prod

            discount = discount or 0.0
            quantity = quantity or 0

            row_bg = None
            if quantity == 0:
                row_bg = QColor(OUT_OF_STOCK_BG)
            elif discount > 12:
                row_bg = QColor(DISCOUNT_HIGH_BG)

            photo_label = QLabel()
            photo_label.setAlignment(Qt.AlignCenter)
            pixmap = None
            if image_path and os.path.exists(image_path):
                pixmap = QPixmap(image_path)
            if pixmap is None or pixmap.isNull():
                pixmap = placeholder_pixmap
            if pixmap and not pixmap.isNull():
                photo_label.setPixmap(
                    pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
            self.table.setCellWidget(row_idx, COL_PHOTO, photo_label)

            self._set_item(row_idx, COL_NAME,         name or "",        row_bg)
            self._set_item(row_idx, COL_CATEGORY,     category or "",    row_bg)
            self._set_item(row_idx, COL_DESCRIPTION,  description or "", row_bg)
            self._set_item(row_idx, COL_MANUFACTURER, manufacturer or "",row_bg)
            self._set_item(row_idx, COL_SUPPLIER,     supplier or "",    row_bg)

            price_widget = self._build_price_widget(price, discount, row_bg)
            self.table.setCellWidget(row_idx, COL_PRICE, price_widget)

            self._set_item(row_idx, COL_UNIT,     unit or "",       row_bg)
            self._set_item(row_idx, COL_QTY,      str(quantity),    row_bg, center=True)
            self._set_item(row_idx, COL_DISCOUNT, f"{discount:.0f}%", row_bg, center=True)

            if row_bg:
                for col in [COL_UNIT, COL_QTY, COL_DISCOUNT]:
                    item = self.table.item(row_idx, col)
                    if item:
                        item.setBackground(QBrush(row_bg))

    def _set_item(self, row, col, text, bg_color=None, center=False):
        item = QTableWidgetItem(text)
        if center:
            item.setTextAlignment(Qt.AlignCenter)
        if bg_color:
            item.setBackground(QBrush(bg_color))
        self.table.setItem(row, col, item)

    def _build_price_widget(self, price, discount, bg_color=None):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignCenter)

        if bg_color:
            widget.setStyleSheet(f"background-color: {bg_color.name()};")

        if discount > 0:
            original_lbl = QLabel(f"{price:,.2f} ₽".replace(",", " "))
            font = QFont()
            font.setStrikeOut(True)
            original_lbl.setFont(font)
            original_lbl.setStyleSheet("color: #E74C3C;")
            original_lbl.setAlignment(Qt.AlignCenter)

            final_price = price * (1 - discount / 100)
            final_lbl = QLabel(f"{final_price:,.2f} ₽".replace(",", " "))
            final_lbl.setStyleSheet("color: #2C3E50; font-weight: bold;")
            final_lbl.setAlignment(Qt.AlignCenter)

            layout.addWidget(original_lbl)
            layout.addWidget(final_lbl)
        else:
            price_lbl = QLabel(f"{price:,.2f} ₽".replace(",", " "))
            price_lbl.setAlignment(Qt.AlignCenter)
            layout.addWidget(price_lbl)

        return widget

    def _load_placeholder(self):
        if os.path.exists(PLACEHOLDER_IMAGE):
            return QPixmap(PLACEHOLDER_IMAGE)
        pixmap = QPixmap(60, 60)
        pixmap.fill(QColor("#BDC3C7"))
        return pixmap
