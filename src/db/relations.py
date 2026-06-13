import sqlite3

connection = sqlite3.connect("relations_lesson05.db")
cursor = connection.cursor()

print("База данных подключена")

cursor.execute("PRAGMA foreign_keys = ON")

print("Поддержка FOREIGN KEY включена")

cursor.execute("DROP TABLE IF EXISTS interviews")
cursor.execute("DROP TABLE IF EXISTS candidates")
cursor.execute("""
CREATE TABLE candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER
)
""")

connection.commit()

print("Таблица candidates создана")

cursor.execute("DROP TABLE IF EXISTS interviews")
cursor.execute("""
CREATE TABLE interviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER,
    position TEXT,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id)
)
""")

connection.commit()

print("Таблица interviews создана")

cursor.execute("DELETE FROM interviews")
cursor.execute("DELETE FROM candidates")

connection.commit()

print("Таблицы очищены")

candidates = [
    ("Елена М.О.", 30),
    ("Даниил У.Ф.", 25)
]

cursor.executemany(
    "INSERT INTO candidates (name, age) VALUES (?, ?)",
    candidates
)

connection.commit()

print("Кандидаты добавлены")

cursor.execute("SELECT * FROM candidates")

candidates_data = cursor.fetchall()

for candidate in candidates_data:
    print(candidate)

elena_id = candidates_data[0][0]
daniil_id = candidates_data[1][0]

print("ID Елены:", elena_id)
print("ID Даниила:", daniil_id)

assert elena_id is not None
assert daniil_id is not None

interviews = [
    (elena_id, "programmer"),
    (elena_id, "front_end"),
    (daniil_id, "tester")
]

cursor.executemany(
    "INSERT INTO interviews (candidate_id, position) VALUES (?, ?)",
    interviews
)

connection.commit()

print("Заказы добавлены")

print("Кандидаты:")
cursor.execute("SELECT * FROM candidates")
candidates_rows = cursor.fetchall()
for row in candidates_rows:
    print(row)

print("\nИнтервью:")
cursor.execute("SELECT * FROM interviews")
interviews_rows = cursor.fetchall()
for row in interviews_rows:
    print(row)

assert len(candidates_rows) == 2

cursor.execute(
    "SELECT * FROM interviews WHERE candidate_id = ?",
    (elena_id,)
)

elena_interviews = cursor.fetchall()

print("Интервью Елены:")
for interview in elena_interviews:
    print(interview)


connection.close()
print("Соединение закрыто")