"""
Генерация блок-схемы алгоритма работы приложения
в соответствии с ГОСТ 19.701-90.
"""
import os
import math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import (
    HexColor, black, white, lightgrey,
)

OUTPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "flowchart_gost.pdf")

PAGE_W, PAGE_H = A4
MARGIN = 15 * mm

BLK_W  = 60 * mm
BLK_H  = 16 * mm
DIA_W  = 70 * mm
DIA_H  = 20 * mm
TERM_W = 55 * mm
TERM_H = 14 * mm
ARROW  = 5 * mm
GAP    = 10 * mm

COLOR_FILL_TERM    = HexColor("#D6EAF8")
COLOR_FILL_PROC    = HexColor("#FDFEFE")
COLOR_FILL_IO      = HexColor("#E8F8F5")
COLOR_FILL_DEC     = HexColor("#FEF9E7")
COLOR_FILL_CONN    = HexColor("#F9EBEA")
COLOR_BORDER       = HexColor("#2C3E50")
COLOR_ARROW        = HexColor("#2C3E50")
COLOR_TEXT         = HexColor("#1A1A2E")
COLOR_TITLE_BG     = HexColor("#2C3E50")


def _register_fonts():
    base = os.path.dirname(__file__)
    for name, fname in [
        ("DejaVuSans",       "DejaVuSans.ttf"),
        ("DejaVuSans-Bold",  "DejaVuSans-Bold.ttf"),
    ]:
        path = os.path.join(base, fname)
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(name, path))


def _font(bold=False):
    fonts = pdfmetrics.getRegisteredFontNames()
    if bold and "DejaVuSans-Bold" in fonts:
        return "DejaVuSans-Bold"
    if not bold and "DejaVuSans" in fonts:
        return "DejaVuSans"
    return "Helvetica-Bold" if bold else "Helvetica"


def draw_terminator(c: Canvas, cx, cy, w, h, text):
    r = h / 2
    x = cx - w / 2
    y = cy - h / 2
    c.setFillColor(COLOR_FILL_TERM)
    c.setStrokeColor(COLOR_BORDER)
    c.setLineWidth(1.2)
    c.roundRect(x, y, w, h, r, stroke=1, fill=1)
    c.setFillColor(COLOR_TEXT)
    c.setFont(_font(True), 9)
    c.drawCentredString(cx, cy - 3, text)


def draw_process(c: Canvas, cx, cy, w, h, text):
    x = cx - w / 2
    y = cy - h / 2
    c.setFillColor(COLOR_FILL_PROC)
    c.setStrokeColor(COLOR_BORDER)
    c.setLineWidth(1.2)
    c.rect(x, y, w, h, stroke=1, fill=1)
    c.setFillColor(COLOR_TEXT)
    c.setFont(_font(), 8)
    _draw_wrapped_text(c, cx, cy, w - 6, text)


def draw_io(c: Canvas, cx, cy, w, h, text):
    skew = 6 * mm
    x = cx - w / 2
    y = cy - h / 2
    path = c.beginPath()
    path.moveTo(x + skew,   y + h)
    path.lineTo(x + w,      y + h)
    path.lineTo(x + w - skew, y)
    path.lineTo(x,           y)
    path.close()
    c.setFillColor(COLOR_FILL_IO)
    c.setStrokeColor(COLOR_BORDER)
    c.setLineWidth(1.2)
    c.drawPath(path, stroke=1, fill=1)
    c.setFillColor(COLOR_TEXT)
    c.setFont(_font(), 8)
    _draw_wrapped_text(c, cx, cy, w - 10, text)


def draw_decision(c: Canvas, cx, cy, w, h, text, yes_label=None, no_label=None):
    path = c.beginPath()
    path.moveTo(cx,          cy + h / 2)
    path.lineTo(cx + w / 2,  cy)
    path.lineTo(cx,          cy - h / 2)
    path.lineTo(cx - w / 2,  cy)
    path.close()
    c.setFillColor(COLOR_FILL_DEC)
    c.setStrokeColor(COLOR_BORDER)
    c.setLineWidth(1.2)
    c.drawPath(path, stroke=1, fill=1)
    c.setFillColor(COLOR_TEXT)
    c.setFont(_font(), 8)
    _draw_wrapped_text(c, cx, cy, w - 14, text)
    if yes_label:
        c.setFont(_font(True), 7)
        c.drawString(cx - w / 2 - 12 * mm, cy - 2, yes_label)
    if no_label:
        c.setFont(_font(True), 7)
        c.drawCentredString(cx, cy - h / 2 - 4, no_label)


def draw_connector(c: Canvas, cx, cy, r, text=""):
    c.setFillColor(COLOR_FILL_CONN)
    c.setStrokeColor(COLOR_BORDER)
    c.setLineWidth(1.0)
    c.circle(cx, cy, r, stroke=1, fill=1)
    if text:
        c.setFillColor(COLOR_TEXT)
        c.setFont(_font(True), 8)
        c.drawCentredString(cx, cy - 3, text)


def draw_arrow_down(c: Canvas, x, y_top, y_bot):
    c.setStrokeColor(COLOR_ARROW)
    c.setLineWidth(1.2)
    c.line(x, y_top, x, y_bot + ARROW)
    _draw_arrowhead(c, x, y_bot)


def draw_arrow_right(c: Canvas, x_left, x_right, y):
    c.setStrokeColor(COLOR_ARROW)
    c.setLineWidth(1.2)
    c.line(x_left, y, x_right - ARROW, y)
    _arrowhead_right(c, x_right, y)


def draw_line(c: Canvas, x1, y1, x2, y2):
    c.setStrokeColor(COLOR_ARROW)
    c.setLineWidth(1.2)
    c.line(x1, y1, x2, y2)


def _draw_arrowhead(c: Canvas, x, y_tip):
    s = 2.5 * mm
    path = c.beginPath()
    path.moveTo(x,       y_tip)
    path.lineTo(x - s,   y_tip + s * 1.7)
    path.lineTo(x + s,   y_tip + s * 1.7)
    path.close()
    c.setFillColor(COLOR_ARROW)
    c.drawPath(path, stroke=0, fill=1)


def _arrowhead_right(c: Canvas, x_tip, y):
    s = 2.5 * mm
    path = c.beginPath()
    path.moveTo(x_tip,         y)
    path.lineTo(x_tip - s * 1.7, y + s)
    path.lineTo(x_tip - s * 1.7, y - s)
    path.close()
    c.setFillColor(COLOR_ARROW)
    c.drawPath(path, stroke=0, fill=1)


def _draw_wrapped_text(c: Canvas, cx, cy, max_w, text):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if c.stringWidth(test, _font(), 8) <= max_w:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    line_h = 10
    total_h = len(lines) * line_h
    start_y = cy + total_h / 2 - line_h
    for i, line in enumerate(lines):
        c.drawCentredString(cx, start_y - i * line_h, line)


def draw_title_block(c: Canvas):
    title_h = 18 * mm
    c.setFillColor(COLOR_TITLE_BG)
    c.rect(MARGIN, PAGE_H - MARGIN - title_h, PAGE_W - 2 * MARGIN, title_h, stroke=0, fill=1)
    c.setFillColor(white)
    c.setFont(_font(True), 13)
    c.drawCentredString(
        PAGE_W / 2,
        PAGE_H - MARGIN - title_h / 2 - 4,
        "Алгоритм работы системы управления магазином",
    )
    c.setFont(_font(), 9)
    c.drawCentredString(
        PAGE_W / 2,
        PAGE_H - MARGIN - title_h / 2 - 14,
        "ГОСТ 19.701-90",
    )


def draw_stamp(c: Canvas):
    stamp_h = 20 * mm
    stamp_y = MARGIN
    c.setStrokeColor(COLOR_BORDER)
    c.setLineWidth(0.8)
    c.rect(MARGIN, stamp_y, PAGE_W - 2 * MARGIN, stamp_h, stroke=1, fill=0)
    cols = [40 * mm, 50 * mm, 35 * mm, 25 * mm, 25 * mm]
    x = MARGIN
    for w in cols:
        x += w
        c.line(x, stamp_y, x, stamp_y + stamp_h)
    c.setFillColor(COLOR_TEXT)
    c.setFont(_font(), 7)
    headers = ["Разраб.", "Проверил", "Н.контр.", "Утв.", "Лист"]
    x = MARGIN
    for i, (hdr, w) in enumerate(zip(headers, cols)):
        c.drawCentredString(x + w / 2, stamp_y + stamp_h - 8, hdr)
        x += w
    c.drawCentredString(MARGIN + sum(cols) + 10 * mm, stamp_y + stamp_h - 8, "1/1")


def generate_flowchart():
    _register_fonts()
    c = Canvas(OUTPUT_PATH, pagesize=A4)

    draw_title_block(c)
    draw_stamp(c)

    cx = PAGE_W / 2
    title_bottom = PAGE_H - MARGIN - 18 * mm
    stamp_top = MARGIN + 20 * mm

    usable_h = title_bottom - stamp_top
    start_y  = title_bottom - 10 * mm

    def step(y):
        return y - BLK_H / 2 - GAP - BLK_H / 2

    y = start_y

    draw_terminator(c, cx, y, TERM_W, TERM_H, "НАЧАЛО")
    y_prev_bot = y - TERM_H / 2

    y -= TERM_H / 2 + GAP + BLK_H / 2
    draw_arrow_down(c, cx, y_prev_bot, y + BLK_H / 2)
    draw_process(c, cx, y, BLK_W, BLK_H, "Запуск приложения")
    y_prev_bot = y - BLK_H / 2

    y -= BLK_H / 2 + GAP + BLK_H / 2
    draw_arrow_down(c, cx, y_prev_bot, y + BLK_H / 2)
    draw_process(c, cx, y, BLK_W, BLK_H, "Инициализация базы данных")
    y_prev_bot = y - BLK_H / 2

    y -= BLK_H / 2 + GAP + TERM_H / 2
    draw_arrow_down(c, cx, y_prev_bot, y + TERM_H / 2)
    draw_process(c, cx, y, BLK_W, TERM_H, "Отображение окна авторизации")
    y_prev_bot = y - TERM_H / 2

    y -= TERM_H / 2 + GAP + BLK_H / 2
    draw_arrow_down(c, cx, y_prev_bot, y + BLK_H / 2)
    draw_io(c, cx, y, BLK_W, BLK_H, "Ввод логина и пароля")
    y_prev_bot = y - BLK_H / 2

    y -= BLK_H / 2 + GAP + DIA_H / 2
    draw_arrow_down(c, cx, y_prev_bot, y + DIA_H / 2)
    dec_y = y
    draw_decision(c, cx, y, DIA_W, DIA_H, "Вход как гость?", yes_label="Да", no_label="Нет")
    y_prev_bot = y - DIA_H / 2

    guest_x = cx - DIA_W / 2 - BLK_W / 2 - GAP
    guest_dec_y = dec_y
    draw_line(c, cx - DIA_W / 2, dec_y, guest_x + BLK_W / 2, dec_y)
    draw_process(c, guest_x, guest_dec_y, BLK_W, BLK_H, "Роль: Гость")
    guest_bot = guest_dec_y - BLK_H / 2

    y -= DIA_H / 2 + GAP + DIA_H / 2
    draw_arrow_down(c, cx, y_prev_bot, y + DIA_H / 2)
    dec2_y = y
    draw_decision(c, cx, y, DIA_W, DIA_H, "Данные верны?", yes_label="Нет", no_label="Да")
    y_prev_bot = y - DIA_H / 2

    err_x = cx + DIA_W / 2 + BLK_W / 2 + GAP
    draw_line(c, cx + DIA_W / 2, dec2_y, err_x - BLK_W / 2, dec2_y)
    draw_process(c, err_x, dec2_y, BLK_W, BLK_H, "Сообщение об ошибке")

    y -= DIA_H / 2 + GAP + DIA_H / 2
    draw_arrow_down(c, cx, y_prev_bot, y + DIA_H / 2)
    dec3_y = y
    draw_decision(c, cx, y, DIA_W, DIA_H, "Определение роли", yes_label="", no_label="")
    y_prev_bot = y - DIA_H / 2

    roles = ["Клиент", "Менеджер", "Администратор"]
    role_xs = [cx - DIA_W * 0.9, cx, cx + DIA_W * 0.9]
    draw_line(c, cx - DIA_W / 2, dec3_y, cx - DIA_W * 0.9, dec3_y)

    merge_y = y_prev_bot - GAP - BLK_H / 2
    for rx in role_xs:
        draw_process(c, rx, merge_y + GAP + BLK_H / 2 - GAP * 2, BLK_W * 0.7, BLK_H, roles[role_xs.index(rx)] if rx in role_xs else "")

    y = merge_y - 2 * GAP
    draw_arrow_down(c, cx, y_prev_bot, y + BLK_H / 2)
    draw_process(c, cx, y, BLK_W, BLK_H, "Открытие главного окна")
    y_prev_bot = y - BLK_H / 2

    y -= BLK_H / 2 + GAP + BLK_H / 2
    draw_arrow_down(c, cx, y_prev_bot, y + BLK_H / 2)
    draw_process(c, cx, y, BLK_W, BLK_H, "Отображение списка товаров")
    y_prev_bot = y - BLK_H / 2

    y -= BLK_H / 2 + GAP + DIA_H / 2
    draw_arrow_down(c, cx, y_prev_bot, y + DIA_H / 2)
    dec4_y = y
    draw_decision(c, cx, y, DIA_W, DIA_H, "Выйти из системы?", yes_label="Нет", no_label="Да")
    y_prev_bot = y - DIA_H / 2

    y -= DIA_H / 2 + GAP + TERM_H / 2
    draw_arrow_down(c, cx, y_prev_bot, y + TERM_H / 2)
    draw_terminator(c, cx, y, TERM_W, TERM_H, "КОНЕЦ")

    c.save()
    print(f"Блок-схема сохранена: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_flowchart()
