import sqlite3
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "shop.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS roles (
            id   INTEGER PRIMARY KEY,
            name TEXT    NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS users (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            login     TEXT    NOT NULL UNIQUE,
            password  TEXT    NOT NULL,
            full_name TEXT    NOT NULL,
            role_id   INTEGER NOT NULL,
            FOREIGN KEY (role_id) REFERENCES roles(id)
        );

        CREATE TABLE IF NOT EXISTS categories (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT    NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS products (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT    NOT NULL,
            category_id  INTEGER,
            description  TEXT,
            manufacturer TEXT,
            supplier     TEXT,
            price        REAL    NOT NULL,
            unit         TEXT,
            quantity     INTEGER DEFAULT 0,
            discount     REAL    DEFAULT 0,
            image_path   TEXT,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        );
    """)

    cursor.executemany(
        "INSERT OR IGNORE INTO roles (id, name) VALUES (?, ?)",
        [(1, "admin"), (2, "manager"), (3, "client"), (4, "guest")],
    )

    default_users = [
        ("admin",   hash_password("admin123"),   "Администратов Иван Сергеевич",    1),
        ("manager", hash_password("manager123"), "Менеджеров Пётр Николаевич",      2),
        ("client",  hash_password("client123"),  "Клиентов Алексей Владимирович",   3),
    ]
    for login, pwd, full_name, role_id in default_users:
        cursor.execute(
            "INSERT OR IGNORE INTO users (login, password, full_name, role_id) VALUES (?, ?, ?, ?)",
            (login, pwd, full_name, role_id),
        )

    categories = [
        "Электроника",
        "Одежда",
        "Продукты питания",
        "Бытовая химия",
        "Книги",
    ]
    for cat in categories:
        cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (cat,))

    cursor.execute("SELECT id FROM categories WHERE name='Электроника'")
    cat_electronics = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM categories WHERE name='Одежда'")
    cat_clothes = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM categories WHERE name='Продукты питания'")
    cat_food = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM categories WHERE name='Бытовая химия'")
    cat_chem = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM categories WHERE name='Книги'")
    cat_books = cursor.fetchone()[0]

    sample_products = [
        ("Ноутбук ASUS VivoBook",   cat_electronics, "15.6\", Intel Core i5, 8GB RAM, 512GB SSD", "ASUS",        "ТехноСнаб",    65000.0, "шт",  12,  15, None),
        ("Смартфон Samsung Galaxy", cat_electronics, "6.5\", 128GB, Android 14",                   "Samsung",     "МобайлСнаб",   49900.0, "шт",   0,   5, None),
        ("Наушники Sony WH-1000",   cat_electronics, "Беспроводные, шумоподавление",               "Sony",        "ТехноСнаб",     9500.0, "шт",  20,  25, None),
        ("Планшет iPad Air",        cat_electronics, "10.9\", M1, 256GB, Wi-Fi",                   "Apple",       "МобайлСнаб",   72000.0, "шт",   5,   0, None),
        ("Клавиатура Logitech",     cat_electronics, "Беспроводная, подсветка",                    "Logitech",    "ОфисСнаб",      3200.0, "шт",  35,  10, None),
        ("Футболка базовая",        cat_clothes,     "100% хлопок, размеры S-XXL",                 "Calvin Klein","МодаСнаб",      1500.0, "шт", 100,   0, None),
        ("Джинсы классические",     cat_clothes,     "Прямой крой, синие",                         "Levi's",      "МодаСнаб",      4500.0, "шт",  45,  13, None),
        ("Куртка зимняя",           cat_clothes,     "Пуховик, температура до -30°C",              "Columbia",    "МодаСнаб",     12000.0, "шт",   0,   0, None),
        ("Молоко 3.2% 1л",          cat_food,        "Пастеризованное, ГОСТ",                      "Простоквашино","ПродСнаб",       89.0,  "л",  200,  20, None),
        ("Хлеб белый",              cat_food,        "Нарезной, 500г",                             "Хлебозавод №1","ПродСнаб",       52.0,  "шт", 150,   0, None),
        ("Кофе Jacobs 250г",        cat_food,        "Молотый, средняя обжарка",                   "Jacobs",      "КофеСнаб",      450.0,  "шт",  60,  15, None),
        ("Порошок Tide 3кг",        cat_chem,        "Для белого белья, автомат",                  "Tide",        "ХимСнаб",       680.0,  "шт",   0,   0, None),
        ("Шампунь Head&Shoulders",  cat_chem,        "Против перхоти, 400мл",                      "P&G",         "ХимСнаб",       320.0,  "шт",  80,   5, None),
        ("Книга «Python для всех»", cat_books,       "Введение в программирование",                "Чарльз Северанс","КнигаСнаб", 1100.0,  "шт",  25,   0, None),
        ("Книга «Чистый код»",      cat_books,       "Создание, анализ и рефакторинг",             "Роберт Мартин","КнигаСнаб",   1350.0,  "шт",  18,  30, None),
    ]

    for prod in sample_products:
        cursor.execute(
            """INSERT OR IGNORE INTO products
               (name, category_id, description, manufacturer, supplier,
                price, unit, quantity, discount, image_path)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            prod,
        )

    conn.commit()
    conn.close()


def authenticate_user(login, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT u.id, u.full_name, r.name
           FROM users u
           JOIN roles r ON u.role_id = r.id
           WHERE u.login = ? AND u.password = ?""",
        (login, hash_password(password)),
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "full_name": row[1], "role": row[2]}
    return None


def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT p.id, p.name, c.name, p.description, p.manufacturer,
                  p.supplier, p.price, p.unit, p.quantity, p.discount, p.image_path
           FROM products p
           LEFT JOIN categories c ON p.category_id = c.id
           ORDER BY p.id""",
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT u.id, u.login, u.full_name, r.name
           FROM users u
           JOIN roles r ON u.role_id = r.id
           ORDER BY u.id""",
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_product(name, category_id, description, manufacturer, supplier,
                price, unit, quantity, discount, image_path=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO products
           (name, category_id, description, manufacturer, supplier,
            price, unit, quantity, discount, image_path)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (name, category_id, description, manufacturer, supplier,
         price, unit, quantity, discount, image_path),
    )
    conn.commit()
    conn.close()


def update_product(product_id, name, category_id, description, manufacturer,
                   supplier, price, unit, quantity, discount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE products
           SET name=?, category_id=?, description=?, manufacturer=?,
               supplier=?, price=?, unit=?, quantity=?, discount=?
           WHERE id=?""",
        (name, category_id, description, manufacturer, supplier,
         price, unit, quantity, discount, product_id),
    )
    conn.commit()
    conn.close()


def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()


def get_categories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories ORDER BY name")
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_user(login, password, full_name, role_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (login, password, full_name, role_id) VALUES (?, ?, ?, ?)",
        (login, hash_password(password), full_name, role_id),
    )
    conn.commit()
    conn.close()


def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()


def get_roles():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM roles ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return rows
