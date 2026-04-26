# AI Diploma Project
 
## Как запустить (локально в VS Code)
1) Установите Python 3.11+
2) (Рекомендуется) создайте окружение и установите зависимости:
   ```bash
   python -m venv venv
   source venv/Scripts/activate
   pip install -r requirements.txt
   ```
   git checkout -b feature/m1-project-structure
3) Запуск CLI:
   ```bash
   python -m src.cli
   ```
 
## Структура
- `src/core.py` — логика (items, validate, stats)
- `src/parsers.py` — парсинг/нормализация
- `src/storage.py` — JSON, состояние, экспорт/импорт
- `src/cli.py` — запуск и команды
- `colab/` — ноутбуки lesson_XX / hw_XX
- `data/` — локальные данные (в проде лучше БД/volume)
 
## команды
venv/Scripts/activate
git switch main
 
git switch feature/lesson-15-data-utils
python -m src.main
 
## если что-то уже поменял в ветке
git add .
git commit -m "save progress"
git checkout main
git pull origin main
git checkout -b feature/new-lesson
 
git add .
git commit -m "save current progress"
git checkout main
 
## если надо удалить ветки и создать заново
## удаление ветки не изменяет main
git branch
git checkout main
git pull origin main
git branch -D feature/lesson-14-strings
git branch -D feature/lesson-15-data-utils
git branch -D feature/lesson-16-file-utils
git push origin --delete feature/lesson-14-strings
git push origin --delete feature/lesson-15-data-utils
git push origin --delete feature/lesson-16-file-utils
git checkout -b feature/new-lesson
git push -u origin feature/new-lesson
 
## перейти в ветку, если она узе существует
git switch feature/lesson-17-csv-utils
 
## в начале урока
```bash
# 1. Посмотреть ветку, состояние main, синхронизация с main, создать новую папку
git branch
git checkout main
git pull origin main
git checkout -b feature/lesson-17-csv-util
 
# 2. Переименовать текущую ветку
# Было: feature/lesson-16-data-utils
# Станет: feature/lesson-16-file-utils
git branch -m feature/lesson-16-file-utils
 
# 3. Проверить, что ветка переименовалась
git branch
 
# 4. Отправить новую ветку на GitHub
git push -u origin feature/lesson-16-file-utils
 
# 5. Если старая ветка уже была на GitHub, удалить её там
git push origin --delete feature/lesson-16-data-utils
 
# 6. Проверить статус
git status
```
## в конце урока
# 1. Посмотреть, какие файлы изменились
git status
 
# 2. Добавить все изменения в commit
git add .
 
# 3. Сделать commit
git commit -m "feat: add lesson 17 csv utils"
 
# 4. Отправить ветку на GitHub
git push -u origin feature/lesson-17-csv-utils
 
## дальше на гитхаб
Create Pull Request → Merge Pull Request → Confirm merge
 
## после merge
# 1. Вернуться в main
git checkout main
 
# 2. Подтянуть свежий main после merge
git pull origin main
 
# Если надо изменить ветку
git add .
git commit -m "save"
