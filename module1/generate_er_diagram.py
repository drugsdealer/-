"""
Генерация ER-диаграммы базы данных СтройМатериалы в формате PDF.
Содержит: таблицы, атрибуты, PK/FK, связи между таблицами.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import HexColor, white, black

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "er_diagram.pdf")

PAGE_W, PAGE_H = landscape(A3)

C_HEADER_BG  = HexColor("#2C3E50")
C_HEADER_TXT = white
C_PK_BG      = HexColor("#D6EAF8")
C_FK_BG      = HexColor("#D5F5E3")
C_ROW_BG     = HexColor("#FDFEFE")
C_ROW_ALT    = HexColor("#F2F3F4")
C_BORDER     = HexColor("#7F8C8D")
C_LINE_PK    = HexColor("#2980B9")
C_LINE_FK    = HexColor("#27AE60")
C_TITLE_BG   = HexColor("#1A252F")

COL_W   = 58 * mm
ROW_H   = 7  * mm
HEAD_H  = 9  * mm
FONT_S  = 7.5
FONT_B  = 8.5


# ─── Шрифты ──────────────────────────────────────────────────────────────────
FONT_PATHS = [
    r"C:\Windows\Fonts",
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
    os.path.dirname(__file__),
]


def _find_font(names):
    for d in FONT_PATHS:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return p
    return None


def _register():
    reg = pdfmetrics.getRegisteredFontNames()
    if "ERFont" not in reg:
        p = _find_font(["arial.ttf", "Arial.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"])
        if p:
            pdfmetrics.registerFont(TTFont("ERFont", p))
    if "ERFont-Bold" not in reg:
        p = _find_font(["arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"])
        if p:
            pdfmetrics.registerFont(TTFont("ERFont-Bold", p))


def font(bold=False):
    names = pdfmetrics.getRegisteredFontNames()
    if bold and "ERFont-Bold" in names:
        return "ERFont-Bold"
    if not bold and "ERFont" in names:
        return "ERFont"
    return "Helvetica-Bold" if bold else "Helvetica"


# ─── Определение таблиц ──────────────────────────────────────────────────────
# Формат колонки: (имя, тип_данных, метка)  метка: "PK" | "FK" | ""
TABLES = {
    "roles": {
        "title": "roles",
        "cols": [
            ("role_id",   "SERIAL",      "PK"),
            ("role_name", "VARCHAR(50)", ""),
        ],
    },
    "users": {
        "title": "users",
        "cols": [
            ("user_id",   "SERIAL",       "PK"),
            ("full_name", "VARCHAR(150)", ""),
            ("login",     "VARCHAR(100)", ""),
            ("password",  "VARCHAR(100)", ""),
            ("role_id",   "INTEGER",      "FK → roles"),
        ],
    },
    "categories": {
        "title": "categories",
        "cols": [
            ("category_id",   "SERIAL",       "PK"),
            ("category_name", "VARCHAR(150)", ""),
        ],
    },
    "units": {
        "title": "units",
        "cols": [
            ("unit_id",   "SERIAL",     "PK"),
            ("unit_name", "VARCHAR(20)", ""),
        ],
    },
    "suppliers": {
        "title": "suppliers",
        "cols": [
            ("supplier_id",   "SERIAL",       "PK"),
            ("supplier_name", "VARCHAR(150)", ""),
        ],
    },
    "manufacturers": {
        "title": "manufacturers",
        "cols": [
            ("manufacturer_id",   "SERIAL",       "PK"),
            ("manufacturer_name", "VARCHAR(150)", ""),
        ],
    },
    "products": {
        "title": "products",
        "cols": [
            ("product_id",      "SERIAL",        "PK"),
            ("article",         "VARCHAR(20)",   ""),
            ("product_name",    "VARCHAR(250)",  ""),
            ("unit_id",         "INTEGER",       "FK → units"),
            ("price",           "NUMERIC(12,2)", ""),
            ("supplier_id",     "INTEGER",       "FK → suppliers"),
            ("manufacturer_id", "INTEGER",       "FK → manufacturers"),
            ("category_id",     "INTEGER",       "FK → categories"),
            ("discount",        "NUMERIC(5,2)",  ""),
            ("quantity_stock",  "INTEGER",       ""),
            ("description",     "TEXT",          ""),
            ("image_path",      "VARCHAR(255)",  ""),
        ],
    },
    "pickup_points": {
        "title": "pickup_points",
        "cols": [
            ("pickup_point_id", "SERIAL",       "PK"),
            ("address",         "VARCHAR(300)", ""),
        ],
    },
    "order_statuses": {
        "title": "order_statuses",
        "cols": [
            ("status_id",   "SERIAL",     "PK"),
            ("status_name", "VARCHAR(50)", ""),
        ],
    },
    "orders": {
        "title": "orders",
        "cols": [
            ("order_id",        "SERIAL",        "PK"),
            ("user_id",         "INTEGER",       "FK → users"),
            ("order_date",      "TIMESTAMP",     ""),
            ("pickup_point_id", "INTEGER",       "FK → pickup_points"),
            ("status_id",       "INTEGER",       "FK → order_statuses"),
            ("total_amount",    "NUMERIC(14,2)", ""),
        ],
    },
    "order_items": {
        "title": "order_items",
        "cols": [
            ("item_id",    "SERIAL",        "PK"),
            ("order_id",   "INTEGER",       "FK → orders"),
            ("product_id", "INTEGER",       "FK → products"),
            ("quantity",   "INTEGER",       ""),
            ("price",      "NUMERIC(12,2)", ""),
        ],
    },
}

# Позиции таблиц (левый нижний угол) x, y в mm от нижнего левого угла страницы
POSITIONS = {
    "roles":          ( 10,  165),
    "users":          ( 80,  155),
    "categories":     (230,  185),
    "units":          (230,  155),
    "suppliers":      (230,  125),
    "manufacturers":  (230,   95),
    "products":       (155,   85),
    "pickup_points":  ( 10,   75),
    "order_statuses": ( 80,   45),
    "orders":         ( 80,  100),
    "order_items":    (155,   30),
}

# Связи (от FK-таблицы к PK-таблице): (from_table, from_col, to_table, to_col)
RELATIONS = [
    ("users",        "role_id",         "roles",          "role_id"),
    ("products",     "unit_id",         "units",          "unit_id"),
    ("products",     "supplier_id",     "suppliers",      "supplier_id"),
    ("products",     "manufacturer_id", "manufacturers",  "manufacturer_id"),
    ("products",     "category_id",     "categories",     "category_id"),
    ("orders",       "user_id",         "users",          "user_id"),
    ("orders",       "pickup_point_id", "pickup_points",  "pickup_point_id"),
    ("orders",       "status_id",       "order_statuses", "status_id"),
    ("order_items",  "order_id",        "orders",         "order_id"),
    ("order_items",  "product_id",      "products",       "product_id"),
]


def table_height(tbl_key):
    return HEAD_H + len(TABLES[tbl_key]["cols"]) * ROW_H


def table_rect(tbl_key):
    """Возвращает (x, y, w, h) в pt."""
    px, py = POSITIONS[tbl_key]
    x = px * mm
    y = py * mm
    w = COL_W
    h = table_height(tbl_key)
    return x, y, w, h


def col_y_center(tbl_key, col_name):
    """Y-центр строки колонки в pt."""
    x, y, w, h = table_rect(tbl_key)
    cols = TABLES[tbl_key]["cols"]
    for i, (cname, _, _) in enumerate(cols):
        if cname == col_name:
            row_y = y + h - HEAD_H - (i + 0.5) * ROW_H
            return row_y
    return y + h / 2


def draw_table(c, tbl_key):
    x, y, w, h = table_rect(tbl_key)
    title = TABLES[tbl_key]["title"]
    cols  = TABLES[tbl_key]["cols"]

    # Заголовок
    c.setFillColor(C_HEADER_BG)
    c.rect(x, y + h - HEAD_H, w, HEAD_H, stroke=0, fill=1)
    c.setFillColor(C_HEADER_TXT)
    c.setFont(font(True), FONT_B)
    c.drawCentredString(x + w / 2, y + h - HEAD_H + (HEAD_H - FONT_B) / 2, title)

    # Строки
    for i, (col_name, col_type, col_key) in enumerate(cols):
        row_y = y + h - HEAD_H - (i + 1) * ROW_H
        bg = C_PK_BG if col_key == "PK" else (C_FK_BG if "FK" in col_key else (C_ROW_ALT if i % 2 else C_ROW_BG))
        c.setFillColor(bg)
        c.rect(x, row_y, w, ROW_H, stroke=0, fill=1)

        # Метка PK/FK
        c.setFont(font(True), 6)
        if col_key == "PK":
            c.setFillColor(HexColor("#1A5276"))
            c.drawString(x + 2, row_y + 1.5, "PK")
        elif "FK" in col_key:
            c.setFillColor(HexColor("#1D6A39"))
            c.drawString(x + 2, row_y + 1.5, "FK")

        # Имя колонки
        c.setFillColor(black)
        c.setFont(font(True) if col_key == "PK" else font(), FONT_S)
        c.drawString(x + 10, row_y + ROW_H / 2 - FONT_S / 2 + 0.5, col_name)

        # Тип данных (правое выравнивание)
        c.setFont(font(), FONT_S - 0.5)
        c.setFillColor(HexColor("#555555"))
        c.drawRightString(x + w - 2, row_y + ROW_H / 2 - FONT_S / 2 + 0.5, col_type)

    # Внешняя рамка
    c.setStrokeColor(C_BORDER)
    c.setLineWidth(1.2)
    c.rect(x, y, w, h, stroke=1, fill=0)

    # Разделитель заголовка
    c.setLineWidth(0.5)
    for i in range(1, len(cols)):
        line_y = y + h - HEAD_H - i * ROW_H
        c.line(x, line_y, x + w, line_y)


def draw_relation(c, from_tbl, from_col, to_tbl, to_col):
    x1, y1, w1, h1 = table_rect(from_tbl)
    x2, y2, w2, h2 = table_rect(to_tbl)

    fy = col_y_center(from_tbl, from_col)
    ty = col_y_center(to_tbl,   to_col)

    # Определяем стороны соединения
    fx = x1 + w1 if x1 < x2 else x1
    tx = x2 + w2 if x2 < x1 else x2

    c.setStrokeColor(C_LINE_FK)
    c.setLineWidth(1.0)
    c.line(fx, fy, tx, ty)

    # Точка на конце (у PK-таблицы)
    c.setFillColor(C_LINE_FK)
    c.circle(tx, ty, 2.5, stroke=0, fill=1)
    # Перпендикуляр на конце FK (одинарная черта)
    c.setLineWidth(1.5)
    perp = 4
    if abs(fy - ty) < 5:
        c.line(tx, ty - perp, tx, ty + perp)
    else:
        mid_x = (fx + tx) / 2
        c.line(mid_x, ty - perp, mid_x, ty + perp)


def draw_title(c):
    bar_h = 12 * mm
    c.setFillColor(C_TITLE_BG)
    c.rect(0, PAGE_H - bar_h, PAGE_W, bar_h, stroke=0, fill=1)
    c.setFillColor(white)
    c.setFont(font(True), 14)
    c.drawCentredString(PAGE_W / 2, PAGE_H - bar_h + (bar_h - 14) / 2,
                        "ER-диаграмма БД «СтройМатериалы»  ·  PostgreSQL  ·  3НФ")

    # Легенда
    legend_x = PAGE_W - 75 * mm
    legend_y = PAGE_H - bar_h - 14 * mm
    for color, label in [
        (C_PK_BG,  "PK — первичный ключ"),
        (C_FK_BG,  "FK — внешний ключ"),
        (C_LINE_FK, "— связь (FK → PK)"),
    ]:
        c.setFillColor(color)
        c.rect(legend_x, legend_y, 8, 8, stroke=1, fill=1)
        c.setFillColor(black)
        c.setFont(font(), 8)
        c.drawString(legend_x + 11, legend_y + 1, label)
        legend_y -= 11


def generate():
    _register()
    c = Canvas(OUTPUT_PATH, pagesize=landscape(A3))

    draw_title(c)

    # Сначала связи (под таблицами)
    for from_tbl, from_col, to_tbl, to_col in RELATIONS:
        draw_relation(c, from_tbl, from_col, to_tbl, to_col)

    # Поверх — таблицы
    for tbl_key in TABLES:
        draw_table(c, tbl_key)

    c.save()
    print(f"ER-диаграмма сохранена: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate()
