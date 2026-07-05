"""
Модуль с алгоритмами оптимизации
"""

import math
import time
from src.error_function import ErrorFunction

class Optimizer:
    """Класс для оптимизации функции ошибки"""
    
    def __init__(self, error_function):
        """
        Инициализация оптимизатора
        
        Args:
            error_function: объект ErrorFunction
        """
        self.error_function = error_function
        self.history = []
        self.iteration = 0
    
    def gradient_descent(self, x0, learning_rate=0.1, max_iterations=50, tolerance=1e-6):
        """
        Метод градиентного спуска
        
        Args:
            x0: начальное значение параметра
            learning_rate: скорость обучения
            max_iterations: максимальное число итераций
            tolerance: порог остановки
            
        Returns:
            dict: результаты оптимизации
        """
        self.history = []
        self.iteration = 0
        x = x0
        
        start_time = time.time()
        
        for i in range(max_iterations):
            # Вычисляем значение функции и производной
            error = self.error_function.calculate_error(x)
            derivative = self.error_function.calculate_derivative(x)
            
            # Сохраняем историю
            self.history.append({
                'iteration': i + 1,
                'x': x,
                'error': error,
                'derivative': derivative,
                'learning_rate': learning_rate
            })
            
            # Проверка на остановку
            if abs(derivative) < tolerance:
                print(f"Остановка: производная близка к нулю (tolerance={tolerance})")
                break
            
            # Обновляем параметр
            x_new = x - learning_rate * derivative
            
            # Проверка на улучшение
            new_error = self.error_function.calculate_error(x_new)
            
            # Адаптивная скорость обучения (уменьшаем при перескоке)
            if new_error > error:
                learning_rate *= 0.5
                print(f"Скорость обучения уменьшена до {learning_rate:.6f}")
                continue
            
            x = x_new
            self.iteration += 1
        
        end_time = time.time()
        
        return {
            'final_parameter': x,
            'final_error': self.error_function.calculate_error(x),
            'iterations': self.iteration,
            'execution_time': end_time - start_time,
            'function_calls': self.error_function.function_calls,
            'derivative_calls': self.error_function.derivative_calls
        }
    
    def momentum_gradient_descent(self, x0, learning_rate=0.1, momentum=0.9, max_iterations=50):
        """
        Градиентный спуск с моментом (ускоренный)
        
        Args:
            x0: начальное значение
            learning_rate: скорость обучения
            momentum: коэффициент момента
            max_iterations: максимальное число итераций
        """
        self.history = []
        self.iteration = 0
        x = x0
        velocity = 0
        
        start_time = time.time()
        
        for i in range(max_iterations):
            error = self.error_function.calculate_error(x)
            derivative = self.error_function.calculate_derivative(x)
            
            # Сохраняем историю
            self.history.append({
                'iteration': i + 1,
                'x': x,
                'error': error,
                'derivative': derivative,
                'learning_rate': learning_rate
            })
            
            # Обновление с моментом
            velocity = momentum * velocity - learning_rate * derivative
            x_new = x + velocity
            
            # Проверка улучшения
            new_error = self.error_function.calculate_error(x_new)
            if new_error < error:
                x = x_new
                self.iteration += 1
            else:
                # Уменьшаем скорость обучения при перескоке
                learning_rate *= 0.5
                velocity = 0
                
            if self.iteration >= max_iterations:
                break
        
        end_time = time.time()
        
        return {
            'final_parameter': x,
            'final_error': self.error_function.calculate_error(x),
            'iterations': self.iteration,
            'execution_time': end_time - start_time,
            'function_calls': self.error_function.function_calls,
            'derivative_calls': self.error_function.derivative_calls
        }
    
    def get_history(self):
        """Возвращает историю оптимизации"""
        return self.history