from text_utils import normalize_text, word_count, contains_word
from data_utils import find_by_make, filter_by_value, count_items
from file_utils import save_text, load_text, append_text, count_lines
from csv_utils import save_csv, load_csv, count_csv_rows, sum_column, average_column
from json_utils import save_json, load_json, dict_to_json_text


def build_project_report(text, tasks, cars):
    clean_text = normalize_text(text)
    words = word_count(clean_text)
    has_python = contains_word(clean_text, "python")
    task_count = count_items(tasks)
    car_count = count_items(cars)

    report = {
        "clean_text": clean_text,
        "word_count": words,
        "has_python": has_python,
        "task_count": task_count,
        "car_count": car_count
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

    cars = [
        {"make": "Toyota", "model": "Corolla", "volume in ml": 1500},
        {"make": "Volkswagen", "model": "Tayron", "volume in ml": 1400},
        {"make": "Kia", "model": "K3", "volume in ml": 2000},
        {"make": "Volkswagen", "model": "Golf", "volume in ml": 2000},
        {"make": "Mazda", "model": "CX-4", "volume in ml": 2500}
    ]

    # 2. Работа с текстом и данными
    report = build_project_report(text, tasks, cars)

    found_toyota = find_by_make(cars, "Toyota")
    found_Volkswagen = find_by_make(cars, "Volkswagen")
    cars_2000ml = filter_by_value(cars, "volume in ml", 2000)

    # 3. Работа с текстовым файлом
    save_text("project_note.txt", report["clean_text"])
    append_text("project_note.txt", "Проект собран из нескольких модулей.")

    loaded_note = load_text("project_note.txt")
    note_lines = count_lines("project_note.txt")

    # 4. Работа с CSV
    rows = [
        ["vender", "model_name", "memory_gb", "rating", "reviews"],
        ["MSI", "NVIDIA RTX 4060", 8, 4.85, 30],
        ["GigaByte", "NVIDIA RTX 5070 TI", 16, 4.9, 311],
        ["Asus", "AMD Radeon RX 9070", 24, 4.7, 101]
    ]

    save_csv("products.csv", rows)
    loaded_products = load_csv("products.csv")
    product_rows = count_csv_rows("products.csv")
    average_rating = average_column("products.csv", 3)
    average_rating = round(average_rating, 2)
    total_reviews = sum_column("products.csv", 4)


    # 5. Работа с JSON
    project_config = {
        "project_name": "car_final_project",
        "task_count": report["task_count"],
        "car_count": report["car_count"],
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

    print("2. Данные авто:")
    print("Найденное авто Toyota:", found_toyota)
    print("Найденное авто Volkswagen:", found_Volkswagen)
    print("Авто с 2л:", cars_2000ml)
    print("Количество авто:", report["car_count"])
    print()

    print("3. Текстовый файл:")
    print("Содержимое project_note.txt:")
    print(loaded_note)
    print("Количество строк:", note_lines)
    print()

    print("4. CSV:")
    print("Данные products.csv:", loaded_products)
    print("Количество строк в CSV:", product_rows)
    print("Средний rating:", average_rating)
    print("Количество reviews:", total_reviews)
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
