-- Таблица для хранения истории ошибок модели
CREATE TABLE IF NOT EXISTS model_errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    iteration INTEGER NOT NULL,
    parameter REAL NOT NULL,
    error REAL NOT NULL,
    derivative REAL NOT NULL,
    learning_rate REAL NOT NULL,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Таблица для хранения параметров модели
CREATE TABLE IF NOT EXISTS model_params (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    param_name TEXT NOT NULL,
    param_value REAL NOT NULL,
    description TEXT,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Таблица для хранения результатов оптимизации
CREATE TABLE IF NOT EXISTS optimization_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    optimizer_type TEXT NOT NULL,
    iterations INTEGER NOT NULL,
    final_error REAL NOT NULL,
    final_parameter REAL NOT NULL,
    execution_time REAL NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);