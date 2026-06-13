import sqlite3

connection = sqlite3.connect("shop_lesson02.db")
cursor = connection.cursor()

print("База данных подключена")

cursor.execute("""
CREATE TABLE IF NOT EXISTS building_materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    category TEXT,
    price INTEGER,
    count INTEGER
)
""")

connection.commit()

print("Таблица building_materials создана")

cursor.execute("DELETE FROM building_materials")

building_materials = [
    ("Цемент М500", "Строительные материалы", 500, 100),
    ("Кирпич красный", "Строительные материалы", 25, 1000),
    ("Доска обрезная 50х150", "Пиломатериалы", 800, 50),
    ("Штукатурка гипсовая", "Отделочные материалы", 300, 75),
    ("Краска водоэмульсионная", "Отделочные материалы", 1500, 20),
    ("Саморезы по дереву", "Крепеж", 10, 5000),
    ("Песок строительный", "Строительные материалы", 150, 200),
    ("Арматура D12", "Металлопрокат", 700, 30)
]

cursor.executemany(
    "INSERT INTO building_materials (title, category, price, count) VALUES (?, ?, ?, ?)",
    building_materials
)

connection.commit()

print("Тестовые товары добавлены")

cursor.execute("SELECT * FROM building_materials")

all_building_materials = cursor.fetchall()

for product in all_building_materials:
    print(product)

assert len(all_building_materials) == 8

cursor.execute("SELECT category, count FROM building_materials")

category_and_count = cursor.fetchall()

for row in category_and_count:
    print(row)

assert len(category_and_count) == 8

cursor.execute(
    "SELECT * FROM building_materials WHERE price < ?",
    (700,)
)

expensive_building_materials = cursor.fetchall()

for product in expensive_building_materials:
    print(product)

cursor.execute(
    "SELECT * FROM building_materials WHERE category = ?",
    ("Строительные материалы",)
)

tech_building_materials = cursor.fetchall()

for product in tech_building_materials:
    print(product)

assert len(tech_building_materials) == 3

cursor.execute(
    "SELECT * FROM building_materials WHERE category = ? AND price > ?",
    ("Отделочные материалы", 500)
)

filtered_and = cursor.fetchall()

print("Отделочные материалы дороже 500:")
for product in filtered_and:
    print(product)

cursor.execute(
    "SELECT * FROM building_materials WHERE category = ? OR category = ?",
    ("Строительные материалы", "Отделочные материалы")
)

filtered_or = cursor.fetchall()

print("\nСтроительные материалы или Отделочные материалы:")
for product in filtered_or:
    print(product)

cursor.execute(
    "SELECT * FROM building_materials ORDER BY count DESC LIMIT 5"
)

top_expensive = cursor.fetchall()

for building_material in top_expensive:
    print(building_material)

assert len(top_expensive) == 5

connection.close()

print("Соединение закрыто")
