#!/usr/bin/env python3
"""
Главный скрипт для анализа продаж
"""

import sqlite3
import os
import sys
from datetime import datetime
from tabulate import tabulate

def format_number(value):
    """Форматирует число с разделителями тысяч и без копеек"""
    if value is None:
        return "0"
    # Округляем до целого числа и добавляем разделители тысяч
    return f"{int(round(value)):,}"

def print_header(text):
    """Печатает красивые заголовки"""
    print("\n" + "="*80)
    print(f" {text}")
    print("="*80)

def check_database():
    """Проверяет наличие и заполненность БД"""
    if not os.path.exists('database/sales.db'):
        print("\n❌ База данных не найдена!")
        print("📝 Создаю новую базу данных...")
        return False
    
    # Проверяем, есть ли данные
    conn = sqlite3.connect('database/sales.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sales")
    count = cursor.fetchone()[0]
    conn.close()
    
    if count == 0:
        print("\n⚠️ База данных пуста!")
        print("📝 Заполняю данными...")
        return False
    
    print(f"\n✅ База данных найдена. Содержит {count} продаж.")
    return True

def create_and_fill_database():
    """Создает БД и заполняет тестовыми данными"""
    
    # Создаем директорию если её нет
    os.makedirs('database', exist_ok=True)
    
    conn = sqlite3.connect('database/sales.db')
    cursor = conn.cursor()
    
    # Создаем таблицы
    print("📋 Создание таблиц...")
    cursor.executescript('''
        DROP TABLE IF EXISTS sales;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS customers;
        
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        );
        
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            city TEXT NOT NULL
        );
        
        CREATE TABLE sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            sale_date TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );
    ''')
    
    # Добавляем товары (20 товаров, 5 категорий)
    print("🛍️ Добавление товаров...")
    products = [
        # Электроника
        ("Ноутбук", "Электроника", 55000),
        ("Смартфон", "Электроника", 35000),
        ("Планшет", "Электроника", 25000),
        ("Монитор", "Электроника", 22000),
        ("Телевизор", "Электроника", 45000),
        # Аксессуары
        ("Наушники", "Аксессуары", 5000),
        ("Клавиатура", "Аксессуары", 3500),
        ("Мышь", "Аксессуары", 1500),
        ("Чехол", "Аксессуары", 1000),
        ("Зарядка", "Аксессуары", 2000),
        # Одежда
        ("Футболка", "Одежда", 1500),
        ("Джинсы", "Одежда", 4000),
        ("Куртка", "Одежда", 8000),
        ("Кроссовки", "Одежда", 6000),
        ("Шапка", "Одежда", 800),
        # Дом
        ("Чайник", "Дом", 2500),
        ("Микроволновка", "Дом", 8000),
        ("Пылесос", "Дом", 12000),
        # Книги
        ("Python книга", "Книги", 1200),
        ("SQL книга", "Книги", 1000),
    ]
    
    for name, category, price in products:
        cursor.execute("INSERT INTO products (name, category, price) VALUES (?, ?, ?)",
                      (name, category, price))
    
    # Добавляем покупателей (15 человек)
    print("👥 Добавление покупателей...")
    customers = [
        ("Иван Петров", "ivan@mail.ru", "Москва"),
        ("Мария Сидорова", "maria@mail.ru", "Санкт-Петербург"),
        ("Алексей Иванов", "alex@mail.ru", "Новосибирск"),
        ("Елена Смирнова", "elena@mail.ru", "Екатеринбург"),
        ("Дмитрий Козлов", "dmitry@mail.ru", "Казань"),
        ("Анна Кузнецова", "anna@mail.ru", "Москва"),
        ("Сергей Попов", "sergey@mail.ru", "Санкт-Петербург"),
        ("Ольга Васильева", "olga@mail.ru", "Новосибирск"),
        ("Павел Соколов", "pavel@mail.ru", "Москва"),
        ("Наталья Михайлова", "natalia@mail.ru", "Казань"),
        ("Владимир Новиков", "vladimir@mail.ru", "Москва"),
        ("Екатерина Федорова", "ekaterina@mail.ru", "Санкт-Петербург"),
        ("Андрей Морозов", "andrey@mail.ru", "Новосибирск"),
        ("Юлия Алексеева", "yulia@mail.ru", "Москва"),
        ("Максим Орлов", "maxim@mail.ru", "Казань"),
    ]
    
    for name, email, city in customers:
        cursor.execute("INSERT INTO customers (name, email, city) VALUES (?, ?, ?)",
                      (name, email, city))
    
    # Генерируем продажи
    print("💰 Генерация продаж...")
    import random
    from datetime import datetime, timedelta
    
    cursor.execute("SELECT id FROM products")
    product_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id FROM customers")
    customer_ids = [row[0] for row in cursor.fetchall()]
    
    start_date = datetime(2024, 1, 1)
    sales_count = 300  # Генерируем 300 продаж
    
    for i in range(sales_count):
        product_id = random.choice(product_ids)
        customer_id = random.choice(customer_ids)
        
        # Случайная дата в 2024 году
        random_days = random.randint(0, 365)
        sale_date = start_date + timedelta(days=random_days)
        
        quantity = random.randint(1, 5)
        
        # Получаем цену товара
        cursor.execute("SELECT price FROM products WHERE id = ?", (product_id,))
        price = cursor.fetchone()[0]
        total_amount = price * quantity
        
        cursor.execute('''
            INSERT INTO sales (product_id, customer_id, sale_date, quantity, total_amount)
            VALUES (?, ?, ?, ?, ?)
        ''', (product_id, customer_id, sale_date.strftime('%Y-%m-%d'), quantity, total_amount))
        
        if (i + 1) % 100 == 0:
            print(f"   Сгенерировано {i + 1} продаж...")
    
    conn.commit()
    
    # Проверяем результат
    cursor.execute("SELECT COUNT(*) FROM products")
    product_cnt = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM customers")
    customer_cnt = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM sales")
    sales_cnt = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"\n✅ База данных создана!")
    print(f"   📦 Товаров: {product_cnt}")
    print(f"   👥 Покупателей: {customer_cnt}")
    print(f"   💰 Продаж: {sales_cnt}")
    
    return True

def analyze_sales():
    """Выполняет анализ продаж"""
    
    conn = sqlite3.connect('database/sales.db')
    cursor = conn.cursor()
    
    # 1. Выручка по категориям товаров
    print("\n📊 1. ВЫРУЧКА ПО КАТЕГОРИЯМ ТОВАРОВ:")
    query = '''
        SELECT 
            p.category,
            COUNT(*) as sales_count,
            ROUND(SUM(s.total_amount), 0) as total_revenue,
            ROUND(AVG(s.total_amount), 0) as avg_check
        FROM sales s
        JOIN products p ON s.product_id = p.id
        GROUP BY p.category
        ORDER BY total_revenue DESC
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    
    if results:
        table_data = []
        for row in results:
            table_data.append([
                row[0], 
                row[1], 
                format_number(row[2]),  # Форматированная выручка
                format_number(row[3])   # Форматированный средний чек
            ])
        
        print(tabulate(table_data, 
                      headers=["Категория", "Продажи", "Выручка (руб)", "Средний чек (руб)"],
                      tablefmt="grid",
                      stralign="left",
                      numalign="right"))
    
    # 2. Топ-10 покупателей
    print("\n🏆 2. ТОП-10 ПОКУПАТЕЛЕЙ ПО СУММЕ ПОКУПОК:")
    query = '''
        SELECT 
            c.name,
            c.city,
            COUNT(s.id) as purchases,
            ROUND(SUM(s.total_amount), 0) as total_spent,
            ROUND(AVG(s.total_amount), 0) as avg_purchase
        FROM customers c
        JOIN sales s ON c.id = s.customer_id
        GROUP BY c.id
        ORDER BY total_spent DESC
        LIMIT 10
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    
    if results:
        table_data = []
        for row in results:
            table_data.append([
                row[0], 
                row[1], 
                row[2], 
                format_number(row[3]), 
                format_number(row[4])
            ])
        
        print(tabulate(table_data,
                      headers=["Покупатель", "Город", "Покупок", "Сумма (руб)", "Средний чек (руб)"],
                      tablefmt="grid",
                      stralign="left",
                      numalign="right"))
    
    # 3. Динамика продаж по месяцам
    print("\n📈 3. ДИНАМИКА ПРОДАЖ ПО МЕСЯЦАМ:")
    query = '''
        SELECT 
            strftime('%Y-%m', s.sale_date) as month,
            COUNT(*) as sales_count,
            ROUND(SUM(s.total_amount), 0) as revenue,
            COUNT(DISTINCT s.customer_id) as unique_customers
        FROM sales s
        GROUP BY month
        ORDER BY month
        LIMIT 12
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    
    if results:
        table_data = []
        for row in results:
            table_data.append([
                row[0], 
                row[1], 
                format_number(row[2]), 
                row[3]
            ])
        
        print(tabulate(table_data,
                      headers=["Месяц", "Продажи", "Выручка (руб)", "Покупателей"],
                      tablefmt="grid",
                      stralign="left",
                      numalign="right"))
    
    # 4. Средний чек по городам (улучшенное форматирование)
    print("\n🏙️ 4. СРЕДНИЙ ЧЕК ПО ГОРОДАМ:")
    query = '''
        SELECT 
            c.city,
            COUNT(DISTINCT c.id) as customers,
            COUNT(s.id) as sales_count,
            ROUND(AVG(s.total_amount), 0) as avg_check,
            ROUND(SUM(s.total_amount), 0) as total_revenue
        FROM customers c
        JOIN sales s ON c.id = s.customer_id
        GROUP BY c.city
        ORDER BY avg_check DESC
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    
    if results:
        table_data = []
        for row in results:
            table_data.append([
                row[0],
                row[1],
                row[2],
                format_number(row[3]),
                format_number(row[4])
            ])
        
        print(tabulate(table_data,
                      headers=["Город", "Покупателей", "Продаж", "Средний чек (руб)", "Выручка (руб)"],
                      tablefmt="grid",
                      stralign="left",
                      numalign="right"))
    
    # 5. Самые популярные товары
    print("\n⭐ 5. ТОП-5 САМЫХ ПОПУЛЯРНЫХ ТОВАРОВ:")
    query = '''
        SELECT 
            p.name,
            p.category,
            SUM(s.quantity) as total_sold,
            COUNT(DISTINCT s.customer_id) as buyers,
            ROUND(SUM(s.total_amount), 0) as revenue
        FROM products p
        JOIN sales s ON p.id = s.product_id
        GROUP BY p.id
        ORDER BY total_sold DESC
        LIMIT 5
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    
    if results:
        table_data = []
        for row in results:
            table_data.append([
                row[0], 
                row[1], 
                row[2], 
                row[3], 
                format_number(row[4])
            ])
        
        print(tabulate(table_data,
                      headers=["Товар", "Категория", "Продано (шт)", "Покупателей", "Выручка (руб)"],
                      tablefmt="grid",
                      stralign="left",
                      numalign="right"))
    
    # 6. Общая статистика
    print("\n📊 6. ОБЩАЯ СТАТИСТИКА:")
    cursor.execute('''
        SELECT 
            COUNT(*) as total_sales,
            ROUND(SUM(total_amount), 0) as total_revenue,
            ROUND(AVG(total_amount), 0) as avg_sale,
            COUNT(DISTINCT customer_id) as unique_customers,
            COUNT(DISTINCT product_id) as unique_products,
            MIN(sale_date) as first_sale,
            MAX(sale_date) as last_sale
        FROM sales
    ''')
    stats = cursor.fetchone()
    
    print(f"   • Всего продаж:           {stats[0]:,}")
    print(f"   • Общая выручка:          {format_number(stats[1])} руб.")
    print(f"   • Средний чек:            {format_number(stats[2])} руб.")
    print(f"   • Уникальных покупателей: {stats[3]}")
    print(f"   • Уникальных товаров:     {stats[4]}")
    print(f"   • Период:                 с {stats[5]} по {stats[6]}")
    
    conn.close()

def save_report():
    """Сохраняет отчет в файл"""
    
    os.makedirs('reports', exist_ok=True)
    
    conn = sqlite3.connect('database/sales.db')
    cursor = conn.cursor()
    
    with open('reports/analytics_report.txt', 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("ОТЧЕТ ПО АНАЛИТИКЕ ПРОДАЖ\n")
        f.write(f"Дата генерации: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        
        # Выручка по категориям
        f.write("1. ВЫРУЧКА ПО КАТЕГОРИЯМ ТОВАРОВ\n")
        f.write("-"*40 + "\n")
        cursor.execute('''
            SELECT p.category, COUNT(*) as cnt, ROUND(SUM(s.total_amount), 0) as revenue
            FROM sales s JOIN products p ON s.product_id = p.id
            GROUP BY p.category ORDER BY revenue DESC
        ''')
        results = cursor.fetchall()
        for row in results:
            f.write(f"   {row[0]}: {row[1]} продаж, выручка {format_number(row[2])} руб.\n")
        
        # Топ покупателей
        f.write("\n2. ТОП-5 ПОКУПАТЕЛЕЙ\n")
        f.write("-"*40 + "\n")
        cursor.execute('''
            SELECT c.name, c.city, COUNT(*) as purchases, ROUND(SUM(s.total_amount), 0) as spent
            FROM sales s JOIN customers c ON s.customer_id = c.id
            GROUP BY c.id ORDER BY spent DESC LIMIT 5
        ''')
        results = cursor.fetchall()
        for i, row in enumerate(results, 1):
            f.write(f"   {i}. {row[0]} ({row[1]}): {row[2]} покупок на сумму {format_number(row[3])} руб.\n")
        
        # Общая статистика
        cursor.execute('SELECT COUNT(*) FROM sales')
        total_sales = cursor.fetchone()[0]
        cursor.execute('SELECT ROUND(SUM(total_amount), 0) FROM sales')
        total_revenue = cursor.fetchone()[0]
        
        f.write("\n3. ОБЩАЯ СТАТИСТИКА\n")
        f.write("-"*40 + "\n")
        f.write(f"   Всего продаж: {total_sales}\n")
        f.write(f"   Общая выручка: {format_number(total_revenue)} руб.\n")
    
    conn.close()
    print(f"\n📄 Полный отчет сохранен в 'reports/analytics_report.txt'")

def main():
    """Главная функция"""
    
    print_header("СИСТЕМА АНАЛИЗА ПРОДАЖ")
    
    # Проверяем и создаем БД при необходимости
    if not check_database():
        create_and_fill_database()
    
    # Выполняем анализ
    analyze_sales()
    
    # Сохраняем отчет
    save_report()
    
    print_header("АНАЛИЗ УСПЕШНО ЗАВЕРШЕН")

if __name__ == "__main__":
    main()