import sqlite3

connection = sqlite3.connect("hr_analytics.db")
cursor = connection.cursor()

print("База данных подключена")

cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    city TEXT,
    age INTEGER,
    rating INTEGER,
    revenue INTEGER
)
""")

connection.commit()

print("Таблица candidates создана")

cursor.execute("DELETE FROM candidates")

candidates_data = [
    ("Иван", "Москва", 30, 8, 50000),
    ("Мария", "Казань", 25, 9, 60000),
    ("Петр", "Уфа", 35, 7, 45000),
    ("Анна", "Санкт-Петербург", 28, 7, 55000),
    ("Сергей", "Казань", 40, 6, 70000),
    ("Елена", "Москва", 27, 8, 52000),
    ("Дмитрий", "Уфа", 32, 7, 48000),
    ("Ольга", "Санкт-Петербург", 29, 9, 62000),
    ("Павел", "Казань", 38, 6, 68000),
    ("Светлана", "Москва", 26, 9, 58000)
]

cursor.executemany(
    "INSERT INTO candidates (name, city, age, rating, revenue) VALUES (?, ?, ?, ?, ?)",
    candidates_data
)

connection.commit()

print("Данные для таблицы candidates добавлены")

cursor.execute("SELECT COUNT(*) FROM candidates")

total_rows = cursor.fetchone()[0]

print("Количество строк:", total_rows)

assert total_rows == 10

cursor.execute("SELECT SUM(revenue) FROM candidates")

total_revenue = cursor.fetchone()[0]

print("Общая зарплата:", total_revenue)

assert total_revenue > 0

cursor.execute("SELECT AVG(revenue), MIN(revenue), MAX(revenue) FROM candidates")

avg_revenue, min_revenue, max_revenue = cursor.fetchone()

print("Средняя зарплата:", round(avg_revenue, 2))
print("Минимальная зарплата:", min_revenue)
print("Максимальная зарплата:", max_revenue)

assert max_revenue >= min_revenue

cursor.execute("""
SELECT city, COUNT(*), SUM(revenue), AVG(age)
FROM candidates
GROUP BY city
""")

city_report = cursor.fetchall()

for row in city_report:
    print("Город:", row[0], "| Количество кандидатов:", row[1], "| Общая ожидаемая зарплата:", row[2], "| Средний возраст:", round(row[3], 2))

assert len(city_report) >= 1

cursor.execute("""
SELECT city, SUM(revenue) AS total_revenue
FROM candidates
GROUP BY city
ORDER BY total_revenue DESC
""")

sorted_categories = cursor.fetchall()

for row in sorted_categories:
    print("Город:", row[0], "| Общая ожидаемая зарплата:", row[1])

assert sorted_categories[0][1] >= sorted_categories[-1][1]

cursor.execute("""
SELECT city, SUM(revenue) AS total_revenue
FROM candidates
GROUP BY city
ORDER BY total_revenue DESC
""")

sorted_categories = cursor.fetchall()

for row in sorted_categories:
    print("Город:", row[0], "| Общая ожидаемая зарплата:", row[1])

assert sorted_categories[0][1] >= sorted_categories[-1][1]

cursor.execute("""
SELECT city, SUM(revenue) AS total_revenue
FROM candidates
GROUP BY city
HAVING SUM(revenue) > 30000
ORDER BY total_revenue DESC
""")

big_categories = cursor.fetchall()

print("Города с общей ожидаемой зарплатой больше 30000:")
for row in big_categories:
    print("Город:", row[0], "| Общая ожидаемая зарплата:", row[1])

assert len(big_categories) >= 1
connection.close()
print("Соединение закрыто")
