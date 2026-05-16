# AI Diploma Project
 
## 1. Загружаем функции из заранее подготовленных репозиторий
# 1
# 2 from text_utils import normalize_text, word_count, contains_word
# 3 from data_utils import find_by_make, filter_by_value, count_items
# 4 from file_utils import save_text, load_text, append_text, count_lines
# 5 from csv_utils import save_csv, load_csv, count_csv_rows, sum_column, average_column
# 6 from json_utils import save_json, load_json, dict_to_json_text
## 2. Записываем новые функции
build_project_report
1. normalize_text - номализация текста
2. word_count - подсчет слов
3. contains_word - проверка наличия слова
4. count_items - подсчет заданий
5. car_count - подсчет авто
И report в словаре
## 3. Исходные данные проекта
text - строка
tasks - список заданий
cars - список из словарей, краткое описание авто
## 4. Работа с текстом и данными
report - выполняет функцию build_project_report с text, tasks, cars
found_toyota - первое авто в списке с маркой Toyota
found_Volkswagen - первое авто в списке с маркой Volkswagen
cars_2000ml - все авто в списке с двигателем объемом 2л
## 5. Работа с текстовым файлом
save_text - сохраняет текст в файл
append_text - добавляет строку "Проект собран из нескольких модулей." в конец файла "project_note.txt"
loaded_note - Загружаем содержимое файла "project_note.txt" в переменную `loaded_note`.
note_lines - Подсчитываем количество строк в файле "project_note.txt" и сохраняем результат в `note_lines`.
## 6. Работа с CSV
rows - данные о видеокартах, список из словарей
loaded_products - загрузить данные
product_rows - количество продуктов
average_rating - средний рейтинг
total_reviews - количество отзывов
## 7 . JSON
Создание json файлов в папке
## 8 Вывод результатов