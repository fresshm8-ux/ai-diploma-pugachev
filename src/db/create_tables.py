import sqlite3

connection = sqlite3.connect("design_lesson04.db")
cursor = connection.cursor()

print("База данных подключена")

cursor.execute("""
CREATE TABLE IF NOT EXISTS meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    meal_type TEXT,
    calories INTEGER,
    protein REAL,
    fat REAL,
    carbs REAL
)
""")

connection.commit()

print("Таблица meals создана")

cursor.execute("""
CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exercise TEXT,
    workout_type TEXT,
    duration_min INTEGER,
    calories_burned INTEGER,
    effort INTEGER
)
""")

connection.commit()

print("Таблица workouts создана")

cursor.execute("""
CREATE TABLE IF NOT EXISTS resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    position TEXT,
    experience_years INTEGER,
    city TEXT,
    score REAL
)
""")

connection.commit()

print("Таблица resumes создана")

cursor.execute("""
SELECT name FROM sqlite_master
WHERE type = 'table'
""")

tables = cursor.fetchall()

print("Таблицы в базе:")
for table in tables:
    print(table)

assert len(tables) >= 3

cursor.execute(
    "INSERT INTO resumes (full_name, position, experience_years, city, score) VALUES (?, ?, ?, ?, ?)",
    ("Анна Смирнова", "Python Developer", 2, "Казань", 87.5)
)

cursor.execute(
    "INSERT INTO resumes (full_name, position, experience_years, city, score) VALUES (?, ?, ?, ?, ?)",
    ("Иван Петров", "Data Analyst", 1, "Москва", 78.0)
)

cursor.execute(
    "INSERT INTO resumes (full_name, position, experience_years, city, score) VALUES (?, ?, ?, ?, ?)",
    ("Ольга Козлова", "Project Manager", 5, "Санкт-Петербург", 92.0)
)

cursor.execute(
    "INSERT INTO resumes (full_name, position, experience_years, city, score) VALUES (?, ?, ?, ?, ?)",
    ("Дмитрий Волков", "Frontend Developer", 3, "Екатеринбург", 85.0)
)

connection.commit()

print("Резюме добавлены")

cursor.execute(
    "INSERT INTO meals (product, meal_type, calories, protein, fat, carbs) VALUES (?, ?, ?, ?, ?, ?)",
    ("Овсянка", "breakfast", 350, 12.5, 6.0, 60.0)
)

cursor.execute(
    "INSERT INTO meals (product, meal_type, calories, protein, fat, carbs) VALUES (?, ?, ?, ?, ?, ?)",
    ("Курица", "lunch", 450, 35.0, 10.0, 25.0)
)

cursor.execute(
    "INSERT INTO meals (product, meal_type, calories, protein, fat, carbs) VALUES (?, ?, ?, ?, ?, ?)",
    ("Яблоко", "snack", 95, 0.5, 0.3, 25.0)
)

cursor.execute(
    "INSERT INTO meals (product, meal_type, calories, protein, fat, carbs) VALUES (?, ?, ?, ?, ?, ?)",
    ("Рыба", "dinner", 300, 30.0, 15.0, 0.0)
)

connection.commit()

print("Данные питания добавлены")

cursor.execute(
    "INSERT INTO workouts (exercise, workout_type, duration_min, calories_burned, effort) VALUES (?, ?, ?, ?, ?)",
    ("Бег", "cardio", 40, 420, 7)
)

cursor.execute(
    "INSERT INTO workouts (exercise, workout_type, duration_min, calories_burned, effort) VALUES (?, ?, ?, ?, ?)",
    ("Приседания", "strength", 30, 250, 8)
)

cursor.execute(
    "INSERT INTO workouts (exercise, workout_type, duration_min, calories_burned, effort) VALUES (?, ?, ?, ?, ?)",
    ("Прыжки на скакалке", "cardio", 20, 200, 6)
)

cursor.execute(
    "INSERT INTO workouts (exercise, workout_type, duration_min, calories_burned, effort) VALUES (?, ?, ?, ?, ?)",
    ("Отжимания", "strength", 15, 100, 7)
)

connection.commit()

print("Тренировки добавлены")

for table_name in ["resumes", "meals", "workouts"]:
    print("\nТаблица:", table_name)
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    assert len(rows) >= 1

connection.close()

print("Соединение закрыто")    