import sqlite3
import random
from datetime import datetime, timedelta
from tabulate import tabulate

# СОЗДАНИЕ БД
conn = sqlite3.connect('database/sales.db')
cursor = conn.cursor()

# Создание таблиц
cursor.executescript('''
    DROP TABLE IF EXISTS sales;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS customers;
    
    CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL);
    CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, email TEXT, city TEXT);
    CREATE TABLE sales (id INTEGER PRIMARY KEY, product_id INTEGER, customer_id INTEGER, 
                       sale_date TEXT, quantity INTEGER, total_amount REAL);
''')

# Товары (20 штук)
products = [
    ("Ноутбук", "Электроника", 55000), ("Смартфон", "Электроника", 35000),
    ("Наушники", "Аксессуары", 5000), ("Клавиатура", "Аксессуары", 3500),
    ("Футболка", "Одежда", 1500), ("Джинсы", "Одежда", 4000),
    ("Чайник", "Дом", 2500), ("Микроволновка", "Дом", 8000),
    ("Python книга", "Книги", 1200), ("Мышь", "Аксессуары", 1500),
    ("Куртка", "Одежда", 8000), ("Пылесос", "Дом", 12000),
    ("Планшет", "Электроника", 25000), ("Монитор", "Электроника", 22000),
    ("Чехол", "Аксессуары", 1000), ("Кроссовки", "Одежда", 6000),
    ("SQL книга", "Книги", 1000), ("Зарядка", "Аксессуары", 2000),
    ("Телевизор", "Электроника", 45000), ("Шапка", "Одежда", 800)
]

for name, cat, price in products:
    cursor.execute("INSERT INTO products (name, category, price) VALUES (?,?,?)", (name, cat, price))

# Покупатели (15 человек)
customers = [
    ("Иван Петров", "ivan@mail.ru", "Москва"), ("Мария Сидорова", "maria@mail.ru", "СПб"),
    ("Алексей Иванов", "alex@mail.ru", "Новосибирск"), ("Елена Смирнова", "elena@mail.ru", "Екатеринбург"),
    ("Дмитрий Козлов", "dima@mail.ru", "Казань"), ("Анна Кузнецова", "anna@mail.ru", "Москва"),
    ("Сергей Попов", "sergey@mail.ru", "СПб"), ("Ольга Васильева", "olga@mail.ru", "Новосибирск"),
    ("Павел Соколов", "pavel@mail.ru", "Москва"), ("Наталья Михайлова", "natalia@mail.ru", "Казань"),
    ("Владимир Новиков", "vlad@mail.ru", "Москва"), ("Екатерина Федорова", "katya@mail.ru", "СПб"),
    ("Андрей Морозов", "andrey@mail.ru", "Новосибирск"), ("Юлия Алексеева", "yulia@mail.ru", "Москва"),
    ("Максим Орлов", "max@mail.ru", "Казань")
]

for name, email, city in customers:
    cursor.execute("INSERT INTO customers (name, email, city) VALUES (?,?,?)", (name, email, city))

# Генерация продаж (300 штук)
cursor.execute("SELECT id FROM products")
product_ids = [r[0] for r in cursor.fetchall()]
cursor.execute("SELECT id FROM customers")
customer_ids = [r[0] for r in cursor.fetchall()]

start = datetime(2024, 1, 1)
for _ in range(300):
    pid = random.choice(product_ids)
    cid = random.choice(customer_ids)
    date = start + timedelta(days=random.randint(0, 365))
    qty = random.randint(1, 4)
    cursor.execute("SELECT price FROM products WHERE id=?", (pid,))
    price = cursor.fetchone()[0]
    cursor.execute("INSERT INTO sales (product_id, customer_id, sale_date, quantity, total_amount) VALUES (?,?,?,?,?)",
                  (pid, cid, date.strftime('%Y-%m-%d'), qty, price*qty))

conn.commit()

# АНАЛИЗ
print("\n" + "="*70)
print("РЕЗУЛЬТАТЫ АНАЛИЗА ПРОДАЖ")
print("="*70)

# 1. Выручка по категориям
print("\n📊 ВЫРУЧКА ПО КАТЕГОРИЯМ:")
cursor.execute('''
    SELECT p.category, COUNT(*) as cnt, ROUND(SUM(s.total_amount),0) as revenue
    FROM sales s JOIN products p ON s.product_id=p.id
    GROUP BY p.category ORDER BY revenue DESC
''')
print(tabulate(cursor.fetchall(), headers=["Категория", "Продажи", "Выручка (руб)"], tablefmt="grid"))

# 2. Топ покупателей
print("\n🏆 ТОП-5 ПОКУПАТЕЛЕЙ:")
cursor.execute('''
    SELECT c.name, c.city, COUNT(*) as purchases, ROUND(SUM(s.total_amount),0) as spent
    FROM sales s JOIN customers c ON s.customer_id=c.id
    GROUP BY c.id ORDER BY spent DESC LIMIT 5
''')
print(tabulate(cursor.fetchall(), headers=["Имя", "Город", "Покупок", "Потрачено (руб)"], tablefmt="grid"))

# 3. Общая статистика
cursor.execute('SELECT COUNT(*) FROM sales')
total_sales = cursor.fetchone()[0]
cursor.execute('SELECT ROUND(SUM(total_amount),0) FROM sales')
total_revenue = cursor.fetchone()[0]
cursor.execute('SELECT ROUND(AVG(total_amount),0) FROM sales')
avg_check = cursor.fetchone()[0]

print(f"\n📈 ОБЩАЯ СТАТИСТИКА:")
print(f"   • Всего продаж: {total_sales}")
print(f"   • Общая выручка: {total_revenue:,.0f} руб.")
print(f"   • Средний чек: {avg_check:,.0f} руб.")

conn.close()
print("\n✅ Готово! Запустите: python quick_start.py")