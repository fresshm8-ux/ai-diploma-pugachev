import sqlite3

connection = sqlite3.connect("join_lesson06.db")
cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

print("База данных подключена")


cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    city TEXT
)
""")

connection.commit()

print("Таблица users создана")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT,
    price INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

connection.commit()

print("Таблица orders создана")

cursor.execute("DELETE FROM orders")
cursor.execute("DELETE FROM users")

users = [
    ("Анна", "Казань"),
    ("Иван", "Москва"),
    ("Ольга", "Уфа"),
    ("Петр", "Самара"),
    ("Мария", "Екатеринбург")
]

cursor.executemany(
    "INSERT INTO users (name, city) VALUES (?, ?)",
    users
)

connection.commit()

print("Пользователи добавлены")

cursor.execute("SELECT * FROM users")
users_data = cursor.fetchall()

for user in users_data:
    print(user)

anna_id = users_data[0][0]
ivan_id = users_data[1][0]
olga_id = users_data[2][0]
petr_id = users_data[3][0]
mariya_id = users_data[4][0]

orders = [
    (anna_id, "Ноутбук", 70000),
    (anna_id, "Мышь", 1500),
    (ivan_id, "Книга Python", 2500),
    (petr_id, "Велосипед", 30000),
    (mariya_id, "Наушники", 5000)
]

cursor.executemany(
    "INSERT INTO orders (user_id, title, price) VALUES (?, ?, ?)",
    orders
)

connection.commit()

print("Заказы добавлены")

print("USERS:")
cursor.execute("SELECT * FROM users")
users_rows = cursor.fetchall()
for row in users_rows:
    print(row)

print("\nORDERS:")
cursor.execute("SELECT * FROM orders")
orders_rows = cursor.fetchall()
for row in orders_rows:
    print(row)


cursor.execute("""
SELECT users.name, users.city, orders.title, orders.price
FROM users
INNER JOIN orders ON users.id = orders.user_id
""")

join_rows = cursor.fetchall()

for row in join_rows:
    print(row)

assert len(join_rows) == 5

cursor.execute("""
SELECT users.name, users.city, orders.title, orders.price
FROM users
INNER JOIN orders ON users.id = orders.user_id
""")

all_joined_orders = cursor.fetchall()

for row in all_joined_orders:
    print(row)

assert len(all_joined_orders) == 5

cursor.execute("""
SELECT users.name, users.city, orders.title, orders.price
FROM users
LEFT JOIN orders ON users.id = orders.user_id
""")

left_join_rows = cursor.fetchall()

for row in left_join_rows:
    print(row)

assert len(left_join_rows) == 6

cursor.execute("""
SELECT users.name, COUNT(orders.id), SUM(orders.price)
FROM users
LEFT JOIN orders ON users.id = orders.user_id
GROUP BY users.id
""")

report = cursor.fetchall()

print("Отчёт по пользователям:")
for row in report:
    print("Пользователь:", row[0], "| Количество заказов:", row[1], "| Сумма:", row[2])

assert len(report) == 5

connection.close()
print("Соединение закрыто")

