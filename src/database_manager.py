"""
Модуль для работы с базой данных
"""

import sqlite3
import os
from pathlib import Path
from datetime import datetime

class DatabaseManager:
    """Класс для управления базой данных"""
    
    def __init__(self, db_path="database/model_data.db"):
        self.db_path = db_path
        self.connection = None
        self._ensure_database_dir()
        self._initialize_database()
    
    def _ensure_database_dir(self):
        """Создает директорию для БД если её нет"""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(exist_ok=True)
    
    def _initialize_database(self):
        """Инициализирует базу данных"""
        with self.connect() as conn:
            cursor = conn.cursor()
            
            # Создаем таблицы
            cursor.executescript('''
                CREATE TABLE IF NOT EXISTS model_errors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    iteration INTEGER NOT NULL,
                    parameter REAL NOT NULL,
                    error REAL NOT NULL,
                    derivative REAL NOT NULL,
                    learning_rate REAL NOT NULL,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS model_params (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    param_name TEXT NOT NULL,
                    param_value REAL NOT NULL,
                    description TEXT,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS optimization_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    optimizer_type TEXT NOT NULL,
                    iterations INTEGER NOT NULL,
                    final_error REAL NOT NULL,
                    final_parameter REAL NOT NULL,
                    execution_time REAL NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            
            conn.commit()
    
    def connect(self):
        """Устанавливает соединение с БД"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def save_iteration(self, iteration, parameter, error, derivative, learning_rate):
        """Сохраняет итерацию оптимизации в БД"""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO model_errors 
                (iteration, parameter, error, derivative, learning_rate)
                VALUES (?, ?, ?, ?, ?)
            ''', (iteration, parameter, error, derivative, learning_rate))
            conn.commit()
    
    def save_optimization_result(self, optimizer_type, iterations, final_error, 
                                 final_parameter, execution_time):
        """Сохраняет результат оптимизации"""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO optimization_history 
                (optimizer_type, iterations, final_error, final_parameter, execution_time)
                VALUES (?, ?, ?, ?, ?)
            ''', (optimizer_type, iterations, final_error, final_parameter, execution_time))
            conn.commit()
    
    def get_history(self, limit=None):
        """Получает историю оптимизации из БД"""
        with self.connect() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM model_errors ORDER BY iteration"
            if limit:
                query += f" LIMIT {limit}"
            cursor.execute(query)
            return cursor.fetchall()
    
    def get_optimization_results(self):
        """Получает результаты всех оптимизаций"""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM optimization_history ORDER BY created_at DESC")
            return cursor.fetchall()
    
    def clear_history(self):
        """Очищает историю"""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM model_errors")
            cursor.execute("DELETE FROM optimization_history")
            conn.commit()