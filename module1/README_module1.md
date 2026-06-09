# Модуль 1 — База данных «СтройМатериалы» (PostgreSQL)

> Этот модуль полностью независим от остальных модулей репозитория.

---

## Состав модуля

| Файл | Описание |
|------|----------|
| `db_schema.sql` | DDL-скрипт создания БД (3НФ, PK/FK, индексы) |
| `import_data.py` | Импорт данных из Excel-файлов в PostgreSQL |
| `generate_er_diagram.py` | Генерация ER-диаграммы в PDF |
| `er_diagram.pdf` | Готовая ER-диаграмма (таблицы, связи, атрибуты, ключи) |
| `import/` | Файлы данных для импорта (xlsx + фото товаров) |

---

## Схема базы данных (3НФ)

```
roles              ← users
units              ← products
suppliers          ← products
manufacturers      ← products
categories         ← products
products           ← order_items
users              ← orders
pickup_points      ← orders
order_statuses     ← orders
orders             ← order_items
```

### Таблицы

| Таблица | Назначение |
|---------|------------|
| `roles` | Роли пользователей (Администратор, Менеджер, Клиент, Гость) |
| `users` | Пользователи системы |
| `categories` | Категории товаров |
| `units` | Единицы измерения |
| `suppliers` | Поставщики |
| `manufacturers` | Производители |
| `products` | Товары (артикул, цена, скидка, остаток и др.) |
| `pickup_points` | Пункты выдачи заказов |
| `order_statuses` | Статусы заказов |
| `orders` | Заказы |
| `order_items` | Позиции заказа |

---

## Установка и запуск

### 1. Требования

- PostgreSQL 13+
- Python 3.8+
- Пакеты: `psycopg2-binary`, `openpyxl`

```bash
pip install psycopg2-binary openpyxl
```

### 2. Создание базы данных

Подключитесь к PostgreSQL и создайте БД:

```sql
CREATE DATABASE stroy_materials
    ENCODING 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE   = 'Russian_Russia.1251'
    TEMPLATE template0;
```

Или через командную строку:

```bash
createdb -U postgres -E UTF8 stroy_materials
```

### 3. Применение DDL-скрипта

```bash
psql -U postgres -d stroy_materials -f db_schema.sql
```

Или через pgAdmin: открыть Query Tool → вставить содержимое `db_schema.sql` → выполнить.

### 4. Импорт данных

```bash
# Параметры по умолчанию: host=localhost, port=5432, db=stroy_materials, user=postgres, pass=postgres
python import_data.py

# Или с кастомными параметрами:
DB_HOST=localhost DB_PORT=5432 DB_NAME=stroy_materials DB_USER=postgres DB_PASSWORD=ваш_пароль python import_data.py
```

На Windows (PowerShell):
```powershell
$env:DB_PASSWORD="ваш_пароль"; python import_data.py
```

После импорта в БД будут:
- **11 таблиц** с ключами и индексами
- **30 товаров** (из Tovar.xlsx)
- **10 пользователей** (из user_import.xlsx)
- **Пункты выдачи** и **тестовые заказы**

### 5. Генерация ER-диаграммы

```bash
python generate_er_diagram.py
```

Файл `er_diagram.pdf` будет создан в папке `module1/`.

---

## Подключение через pgAdmin

1. Открыть pgAdmin → Servers → Create → Server
2. **General**: Name = `СтройМатериалы`
3. **Connection**:
   - Host: `localhost`
   - Port: `5432`
   - Database: `stroy_materials`
   - Username: `postgres`
   - Password: ваш пароль
4. Save → Connect

---

## Тестовые данные (после импорта)

**Пользователи** (пароли хешированы SHA-256):

| Логин | Пароль | Роль |
|-------|--------|------|
| 94d5ous@gmail.com | uzWC67 | Администратор |
| uth4iz@mail.com | 2L6KZG | Администратор |
| 1diph5e@tutanota.com | 8ntwUp | Менеджер |
| 5d4zbu@tutanota.com | rwVDh9 | Авторизированный клиент |

**Категории товаров:**
- Общестроительные материалы
- Стеновые и фасадные материалы
- Сухие строительные смеси и гидроизоляция
- Ручной инструмент
- Защита лица, глаз, головы
