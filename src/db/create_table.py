import sqlite3

print("sqlite3 успешно подключен")

connection = sqlite3.connect("students_lesson01.db")

print("База данных создана или открыта")

cursor = connection.cursor()

print("Cursor создан")

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    city TEXT,
    age INTEGER
)
""")

print("Таблица students создана")

cursor.execute(
    "INSERT INTO students (name, city, age) VALUES (?, ?, ?)",
    ("Анна", "Казань", 20)
)

cursor.execute(
    "INSERT INTO students (name, city, age) VALUES (?, ?, ?)",
    ("Иван", "Москва", 21)
)

cursor.execute(
    "INSERT INTO students (name, city, age) VALUES (?, ?, ?)",
    ("Ольга", "Казань", 19)
)

cursor.execute(
    "INSERT INTO students (name, city, age) VALUES (?, ?, ?)",
    ("Петр", "Санкт-Петербург", 22)
)

cursor.execute(
    "INSERT INTO students (name, city, age) VALUES (?, ?, ?)",
    ("Мария", "Казань", 20)
)

print("Данные добавлены")

connection.commit()

print("Изменения сохранены")

cursor.execute("SELECT * FROM students")

students = cursor.fetchall()

print(students)

assert len(students) >= 3
assert len(students) >= 4
assert len(students) >= 5

for student in students:
    print("ID:", student[0], "| Имя:", student[1], "| Город:", student[2], "| Возраст:", student[3])

cursor.execute(
    "SELECT * FROM students WHERE city = ?",
    ("Казань",)
)

kazan_students = cursor.fetchall()

print(kazan_students)

assert len(kazan_students) >= 1

connection.close()

print("Соединение с базой данных закрыто")