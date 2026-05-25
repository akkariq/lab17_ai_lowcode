<div align="center">

# Технологии Программирования · Лабораторная работа №17 (Часть 2)
## 📊 Low-code CRM-система на Streamlit
### Python · Streamlit · SQLite · Реляционная модель · CRUD · Lookup · Rollup

<br/>

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-FK%20%2B%20CASCADE-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-DataFrames-150458?style=for-the-badge&logo=pandas&logoColor=white)
![CRUD](https://img.shields.io/badge/CRUD-Full%20Implementation-28A745?style=for-the-badge)

</div>

---

# Технологии Программирования · Паспорт работы

**Дисциплина:** Технологии Программирования  
**Руководитель:** Щеголев Алексей Алексеевич  
**Студент:** Иванников Сергей Сергеевич  
**Семестр:** 2 курс, 4 семестр  
**Тема лабораторной работы:** Знакомство с инструментами AI и low-code: автоматизация разработки с GigaChat и создание CRM на Streamlit. Часть 2 — разработка low-code CRM-системы на Streamlit с реляционной СУБД SQLite.

---

# Оглавление

- [Паспорт работы](#технологии-программирования--паспорт-работы)
- [Цели и задачи](#технологии-программирования--цели-и-задачи-лабораторной-работы)
- [Стек технологий](#технологии-программирования--используемый-стек-технологий)
- [Реляционная архитектура БД](#технологии-программирования--реляционная-архитектура-базы-данных)
- [Структура проекта](#технологии-программирования--структура-проекта)
- [Ход выполнения](#технологии-программирования--ход-выполнения)
  - [1. Инициализация схемы SQLite](#1-инициализация-схемы-sqlite-с-контролем-foreign-keys)
  - [2. Аналитический дашборд](#2-аналитический-дашборд-rollup-через-sql)
  - [3. База клиентов](#3-панель-управления-базой-клиентов)
  - [4. Каталог товаров](#4-складской-каталог-товаров)
  - [5. Форма заказа — Lookup и валидация](#5-crud-форма-создания-заказа-lookup-и-валидация-остатков)
  - [6. Книга заказов](#6-книга-заказов)
- [Контрольные вопросы](#технологии-программирования--контрольные-вопросы)
- [Вывод](#технологии-программирования--вывод)

---

# Технологии Программирования · Цели и задачи лабораторной работы

**Цель лабораторной работы** заключается в построении полноценного локального CRUD веб-приложения на базе фреймворка Streamlit, выступающего независимой программной заменой облачным low-code платформам (Airtable), с жёстким контролем реляционных связей на уровне СУБД.

**В рамках выполнения лабораторной работы были поставлены следующие задачи:**

- Спроектировать нормализованную реляционную схему из 4 связанных таблиц с первичными и внешними ключами.
- Включить строгий контроль Foreign Keys в SQLite через `PRAGMA foreign_keys = ON` и настроить каскадное удаление.
- Реализовать концепции low-code платформ средствами чистого SQL: функцию **Rollup** через агрегирующие JOIN-запросы и функцию **Lookup** через динамическую подстановку актуальных цен.
- Построить многостраничный Streamlit-интерфейс с дашбордом аналитики, CRUD-формами для клиентов, товаров и заказов.
- Реализовать валидацию складских остатков в форме заказа со списанием товаров при успешной транзакции.

---

# Технологии Программирования · Используемый стек технологий

| Компонент | Технология | Назначение |
|---|---|---|
| Язык программирования | Python 3.12 | Основной язык реализации |
| UI-фреймворк | Streamlit | Построение веб-интерфейса без frontend-стека |
| Обработка данных | Pandas | Представление результатов SQL-запросов в виде DataFrame |
| СУБД | SQLite 3 | Реляционное хранилище; файл `crm_system.db` |
| Контроль FK | `PRAGMA foreign_keys = ON` | Жёсткое соблюдение ссылочной целостности |
| Каскадное удаление | `ON DELETE CASCADE` | Автоматическое удаление заказов при удалении клиента |
| Среда разработки | VS Code, Windows 11 | IDE и операционная система |

---

# Технологии Программирования · Реляционная архитектура базы данных

БД спроектирована по принципу нормализации 3NF. Все четыре таблицы связаны через внешние ключи:

```text
customers (PK: customer_id)
    │
    │  ON DELETE CASCADE
    ▼
orders (PK: order_id, FK: customer_id → customers)
    │
    │  FK
    ▼
order_items (PK: item_id, FK: order_id → orders, FK: product_id → products)
    │
    ▲
products (PK: product_id)
```

### Схема таблиц

**`customers`** — база клиентов:

| Поле | Тип | Ограничения |
|---|---|---|
| customer_id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| fio | TEXT | NOT NULL |
| email | TEXT | UNIQUE, NOT NULL |
| phone | TEXT | — |
| city | TEXT | — |
| status | TEXT | DEFAULT 'Активный' |

**`products`** — каталог товаров:

| Поле | Тип | Ограничения |
|---|---|---|
| product_id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| name | TEXT | NOT NULL |
| category | TEXT | — |
| price | REAL | CHECK(price > 0) |
| stock | INTEGER | CHECK(stock >= 0) |

**`orders`** — книга заказов:

| Поле | Тип | Ограничения |
|---|---|---|
| order_id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| customer_id | INTEGER | FK → customers(customer_id) ON DELETE CASCADE |
| order_date | TEXT | NOT NULL |
| status | TEXT | DEFAULT 'Новый' |
| payment_method | TEXT | — |

**`order_items`** — позиции заказа:

| Поле | Тип | Ограничения |
|---|---|---|
| item_id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| order_id | INTEGER | FK → orders(order_id) |
| product_id | INTEGER | FK → products(product_id) |
| quantity | INTEGER | CHECK(quantity > 0) |
| price_at_order | REAL | Фиксируется на момент создания заказа (Lookup) |

---

# Технологии Программирования · Структура проекта

```text
lab7_streamlit/
├── app.py                  # Точка входа; навигация по страницам Streamlit
├── database.py             # Инициализация схемы; все SQL-запросы
├── crm_system.db           # Файл базы данных SQLite (генерируется при запуске)
├── requirements.txt        # streamlit, pandas
└── screenshots/
    ├── Снимок экрана 2026-05-25 194457.png   # Аналитический дашборд
    ├── Снимок экрана 2026-05-25 194510.png   # База клиентов
    ├── Снимок экрана 2026-05-25 194521.png   # Каталог товаров
    ├── Снимок экрана 2026-05-25 194531.png   # Форма заказа
    └── Снимок экрана 2026-05-25 194538.png   # Книга заказов
```

---

# Технологии Программирования · Ход выполнения

## 1. Инициализация схемы SQLite с контролем Foreign Keys

При запуске приложения модуль `database.py` создаёт файл `crm_system.db` и применяет DDL-скрипт. Первой командой включается строгий контроль ссылочной целостности:

```python
import sqlite3

DB_PATH = "crm_system.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")  # Обязательно при каждом подключении
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                fio           TEXT    NOT NULL,
                email         TEXT    UNIQUE NOT NULL,
                phone         TEXT,
                city          TEXT,
                status        TEXT    DEFAULT 'Активный'
            );
            CREATE TABLE IF NOT EXISTS products (
                product_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT    NOT NULL,
                category      TEXT,
                price         REAL    CHECK(price > 0),
                stock         INTEGER CHECK(stock >= 0)
            );
            CREATE TABLE IF NOT EXISTS orders (
                order_id      INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id   INTEGER NOT NULL,
                order_date    TEXT    NOT NULL,
                status        TEXT    DEFAULT 'Новый',
                payment_method TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                    ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS order_items (
                item_id         INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id        INTEGER NOT NULL,
                product_id      INTEGER NOT NULL,
                quantity        INTEGER CHECK(quantity > 0),
                price_at_order  REAL,
                FOREIGN KEY (order_id)   REFERENCES orders(order_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            );
        """)
```

> **Архитектурная деталь:** в SQLite режим `foreign_keys` необходимо включать при **каждом** новом подключении — он не сохраняется в файле базы данных. Поэтому `PRAGMA foreign_keys = ON` вынесен в функцию `get_connection()`.

---

## 2. Аналитический дашборд — Rollup через SQL

Дашборд реализует концепцию **Rollup** из low-code платформ: агрегирующие JOIN-запросы вычисляют ключевые метрики без ручных вычислений на уровне Python.

```python
# Rollup 1: общая выручка по всем доставленным заказам
def get_total_revenue(conn):
    row = conn.execute("""
        SELECT COALESCE(SUM(oi.quantity * oi.price_at_order), 0) AS revenue
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.status = 'Доставлен'
    """).fetchone()
    return row["revenue"]

# Rollup 2: сумма покупок каждого клиента
def get_customer_totals(conn):
    return conn.execute("""
        SELECT c.fio, c.city,
               COALESCE(SUM(oi.quantity * oi.price_at_order), 0) AS total_spent
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        GROUP BY c.customer_id
        ORDER BY total_spent DESC
    """).fetchall()
```

Streamlit-интерфейс дашборда:

```python
import streamlit as st
import pandas as pd
from database import get_connection, get_total_revenue, get_customer_totals

st.title("📊 Аналитика интернет-магазина")
conn = get_connection()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Общая выручка", f"{get_total_revenue(conn):,.0f} ₽")
col2.metric("👥 Клиентов",  conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0])
col3.metric("📦 Заказов",   conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0])

st.subheader("Топ клиентов по сумме покупок")
df = pd.DataFrame(get_customer_totals(conn), columns=["ФИО", "Город", "Сумма покупок, ₽"])
st.dataframe(df, use_container_width=True)
```

![Аналитический дашборд](./screenshots/Снимок%20экрана%202026-05-25%20194457.png)
*Аналитический дашборд: метрики выручки, числа клиентов и заказов; таблица Rollup по клиентам.*

---

## 3. Панель управления базой клиентов

Страница «Клиенты» реализует полный CRUD-цикл: просмотр таблицы, добавление новых клиентов через форму, удаление записей.

```python
st.title("👥 База клиентов")

# READ — отображение таблицы
df = pd.read_sql_query("SELECT * FROM customers", conn)
st.dataframe(df, use_container_width=True)

# CREATE — форма добавления
with st.expander("➕ Добавить клиента"):
    with st.form("add_customer"):
        fio    = st.text_input("ФИО")
        email  = st.text_input("Email")
        phone  = st.text_input("Телефон")
        city   = st.text_input("Город")
        status = st.selectbox("Статус", ["Активный", "Неактивный", "VIP"])
        if st.form_submit_button("Сохранить"):
            conn.execute(
                "INSERT INTO customers (fio, email, phone, city, status) VALUES (?,?,?,?,?)",
                (fio, email, phone, city, status)
            )
            conn.commit()
            st.success("Клиент добавлен!")
            st.rerun()
```

![База клиентов](./screenshots/Снимок%20экрана%202026-05-25%20194510.png)
*Панель управления базой клиентов: таблица с CRUD-операциями.*

---

## 4. Складской каталог товаров

Страница «Товары» отображает каталог с остатками на складе. CHECK-ограничения (`price > 0`, `stock >= 0`) применяются на уровне СУБД.

```python
st.title("📦 Каталог товаров")

df = pd.read_sql_query(
    "SELECT product_id, name, category, price, stock FROM products ORDER BY category",
    conn
)
st.dataframe(df, use_container_width=True)

with st.expander("➕ Добавить товар"):
    with st.form("add_product"):
        name     = st.text_input("Наименование")
        category = st.selectbox("Категория", ["Электроника", "Книги", "Одежда", "Другое"])
        price    = st.number_input("Цена, ₽", min_value=0.01, step=0.01)
        stock    = st.number_input("Остаток на складе", min_value=0, step=1)
        if st.form_submit_button("Сохранить"):
            conn.execute(
                "INSERT INTO products (name, category, price, stock) VALUES (?,?,?,?)",
                (name, category, price, stock)
            )
            conn.commit()
            st.success("Товар добавлен!")
            st.rerun()
```

![Каталог товаров](./screenshots/Снимок%20экрана%202026-05-25%20194521.png)
*Складской каталог: таблица товаров с категорией, ценой и остатками.*

---

## 5. CRUD-форма создания заказа — Lookup и валидация остатков

Форма заказа реализует две ключевые концепции low-code платформ:

- **Lookup** — динамическое подтягивание актуальной цены выбранного товара из таблицы `products`.
- **Валидация остатков** — проверка `quantity > stock` перед INSERT; при успешной транзакции выполняется списание (`UPDATE products SET stock = stock - quantity`).

```python
st.title("🛒 Создать заказ")

# Lookup: загрузка актуального каталога с ценами
products_df = pd.read_sql_query(
    "SELECT product_id, name, price, stock FROM products WHERE stock > 0", conn
)
product_options = {row["name"]: row for _, row in products_df.iterrows()}

customers_df = pd.read_sql_query("SELECT customer_id, fio FROM customers", conn)
customer_options = {row["fio"]: row["customer_id"] for _, row in customers_df.iterrows()}

with st.form("create_order"):
    customer_name  = st.selectbox("Клиент", list(customer_options.keys()))
    payment_method = st.selectbox("Способ оплаты", ["Карта", "Наличные", "Онлайн"])
    status         = st.selectbox("Статус", ["Новый", "В обработке", "Отправлен", "Доставлен"])

    st.markdown("**Позиции заказа**")
    product_name = st.selectbox("Товар", list(product_options.keys()))
    selected     = product_options[product_name]

    # Lookup: отображение актуальной цены
    st.info(f"Цена: {selected['price']:.2f} ₽ | На складе: {selected['stock']} шт.")
    quantity = st.number_input("Количество", min_value=1, step=1)

    if st.form_submit_button("Оформить заказ"):
        # Валидация остатков
        if quantity > selected["stock"]:
            st.error(f"Недостаточно товара на складе! Доступно: {selected['stock']} шт.")
        else:
            from datetime import date
            customer_id = customer_options[customer_name]
            today       = date.today().isoformat()

            # INSERT заказа
            cursor = conn.execute(
                "INSERT INTO orders (customer_id, order_date, status, payment_method) VALUES (?,?,?,?)",
                (customer_id, today, status, payment_method)
            )
            order_id = cursor.lastrowid

            # INSERT позиции с фиксацией цены (Lookup → price_at_order)
            conn.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, price_at_order) VALUES (?,?,?,?)",
                (order_id, int(selected["product_id"]), quantity, float(selected["price"]))
            )

            # Списание остатков со склада
            conn.execute(
                "UPDATE products SET stock = stock - ? WHERE product_id = ?",
                (quantity, int(selected["product_id"]))
            )
            conn.commit()
            st.success(f"Заказ #{order_id} успешно создан!")
            st.rerun()
```

![Форма заказа](./screenshots/Снимок%20экрана%202026-05-25%20194531.png)
*CRUD-форма создания заказа: Lookup актуальных цен и валидация остатков.*

---

## 6. Книга заказов

Страница «Заказы» отображает полную книгу транзакций через JOIN-запрос, связывающий заказы с клиентами, позициями и товарами:

```python
st.title("📋 Книга заказов")

orders_df = pd.read_sql_query("""
    SELECT
        o.order_id      AS "№",
        c.fio           AS "Клиент",
        o.order_date    AS "Дата",
        o.status        AS "Статус",
        o.payment_method AS "Оплата",
        COALESCE(SUM(oi.quantity * oi.price_at_order), 0) AS "Сумма, ₽"
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.order_id
    ORDER BY o.order_date DESC
""", conn)

st.dataframe(orders_df, use_container_width=True)
```

![Книга заказов](./screenshots/Снимок%20экрана%202026-05-25%20194538.png)
*Книга заказов: агрегированное представление транзакций с суммами (Rollup).*

---

# Технологии Программирования · Контрольные вопросы

<details>
<summary><strong>Вопрос 1. Каковы ключевые архитектурные и интерфейсные ограничения low-code подхода (Streamlit) по сравнению с классическим frontend-стеком (React/Vue + Node.js)?</strong></summary>

**Ответ:**  
Streamlit применяет **однопоточную модель исполнения**: при каждом взаимодействии пользователя с виджетом весь Python-скрипт перезапускается сверху вниз. В React/Vue обновляется только изменившийся компонент DOM через Virtual DOM diffing, что принципиально эффективнее при сложном интерактивном UI.

| Характеристика | Streamlit | React/Vue + Node.js |
|---|---|---|
| Модель обновления UI | Полный rerun скрипта | Точечное обновление компонента |
| Компонентная модель | Ограничена | Полная иерархия компонентов |
| Поддержка real-time | Только polling/`st.rerun()` | WebSockets, Server-Sent Events |
| Гибкость роутинга | Минимальна (`st.Page`) | Полный SPA-роутинг |
| Ролевой доступ | Не встроен | Реализуется middleware |
| SEO | Не поддерживается | Поддерживается (SSR) |

Для данной CRM-системы ограничения Streamlit не критичны: интерфейс предназначен для внутреннего использования, реального времени не требуется, а скорость разработки принципиально важнее гибкости UI.

</details>

<details>
<summary><strong>Вопрос 2. В каких сценариях и бизнес-задачах разработка на Streamlit эффективнее традиционного веб-программирования?</strong></summary>

**Ответ:**  
Streamlit оптимален в следующих сценариях:

1. **Внутренние аналитические дашборды** — визуализация KPI, отчётов, BI-метрик без UI-инженеров в команде.
2. **MVP и прототипы** — быстрая демонстрация идеи бизнес-заказчику за 1–2 дня без frontend-разработки.
3. **Инструменты ML-команды** — интерактивный интерфейс для моделей машинного обучения, A/B-тестирования параметров.
4. **Внутренние CRM/операционные формы** — небольшие команды (до 20 пользователей), нет требований к real-time и сложной ролевой модели.
5. **Data Science образование** — демонстрация алгоритмов без затрат на веб-инфраструктуру.

Tradиционный стек (React + Node.js) оправдан при высокой нагрузке, публичном доступе, сложном ролевом разграничении или требованиях к real-time обновлениям.

</details>

<details>
<summary><strong>Вопрос 3. Предложите стратегию масштабирования CRM-приложения при росте нагрузки до 1 миллиона заказов в день.</strong></summary>

**Ответ:**  
Текущая архитектура (SQLite + Streamlit) не способна обслуживать 1 млн заказов/день. Миграция выполняется поэтапно:

**Этап 1 — Переход с SQLite на PostgreSQL:**

```python
# Замена строки подключения в database.py
import psycopg2
conn = psycopg2.connect(
    host="db-host", port=5432,
    dbname="crm", user="app", password="..."
)
```

PostgreSQL обеспечивает MVCC (параллельные транзакции без блокировок на чтение), партиционирование таблицы `orders` по дате, индексы BRIN на `order_date` для временных запросов.

**Этап 2 — Apache Kafka как брокер очередей для записи заказов:**

Вместо синхронного INSERT при отправке формы заказ публикуется в топик `orders.created`:

```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=["kafka:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def submit_order_async(order_data: dict):
    producer.send("orders.created", value=order_data)
    pro