import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Конфигурация страницы веб-приложения
st.set_page_config(page_title="Low-Code CRM Streamlit", page_icon="🛍️", layout="wide")

DB_PATH = "crm_system.db"

def init_db():
    """Инициализация базы данных и создание связанных таблиц (Foreign Keys)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 1. Таблица Клиенты
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            fio TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            city TEXT,
            status TEXT DEFAULT 'Активный'
        )
    """)
    
    # 2. Таблица Товары
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL CHECK(price > 0),
            stock INTEGER NOT NULL CHECK(stock >= 0)
        )
    """)
    
    # 3. Таблица Заказы
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT DEFAULT 'Новый',
            payment_method TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
        )
    """)
    
    # 4. Таблица Позиции заказа
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            price_at_order REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)
    
    # Первичное наполнение тестовыми данными, если база пустая
    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO customers (fio, email, phone, city, status) VALUES (?, ?, ?, ?, ?)
        """, [
            ("Анна Смирнова", "anna@example.com", "+7-999-123-45-67", "Москва", "Активный"),
            ("Петр Иванов", "peter@example.com", "+7-912-345-67-89", "СПб", "Активный"),
            ("Мария Сидорова", "maria@example.com", "+7-921-678-90-12", "Казань", "VIP")
        ])
        
        cursor.executemany("""
            INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)
        """, [
            ("Ноутбук", "Электроника", 75000.0, 10),
            ("Мышь", "Электроника", 1500.0, 50),
            ("Книга SQL", "Книги", 2500.0, 30),
            ("Клавиатура", "Электроника", 5000.0, 15)
        ])
        
    conn.commit()
    conn.close()

init_db()

# Боковое навигационное меню (Аналог Views в Airtable)
st.sidebar.title("🛍️ CRM Low-Code Nav")
page = st.sidebar.radio("Перейти к разделу:", ["📊 Дашборд аналитики", "👥 Клиенты", "📦 Товары", "📝 Создать новый заказ", "🛒 Все заказы"])

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# --- РАЗДЕЛ 1: ДАШБОРД ---
if page == "📊 Дашборд аналитики":
    st.title("📊 Аналитическая панель интернет-магазина")
    conn = get_connection()
    
    df_items = pd.read_sql_query("SELECT quantity, price_at_order FROM order_items", conn)
    df_orders = pd.read_sql_query("SELECT * FROM orders", conn)
    
    total_revenue = (df_items['quantity'] * df_items['price_at_order']).sum()
    total_orders = len(df_orders)
    
    col1, col2 = st.columns(2)
    col1.metric("Общая выручка системы (Rollup)", f"{total_revenue:,.2f} руб.")
    col2.metric("Всего оформлено заказов", total_orders)
    
    st.subheader("📈 Последние транзакции в CRM")
    df_recent = pd.read_sql_query("""
        SELECT o.order_id as 'Номер заказа', c.fio as 'Клиент', o.order_date as 'Дата', o.status as 'Статус', 
               SUM(i.quantity * i.price_at_order) as 'Сумма заказа (руб)'
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        LEFT JOIN order_items i ON o.order_id = i.order_id
        GROUP BY o.order_id ORDER BY o.order_id DESC LIMIT 5
    """, conn)
    st.dataframe(df_recent, use_container_width=True)
    conn.close()

# --- РАЗДЕЛ 2: КЛИЕНТЫ ---
elif page == "👥 Клиенты":
    st.title("👥 Управление базой клиентов")
    conn = get_connection()
    
    with st.expander("➕ Добавить нового клиента (Форма ввода)"):
        with st.form("add_customer_form"):
            fio = st.text_input("ФИО клиента *")
            email = st.text_input("Email адрес *")
            phone = st.text_input("Номер телефона")
            city = st.text_input("Город")
            status = st.selectbox("Статус", ["Активный", "Неактивный", "VIP"])
            
            submit = st.form_submit_button("Сохранить клиента")
            if submit:
                if not fio or not email:
                    st.error("Ошибка валидации: Поля ФИО и Email обязательны для заполнения!")
                else:
                    try:
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO customers (fio, email, phone, city, status) VALUES (?, ?, ?, ?, ?)",
                                       (fio, email, phone, city, status))
                        conn.commit()
                        st.success(f"Клиент {fio} успешно добавлен!")
                    except sqlite3.IntegrityError:
                        st.error("Ошибка: Клиент с таким Email уже существует!")

    df_cust = pd.read_sql_query("""
        SELECT c.customer_id as 'ID', c.fio as 'ФИО', c.email as 'Email', c.phone as 'Телефон', 
               c.city as 'Город', c.status as 'Статус',
               COALESCE(SUM(i.quantity * i.price_at_order), 0) as 'Сумма покупок (Rollup)'
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        LEFT JOIN order_items i ON o.order_id = i.order_id
        GROUP BY c.customer_id
    """, conn)
    st.dataframe(df_cust, use_container_width=True)
    conn.close()

# --- РАЗДЕЛ 3: ТОВАРЫ ---
elif page == "📦 Товары":
    st.title("📦 Каталог товаров и склад")
    conn = get_connection()
    
    with st.expander("➕ Добавить новый товар"):
        with st.form("add_product_form"):
            name = st.text_input("Наименование товара *")
            category = st.selectbox("Категория", ["Электроника", "Книги", "Одежда", "Другое"])
            price = st.number_input("Цена (руб)", min_value=0.0, value=100.0)
            stock = st.number_input("Количество на складе", min_value=0, value=10)
            
            submit = st.form_submit_button("Добавить на склад")
            if submit:
                if not name or price <= 0:
                    st.error("Ошибка валидации: Название не должно быть пустым, а цена должна быть больше 0!")
                else:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)",
                                   (name, category, price, stock))
                    conn.commit()
                    st.success(f"Товар '{name}' успешно добавлен в каталог!")
                    
    df_prod = pd.read_sql_query("SELECT product_id as 'ID', name as 'Наименование', category as 'Категория', price as 'Цена (руб)', stock as 'Остаток на складе' FROM products", conn)
    st.dataframe(df_prod, use_container_width=True)
    conn.close()

# --- РАЗДЕЛ 4: СОЗДАНИЕ ЗАКАЗА ---
elif page == "📝 Создать новый заказ":
    st.title("📝 Оформление комплексного заказа (CRUD Форма)")
    conn = get_connection()
    cursor = conn.cursor()
    
    customers = cursor.execute("SELECT customer_id, fio FROM customers").fetchall()
    products = cursor.execute("SELECT product_id, name, price, stock FROM products WHERE stock > 0").fetchall()
    
    cust_options = {c[1]: c[0] for c in customers}
    prod_options = {f"{p[1]} ({p[2]} руб.) [Остаток: {p[3]} шт.]": (p[0], p[2], p[3]) for p in products}
    
    if not cust_options or not prod_options:
        st.error("Для создания заказа в системе должны быть клиенты и доступные товары!")
    else:
        with st.form("order_wizard"):
            chosen_cust = st.selectbox("Выберите клиента *", list(cust_options.keys()))
            order_date = st.date_input("Дата оформления заказа", max_value=datetime.today())
            status = st.selectbox("Статус заказа", ["Новый", "В обработке", "Отправлен", "Доставлен"])
            payment_method = st.selectbox("Способ оплаты", ["Карта", "Наличные", "Онлайн"])
            
            st.markdown("---")
            st.subheader("🛒 Выберите товар (Позиция заказа)")
            chosen_prod = st.selectbox("Выберите товар *", list(prod_options.keys()))
            quantity = st.number_input("Количество единиц *", min_value=1, value=1)
            
            submit_order = st.form_submit_button("🔴 РАЗМЕСТИТЬ ЗАКАЗ В CRM")
            
            if submit_order:
                prod_id, price, stock = prod_options[chosen_prod]
                if quantity > stock:
                    st.error(f"Ошибка валидации: Недостаточно товара на складе! Доступно всего: {stock} шт.")
                else:
                    # 1. Вставка заказа
                    cursor.execute("""
                        INSERT INTO orders (customer_id, order_date, status, payment_method) 
                        VALUES (?, ?, ?, ?)
                    """, (cust_options[chosen_cust], str(order_date), status, payment_method))
                    order_id = cursor.lastrowid
                    
                    # 2. Вставка позиции заказа (Lookup цены)
                    cursor.execute("""
                        INSERT INTO order_items (order_id, product_id, quantity, price_at_order) 
                        VALUES (?, ?, ?, ?)
                    """, (order_id, prod_id, quantity, price))
                    
                    # 3. Списание остатков
                    cursor.execute("UPDATE products SET stock = stock - ? WHERE product_id = ?", (quantity, prod_id))
                    
                    conn.commit()
                    st.success(f"🚀 Заказ №{order_id} для {chosen_cust} успешно сохранен в базе данных!")
    conn.close()

# --- РАЗДЕЛ 5: ВСЕ ЗАКАЗЫ ---
elif page == "🛒 Все заказы":
    st.title("🛒 Книга заказов интернет-магазина (Представление)")
    conn = get_connection()
    
    df_all_orders = pd.read_sql_query("""
        SELECT o.order_id as 'Номер заказа', c.fio as 'Клиент', o.order_date as 'Дата заказа', 
               o.status as 'Статус', o.payment_method as 'Способ оплаты',
               p.name as 'Товар', i.quantity as 'Кол-во',
               (i.quantity * i.price_at_order) as 'Итоговая сумма (Formula)'
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN order_items i ON o.order_id = i.order_id
        JOIN products p ON i.product_id = p.product_id
        ORDER BY o.order_id DESC
    """, conn)
    
    st.dataframe(df_all_orders, use_container_width=True)
    conn.close()