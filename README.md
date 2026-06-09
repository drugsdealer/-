# Система управления магазином

Десктопное приложение на Python + PyQt5 с базой данных SQLite.  
Реализует авторизацию по ролям, список товаров с подсветкой и управление данными.

---

## Содержание

1. [Требования](#требования)
2. [Быстрый старт](#быстрый-старт)
3. [Пошаговая установка](#пошаговая-установка)
4. [Структура проекта](#структура-проекта)
5. [Запуск приложения](#запуск-приложения)
6. [Тестовые аккаунты](#тестовые-аккаунты)
7. [Функционал по ролям](#функционал-по-ролям)
8. [Генерация блок-схемы PDF](#генерация-блок-схемы-pdf)
9. [Создание документа со скриншотами](#создание-документа-со-скриншотами)
10. [Частые проблемы](#частые-проблемы)

---

## Требования

| Компонент | Версия |
|-----------|--------|
| Python    | 3.8 — 3.12 |
| pip       | любая актуальная |
| ОС        | Windows 10/11, macOS 12+, Ubuntu 20.04+ |

---

## Быстрый старт

```bash
# 1. Клонировать репозиторий
git clone <URL_репозитория>
cd <папка_проекта>

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Сгенерировать ресурсы (логотип, иконка, заглушка)
python resources/generate_resources.py

# 4. Запустить приложение
python main.py
```

---

## Пошаговая установка

### Windows

1. Скачайте Python 3.10+ с [python.org](https://www.python.org/downloads/)  
   При установке поставьте галочку **"Add Python to PATH"**

2. Откройте **Командную строку** (Win+R → `cmd`) или **PowerShell**

3. Перейдите в папку проекта:
   ```cmd
   cd C:\путь\до\проекта
   ```

4. Создайте виртуальное окружение (рекомендуется):
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

5. Установите зависимости:
   ```cmd
   pip install -r requirements.txt
   ```

6. Сгенерируйте ресурсы:
   ```cmd
   python resources\generate_resources.py
   ```

7. Запустите приложение:
   ```cmd
   python main.py
   ```

---

### macOS

1. Убедитесь что установлен Python 3.8+:
   ```bash
   python3 --version
   ```
   Если нет — установите через [Homebrew](https://brew.sh/):
   ```bash
   brew install python@3.11
   ```

2. Перейдите в папку проекта:
   ```bash
   cd /путь/до/проекта
   ```

3. Создайте виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

5. Сгенерируйте ресурсы:
   ```bash
   python resources/generate_resources.py
   ```

6. Запустите:
   ```bash
   python main.py
   ```

> **macOS и PyQt5:** если приложение не запускается с ошибкой `NSWindow`, попробуйте:
> ```bash
> OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES python main.py
> ```

---

### Linux (Ubuntu/Debian)

1. Установите системные зависимости:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv python3-dev \
       libxcb-xinerama0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
       libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxcb-xfixes0 \
       libgl1-mesa-glx fonts-dejavu -y
   ```

2. Перейдите в папку проекта и создайте venv:
   ```bash
   cd /путь/до/проекта
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Сгенерируйте ресурсы:
   ```bash
   python resources/generate_resources.py
   ```

5. Запустите:
   ```bash
   python main.py
   ```

---

## Структура проекта

```
.
├── main.py                        # Точка входа
├── requirements.txt               # Зависимости
├── flowchart_gost.pdf             # Блок-схема (ГОСТ 19.701-90)
│
├── database/
│   ├── __init__.py
│   ├── db_manager.py              # Все операции с БД
│   └── shop.db                    # SQLite-база (создаётся автоматически)
│
├── ui/
│   ├── __init__.py
│   ├── styles.py                  # Стили и цвета
│   ├── login_window.py            # Окно авторизации
│   ├── main_window.py             # Главное окно (с шапкой и вкладками)
│   ├── products_widget.py         # Виджет списка товаров
│   ├── client_tab.py              # Вкладка «Мой профиль» (клиент)
│   ├── manager_tab.py             # Вкладка управления товарами (менеджер/админ)
│   └── admin_tab.py               # Вкладка управления пользователями (админ)
│
├── flowchart/
│   └── generate_pdf.py            # Генератор блок-схемы PDF
│
└── resources/
    ├── generate_resources.py      # Скрипт генерации ресурсов
    ├── logo.png                   # Логотип компании
    ├── icon.png                   # Иконка приложения
    └── picture.png                # Заглушка для товаров без фото
```

---

## Запуск приложения

```bash
python main.py
```

При первом запуске автоматически:
- Создаётся база данных `database/shop.db`
- Заполняются тестовые данные (15 товаров, 3 пользователя, 5 категорий)

---

## Тестовые аккаунты

| Логин     | Пароль       | Роль            |
|-----------|--------------|-----------------|
| `admin`   | `admin123`   | Администратор   |
| `manager` | `manager123` | Менеджер        |
| `client`  | `client123`  | Клиент          |
| —         | —            | Гость (кнопка «Продолжить как гость») |

---

## Функционал по ролям

### Гость
- Просмотр списка товаров (только чтение)
- Поиск и фильтрация по категории
- Нет доступа к управлению

### Клиент
- Всё, что доступно гостю
- Вкладка «Мой профиль» — просмотр своих данных

### Менеджер
- Всё, что доступно гостю
- Вкладка «Управление товарами»:
  - Добавление нового товара
  - Редактирование товара
  - Удаление товара

### Администратор
- Всё, что доступно менеджеру
- Вкладка «Управление пользователями»:
  - Добавление пользователя с выбором роли
  - Удаление пользователя

### Общее для всех (после входа)
- ФИО пользователя и роль отображаются в правом верхнем углу
- Кнопка «Выйти» возвращает на экран авторизации

---

## Подсветка строк в списке товаров

| Условие | Цвет фона |
|---------|-----------|
| Скидка > 12% | `#F4A460` (Sandy Brown) |
| Товара нет на складе (кол-во = 0) | `#ADD8E6` (Light Blue) |
| Есть скидка (любая) | Цена перечёркнута красным + итоговая цена чёрным |

---

## Генерация блок-схемы PDF

Блок-схема уже сгенерирована и находится в файле `flowchart_gost.pdf`.

Для повторной генерации:

```bash
python flowchart/generate_pdf.py
```

Для корректного отображения кириллицы в PDF установите шрифт DejaVu:

**Windows:** скачайте [DejaVu Fonts](https://dejavu-fonts.github.io/) и поместите  
`DejaVuSans.ttf` и `DejaVuSans-Bold.ttf` в папку `flowchart/`

**Linux:**
```bash
sudo apt install fonts-dejavu
cp /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf flowchart/
cp /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf flowchart/
```

---

## Создание документа со скриншотами

Сделайте скриншоты следующих экранов:

1. **Окно авторизации** — запустите `python main.py`
2. **Список товаров (гость)** — нажмите «Продолжить как гость»
3. **Список товаров (клиент)** — войдите как `client/client123`
4. **Список товаров (менеджер)** — войдите как `manager/manager123`
5. **Управление товарами** — вкладка «Управление товарами»
6. **Добавление товара** — нажмите «Добавить товар»
7. **Список товаров (администратор)** — войдите как `admin/admin123`
8. **Управление пользователями** — вкладка «Управление пользователями»

Вставьте скриншоты в документ Word/LibreOffice Writer.

---

## Частые проблемы

### `ModuleNotFoundError: No module named 'PyQt5'`
```bash
pip install PyQt5==5.15.10
```

### `could not load the Qt platform plugin "xcb"` (Linux)
```bash
sudo apt install libxcb-xinerama0 libxcb-icccm4 libxcb-image0 \
    libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 \
    libxcb-shape0 libxcb-xfixes0
```

### `ModuleNotFoundError: No module named 'reportlab'`
```bash
pip install reportlab==4.2.0
```

### `ModuleNotFoundError: No module named 'PIL'`
```bash
pip install Pillow==10.3.0
```

### Приложение не видит базу данных
Убедитесь, что запускаете `python main.py` из корневой папки проекта, а не из подпапки.

### Блок-схема содержит квадраты вместо кириллицы
Скопируйте файлы шрифтов DejaVu в папку `flowchart/` (см. [выше](#генерация-блок-схемы-pdf)).

---

## Стек технологий

| Технология | Назначение |
|------------|------------|
| Python 3.8+ | Основной язык |
| PyQt5 | GUI-фреймворк |
| SQLite3 | База данных (встроена в Python) |
| Pillow | Генерация ресурсов (логотип, иконка) |
| ReportLab | Генерация PDF блок-схемы |
| python-docx | Создание DOCX документов |

---

## Соглашение об именовании

Код написан в стиле **snake_case** (Python PEP 8):
- Переменные и функции: `get_all_products`, `init_database`
- Классы: `LoginWindow`, `ProductsWidget`, `ManagerTab`
- Константы: `DISCOUNT_HIGH_BG`, `OUT_OF_STOCK_BG`
- Не более одной команды в строке
