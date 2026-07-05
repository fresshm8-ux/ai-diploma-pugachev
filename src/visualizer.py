"""
Модуль для визуализации функции ошибки и процесса оптимизации
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Rectangle
import os

class Visualizer:
    """Класс для построения графиков"""
    
    def __init__(self):
        """Инициализация визуализатора"""
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 12
        
        # Создаем папку для графиков
        os.makedirs('reports/plots', exist_ok=True)
    
    def plot_error_function(self, error_function, x_range=(-5, 8), title="Функция ошибки"):
        """
        Построение графика функции ошибки
        
        Args:
            error_function: объект ErrorFunction
            x_range: диапазон x
            title: заголовок графика
        """
        x_values = np.linspace(x_range[0], x_range[1], 1000)
        y_values = [error_function.calculate_error(x) for x in x_values]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Основной график
        ax.plot(x_values, y_values, 'b-', linewidth=2, label='f(x)')
        
        # Находим минимум
        min_idx = np.argmin(y_values)
        ax.plot(x_values[min_idx], y_values[min_idx], 'r*', markersize=15, 
                label=f'Минимум: x={x_values[min_idx]:.2f}, f(x)={y_values[min_idx]:.2f}')
        
        # Информация о функции
        info = error_function.get_function_info()
        ax.set_title(f"{title}\n{info['formula']}", fontsize=14)
        ax.set_xlabel('Параметр (x)', fontsize=12)
        ax.set_ylabel('Ошибка f(x)', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('reports/plots/error_function.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def plot_optimization_path(self, error_function, history, title="Путь оптимизации"):
        """
        Построение графика пути оптимизации
        
        Args:
            error_function: объект ErrorFunction
            history: история оптимизации
            title: заголовок графика
        """
        if not history:
            print("Нет истории для отображения")
            return None
        
        # Извлекаем данные из истории
        iterations = [h['iteration'] for h in history]
        x_values = [h['x'] for h in history]
        errors = [h['error'] for h in history]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # График 1: Ошибка по итерациям
        ax1.plot(iterations, errors, 'bo-', linewidth=2, markersize=8, label='Ошибка')
        ax1.set_title('Снижение ошибки', fontsize=14)
        ax1.set_xlabel('Итерация', fontsize=12)
        ax1.set_ylabel('Ошибка', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # График 2: Путь оптимизации на функции
        x_plot = np.linspace(min(x_values) - 1, max(x_values) + 1, 500)
        y_plot = [error_function.calculate_error(x) for x in x_plot]
        
        ax2.plot(x_plot, y_plot, 'b-', linewidth=2, alpha=0.5, label='f(x)')
        ax2.plot(x_values, errors, 'ro-', linewidth=2, markersize=8, 
                label='Путь оптимизации')
        ax2.scatter(x_values[0], errors[0], color='green', s=100, 
                   label='Старт', zorder=5)
        ax2.scatter(x_values[-1], errors[-1], color='red', s=100, 
                   label='Финиш', zorder=5)
        
        ax2.set_title('Траектория оптимизации', fontsize=14)
        ax2.set_xlabel('Параметр (x)', fontsize=12)
        ax2.set_ylabel('Ошибка', fontsize=12)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('reports/plots/optimization_path.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def plot_comparison(self, results_comparison):
        """
        Построение сравнительного графика для разных оптимизаторов
        
        Args:
            results_comparison: словарь с результатами разных методов
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        methods = list(results_comparison.keys())
        errors = [results_comparison[m]['final_error'] for m in methods]
        iterations = [results_comparison[m]['iterations'] for m in methods]
        
        # График 1: Сравнение финальной ошибки
        colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']
        bars = ax1.bar(methods, errors, color=colors[:len(methods)])
        ax1.set_title('Финальная ошибка', fontsize=14)
        ax1.set_ylabel('Ошибка', fontsize=12)
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Добавляем значения на столбцы
        for bar, error in zip(bars, errors):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{error:.4f}', ha='center', va='bottom', fontsize=10)
        
        # График 2: Сравнение итераций
        bars = ax2.bar(methods, iterations, color=colors[:len(methods)])
        ax2.set_title('Количество итераций', fontsize=14)
        ax2.set_ylabel('Итерации', fontsize=12)
        ax2.grid(True, alpha=0.3, axis='y')
        
        for bar, iters in zip(bars, iterations):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{iters}', ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        plt.savefig('reports/plots/optimizer_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def plot_derivative(self, error_function, x_range=(-5, 8)):
        """
        Построение графика функции и её производной
        
        Args:
            error_function: объект ErrorFunction
            x_range: диапазон x
        """
        x_values = np.linspace(x_range[0], x_range[1], 500)
        y_values = [error_function.calculate_error(x) for x in x_values]
        dy_values = [error_function.calculate_derivative(x) for x in x_values]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # График 1: Функция
        ax1.plot(x_values, y_values, 'b-', linewidth=2, label='f(x)')
        ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax1.axvline(x=0, color='black', linestyle='-', alpha=0.3)
        ax1.set_title('Функция ошибки', fontsize=14)
        ax1.set_xlabel('x', fontsize=12)
        ax1.set_ylabel('f(x)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # График 2: Производная
        ax2.plot(x_values, dy_values, 'r-', linewidth=2, label="f'(x)")
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax2.axvline(x=0, color='black', linestyle='-', alpha=0.3)
        
        # Отмечаем точки, где производная = 0 (экстремумы)
        zero_crossings = []
        for i in range(1, len(dy_values)):
            if dy_values[i-1] * dy_values[i] < 0:
                zero_crossings.append(x_values[i])
        
        for x_zero in zero_crossings:
            ax2.scatter(x_zero, 0, color='green', s=50, zorder=5)
        
        ax2.set_title('Производная функции', fontsize=14)
        ax2.set_xlabel('x', fontsize=12)
        ax2.set_ylabel("f'(x)", fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig('reports/plots/derivative_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig