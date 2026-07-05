#!/usr/bin/env python3
"""
ML Error Function Analyzer
Анализ функции ошибки модели машинного обучения
"""

import sys
import os
from pathlib import Path

# Добавляем src в путь
sys.path.insert(0, str(Path(__file__).parent))

from src.error_function import ErrorFunction
from src.optimizer import Optimizer
from src.visualizer import Visualizer
from src.database_manager import DatabaseManager
from tabulate import tabulate

def print_header(text):
    """Печатает красивый заголовок"""
    print("\n" + "="*80)
    print(f" {text}")
    print("="*80)

def print_section(text):
    """Печатает раздел"""
    print("\n" + "-"*60)
    print(f" {text}")
    print("-"*60)

def main():
    """Главная функция"""
    
    print_header("🧠 АНАЛИЗ ФУНКЦИИ ОШИБКИ МОДЕЛИ")
    
    # Инициализация БД
    print("\n📁 Инициализация базы данных...")
    db = DatabaseManager()
    
    # Создаем объекты
    visualizer = Visualizer()
    
    # Выбор функции ошибки
    print_section("Выбор функции ошибки")
    print("\nДоступные функции:")
    print("1. Квадратичная: f(x) = (x-3)² + 2 (простая)")
    print("2. Синусоидальная: f(x) = sin(x) + 0.1x²")
    print("3. Сложная: f(x) = (x-2)²(x+1)² + 0.5sin(2x)")
    print("4. Экспоненциальная: f(x) = e^(-0.5x) + x²/10")
    
    # Выбор функции (можно захардкодить для автоматизации)
    func_type = input("\nВыберите функцию (1-4): ").strip()
    func_map = {
        '1': 'quadratic',
        '2': 'sine', 
        '3': 'complex',
        '4': 'exponential'
    }
    
    function_type = func_map.get(func_type, 'quadratic')
    error_func = ErrorFunction(function_type=function_type)
    
    # Информация о функции
    info = error_func.get_function_info()
    print(f"\n📊 Выбрана функция: {info['name']}")
    print(f"   Формула: {info['formula']}")
    
    # Построение графика функции
    print_section("График функции ошибки")
    print("📈 Построение графика функции...")
    visualizer.plot_error_function(error_func, title=f"Функция ошибки - {info['name']}")
    
    # Построение графика производной
    print_section("График производной")
    print("📈 Построение графика производной...")
    visualizer.plot_derivative(error_func)
    
    # Выбор метода оптимизации
    print_section("Выбор метода оптимизации")
    print("1. Градиентный спуск (стандартный)")
    print("2. Градиентный спуск с моментом (ускоренный)")
    
    method = input("\nВыберите метод (1-2): ").strip()
    
    # Параметры оптимизации
    print_section("Параметры оптимизации")
    
    try:
        x0 = float(input("Начальное значение x (по умолчанию 5): ") or "5")
        learning_rate = float(input("Скорость обучения (по умолчанию 0.1): ") or "0.1")
        max_iterations = int(input("Максимум итераций (по умолчанию 50): ") or "50")
    except ValueError:
        print("Использую значения по умолчанию")
        x0 = 5.0
        learning_rate = 0.1
        max_iterations = 50
    
    # Оптимизация
    print_section("Запуск оптимизации")
    print("⏳ Оптимизация выполняется...")
    
    optimizer = Optimizer(error_func)
    
    if method == '2':
        momentum = float(input("Коэффициент момента (по умолчанию 0.9): ") or "0.9")
        result = optimizer.momentum_gradient_descent(
            x0, learning_rate=learning_rate, 
            momentum=momentum, max_iterations=max_iterations
        )
        optimizer_type = "momentum_gd"
    else:
        result = optimizer.gradient_descent(
            x0, learning_rate=learning_rate, 
            max_iterations=max_iterations
        )
        optimizer_type = "gd"
    
    # Сохраняем результат в БД
    db.save_optimization_result(
        optimizer_type=optimizer_type,
        iterations=result['iterations'],
        final_error=result['final_error'],
        final_parameter=result['final_parameter'],
        execution_time=result['execution_time']
    )
    
    # Сохраняем историю в БД
    history = optimizer.get_history()
    for h in history:
        db.save_iteration(
            iteration=h['iteration'],
            parameter=h['x'],
            error=h['error'],
            derivative=h['derivative'],
            learning_rate=h['learning_rate']
        )
    
    # Вывод результатов
    print_section("Результаты оптимизации")
    
    results_data = [
        ["Параметр", f"{result['final_parameter']:.6f}"],
        ["Ошибка", f"{result['final_error']:.6f}"],
        ["Итераций", result['iterations']],
        ["Время выполнения", f"{result['execution_time']:.4f} сек"],
        ["Вызовов функции", result['function_calls']],
        ["Вызовов производной", result['derivative_calls']]
    ]
    
    print(tabulate(results_data, tablefmt="grid"))
    
    # Построение пути оптимизации
    print_section("Визуализация процесса оптимизации")
    print("📈 Построение графика пути оптимизации...")
    visualizer.plot_optimization_path(error_func, history, 
                                     title=f"Путь оптимизации - {info['name']}")
    
    # Сравнение методов (если есть данные в БД)
    print_section("Сравнение методов оптимизации")
    
    # Запускаем второй метод для сравнения
    print("🔄 Запускаем второй метод для сравнения...")
    
    error_func2 = ErrorFunction(function_type=function_type)
    optimizer2 = Optimizer(error_func2)
    
    if method == '2':
        result2 = optimizer2.gradient_descent(x0, learning_rate, max_iterations)
        method2_name = "Стандартный GD"
    else:
        result2 = optimizer2.momentum_gradient_descent(x0, learning_rate, 0.9, max_iterations)
        method2_name = "Momentum GD"
    
    comparison = {
        "Выбранный метод": result,
        method2_name: result2
    }
    
    # Сравнительная таблица
    comp_data = []
    for name, res in comparison.items():
        comp_data.append([
            name,
            f"{res['final_error']:.6f}",
            res['iterations'],
            f"{res['execution_time']:.4f} сек"
        ])
    
    print("\nСравнение результатов:")
    print(tabulate(comp_data, 
                   headers=["Метод", "Финальная ошибка", "Итераций", "Время"],
                   tablefmt="grid"))
    
    # Создаем словарь для визуализации сравнения
    comparison_dict = {
        "Выбранный": comparison["Выбранный метод"],
        "Сравнение": comparison[method2_name]
    }
    
    # Визуализация сравнения
    print("📊 Построение графика сравнения...")
    visualizer.plot_comparison(comparison_dict)
    
    # Итоговый отчет
    print_section("📄 Генерация отчета")
    
    # Сохраняем отчет в файл
    os.makedirs('reports', exist_ok=True)
    with open('reports/optimization_report.txt', 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("ОТЧЕТ ПО ОПТИМИЗАЦИИ ФУНКЦИИ ОШИБКИ\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Функция: {info['name']}\n")
        f.write(f"Формула: {info['formula']}\n\n")
        
        f.write("РЕЗУЛЬТАТЫ ОПТИМИЗАЦИИ:\n")
        f.write("-"*40 + "\n")
        f.write(f"Финальный параметр: {result['final_parameter']:.6f}\n")
        f.write(f"Минимальная ошибка: {result['final_error']:.6f}\n")
        f.write(f"Количество итераций: {result['iterations']}\n")
        f.write(f"Время выполнения: {result['execution_time']:.4f} сек\n\n")
        
        f.write("ИСТОРИЯ ОПТИМИЗАЦИИ:\n")
        f.write("-"*40 + "\n")
        f.write(f"{'Итерация':<10} {'Параметр':<12} {'Ошибка':<12} {'Производная':<12}\n")
        f.write("-"*50 + "\n")
        
        for h in history[:20]:  # Показываем первые 20 итераций
            f.write(f"{h['iteration']:<10} {h['x']:<12.6f} {h['error']:<12.6f} {h['derivative']:<12.6f}\n")
        
        if len(history) > 20:
            f.write(f"... и еще {len(history) - 20} итераций\n")
    
    print("\n✅ Отчет сохранен в 'reports/optimization_report.txt'")
    print("📊 Графики сохранены в 'reports/plots/'")
    
    print_header("🎉 АНАЛИЗ ЗАВЕРШЕН")
    
    # Показываем, где лежат файлы
    print("\n📁 Созданные файлы:")
    print("   • reports/optimization_report.txt - текстовый отчет")
    print("   • reports/plots/error_function.png - график функции")
    print("   • reports/plots/derivative_analysis.png - график производной")
    print("   • reports/plots/optimization_path.png - путь оптимизации")
    print("   • reports/plots/optimizer_comparison.png - сравнение методов")
    print("   • database/model_data.db - база данных с историей")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Программа прервана пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка: {str(e)}")
        import traceback
        traceback.print_exc()