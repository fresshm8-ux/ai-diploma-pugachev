from text_utils import normalize_text
from data_utils import count_items

def show_menu():
    print("Выберите действие:")
    print("1 - обработать текст")
    print("2 - посчитать количество объектов")
    print("0 - выход")

def run_choice(choice):
    if choice == "1":
        text = "   Мой проект на Python   "
        print("Результат:", normalize_text(text))
    elif choice == "2":
        items = ["строки", "файлы", "json"]
        print("Количество:", count_items(items))
    elif choice == "0":
        print("Программа завершена")
    else:
        print("Неизвестная команда")