-- ============================================================
--  СтройМатериалы — PostgreSQL DDL
--  Соответствие: 3 нормальная форма, ссылочная целостность
-- ============================================================

-- Роли пользователей
CREATE TABLE roles (
    role_id   SERIAL       PRIMARY KEY,
    role_name VARCHAR(50)  NOT NULL UNIQUE
);

-- Пользователи системы
CREATE TABLE users (
    user_id   SERIAL       PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    login     VARCHAR(100) NOT NULL UNIQUE,
    password  VARCHAR(100) NOT NULL,
    role_id   INTEGER      NOT NULL REFERENCES roles(role_id)
);

-- Категории товаров
CREATE TABLE categories (
    category_id   SERIAL      PRIMARY KEY,
    category_name VARCHAR(150) NOT NULL UNIQUE
);

-- Единицы измерения
CREATE TABLE units (
    unit_id   SERIAL      PRIMARY KEY,
    unit_name VARCHAR(20) NOT NULL UNIQUE
);

-- Поставщики
CREATE TABLE suppliers (
    supplier_id   SERIAL       PRIMARY KEY,
    supplier_name VARCHAR(150) NOT NULL UNIQUE
);

-- Производители
CREATE TABLE manufacturers (
    manufacturer_id   SERIAL       PRIMARY KEY,
    manufacturer_name VARCHAR(150) NOT NULL UNIQUE
);

-- Товары
CREATE TABLE products (
    product_id       SERIAL          PRIMARY KEY,
    article          VARCHAR(20)     NOT NULL UNIQUE,
    product_name     VARCHAR(250)    NOT NULL,
    unit_id          INTEGER         NOT NULL REFERENCES units(unit_id),
    price            NUMERIC(12, 2)  NOT NULL CHECK (price >= 0),
    supplier_id      INTEGER         NOT NULL REFERENCES suppliers(supplier_id),
    manufacturer_id  INTEGER         NOT NULL REFERENCES manufacturers(manufacturer_id),
    category_id      INTEGER         NOT NULL REFERENCES categories(category_id),
    discount         NUMERIC(5, 2)   NOT NULL DEFAULT 0 CHECK (discount >= 0 AND discount <= 100),
    quantity_stock   INTEGER         NOT NULL DEFAULT 0 CHECK (quantity_stock >= 0),
    description      TEXT,
    image_path       VARCHAR(255)
);

-- Пункты выдачи
CREATE TABLE pickup_points (
    pickup_point_id SERIAL       PRIMARY KEY,
    address         VARCHAR(300) NOT NULL UNIQUE
);

-- Статусы заказов
CREATE TABLE order_statuses (
    status_id   SERIAL      PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL UNIQUE
);

-- Заказы
CREATE TABLE orders (
    order_id        SERIAL          PRIMARY KEY,
    user_id         INTEGER         NOT NULL REFERENCES users(user_id),
    order_date      TIMESTAMP       NOT NULL DEFAULT NOW(),
    pickup_point_id INTEGER         REFERENCES pickup_points(pickup_point_id),
    status_id       INTEGER         NOT NULL REFERENCES order_statuses(status_id),
    total_amount    NUMERIC(14, 2)  NOT NULL DEFAULT 0 CHECK (total_amount >= 0)
);

-- Позиции заказа
CREATE TABLE order_items (
    item_id    SERIAL         PRIMARY KEY,
    order_id   INTEGER        NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INTEGER        NOT NULL REFERENCES products(product_id),
    quantity   INTEGER        NOT NULL CHECK (quantity > 0),
    price      NUMERIC(12, 2) NOT NULL CHECK (price >= 0)
);

-- ============================================================
--  Индексы для ускорения поиска
-- ============================================================
CREATE INDEX idx_products_category   ON products(category_id);
CREATE INDEX idx_products_supplier   ON products(supplier_id);
CREATE INDEX idx_products_article    ON products(article);
CREATE INDEX idx_orders_user         ON orders(user_id);
CREATE INDEX idx_order_items_order   ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
CREATE INDEX idx_users_login         ON users(login);

-- ============================================================
--  Базовые справочники
-- ============================================================
INSERT INTO roles (role_name) VALUES
    ('Администратор'),
    ('Менеджер'),
    ('Авторизированный клиент'),
    ('Гость');

INSERT INTO order_statuses (status_name) VALUES
    ('Новый'),
    ('В обработке'),
    ('Передан в доставку'),
    ('Готов к выдаче'),
    ('Выполнен'),
    ('Отменён');
