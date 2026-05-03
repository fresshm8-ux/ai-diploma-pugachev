from text_utils import normalize_text, word_count, contains_word
from data_utils import find_by_name, filter_by_value, count_items
from file_utils import save_text, load_text, append_text, count_lines
from csv_utils import save_csv, load_csv, count_csv_rows, sum_column
from json_utils import save_json, load_json, dict_to_json_text


def build_project_report(text, tasks, students):
    clean_text = normalize_text(text)
    words = word_count(clean_text)
    has_python = contains_word(clean_text, "python")
    task_count = count_items(tasks)
    student_count = count_items(students)

    report = {
        "clean_text": clean_text,
        "word_count": words,
        "has_python": has_python,
        "task_count": task_count,
        "student_count": student_count
    }

    return report


def run_project_scenario():
    # 1. Исходные данные проекта
    text = "   Мой первый проект на Python   "

    tasks = [
        "изучить строки",
        "изучить списки словарей",
        "изучить файлы",
        "изучить CSV",
        "изучить JSON",
        "собрать проект"
    ]

    students = [
        {"name": "Анна", "city": "Казань", "age": 20},
        {"name": "Иван", "city": "Москва", "age": 21},
        {"name": "Ольга", "city": "Казань", "age": 19},
        {"name": "Павел", "city": "Уфа", "age": 22}
    ]

    # 2. Работа с текстом и данными
    report = build_project_report(text, tasks, students)

    found_student = find_by_name(students, "Иван")
    kazan_students = filter_by_value(students, "city", "Казань")

    # 3. Работа с текстовым файлом
    save_text("project_note.txt", report["clean_text"])
    append_text("project_note.txt", "Проект собран из нескольких модулей.")

    loaded_note = load_text("project_note.txt")
    note_lines = count_lines("project_note.txt")

    # 4. Работа с CSV
    rows = [
        ["title", "price", "count"],
        ["Ноутбук", 50000, 2],
        ["Мышь", 1500, 5],
        ["Клавиатура", 3000, 3]
    ]

    save_csv("products.csv", rows)
    loaded_products = load_csv("products.csv")
    product_rows = count_csv_rows("products.csv")
    total_price = sum_column("products.csv", 1)

    # 5. Работа с JSON
    project_config = {
        "project_name": "student_final_project",
        "task_count": report["task_count"],
        "student_count": report["student_count"],
        "note_lines": note_lines,
        "product_rows": product_rows
    }

    save_json("project_config.json", project_config)
    loaded_config = load_json("project_config.json")
    config_text = dict_to_json_text(loaded_config)

    # 6. Вывод результата
    print("=== Финальный учебный проект ===")
    print()
    print("1. Текст:")
    print("Очищенный текст:", report["clean_text"])
    print("Количество слов:", report["word_count"])
    print("Есть слово python:", report["has_python"])
    print()

    print("2. Данные студентов:")
    print("Найден студент Иван:", found_student)
    print("Студенты из Казани:", kazan_students)
    print("Количество студентов:", report["student_count"])
    print()

    print("3. Текстовый файл:")
    print("Содержимое project_note.txt:")
    print(loaded_note)
    print("Количество строк:", note_lines)
    print()

    print("4. CSV:")
    print("Данные products.csv:", loaded_products)
    print("Количество строк в CSV:", product_rows)
    print("Сумма столбца price:", total_price)
    print()

    print("5. JSON:")
    print("Загруженная конфигурация:", loaded_config)
    print("JSON-текст:")
    print(config_text)
    print()

    print("Проект успешно запущен.")


def main():
    run_project_scenario()


if __name__ == "__main__":
    main()
