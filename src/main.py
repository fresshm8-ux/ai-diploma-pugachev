from file_utils import save_text, load_text, append_text, count_lines

save_text("project_note.txt", "Это первая строка проекта.")
append_text("project_note.txt", "Это вторая строка проекта.")

print(load_text("project_note.txt"))
print("Количество строк:", count_lines("project_note.txt"))