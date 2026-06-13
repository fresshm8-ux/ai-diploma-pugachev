import sqlite3

connection = sqlite3.connect("crud_lesson03.db")
cursor = connection.cursor()

print("База подключена")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    weight TEXT,
    calories INTEGER
)
""")

connection.commit()

print("Таблица products создана")

cursor.execute("DELETE FROM products")

connection.commit()

print("Таблица очищена")

products = [
    ("Hamburger", "150g", 300),
    ("Cheeseburger", "180g", 350),
    ("Fries", "120g", 250),
    ("Cola", "300ml", 150)
]

cursor.executemany(
    "INSERT INTO products (name, weight, calories) VALUES (?, ?, ?)",
    products
)

connection.commit()

print("Продукты добавлены")

cursor.execute("SELECT * FROM products")

products_data = cursor.fetchall()

for product in products_data:
    print(product)

assert len(products_data) == 4

cursor.execute(
    "UPDATE products SET calories = ? WHERE name = ?",
    (350, "Hamburger")
)

connection.commit()

print("Калории обновлена")

cursor.execute(
    "SELECT * FROM products WHERE name = ?",
    ("Hamburger",)
)

Hamburger = cursor.fetchone()

print(Hamburger)

assert Hamburger[3] == 350

cursor.execute(
    "DELETE FROM products WHERE name = ?",
    ("Cola",)
)

connection.commit()

print("Запись удалена")

cursor.execute("SELECT * FROM products")

products_after_delete = cursor.fetchall()

for employee in products_after_delete:
    print(employee)

assert len(products_after_delete) == 3

connection.close()

print("Соединение закрыто")
