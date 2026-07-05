"""
Модуль для работы с функцией ошибки и её производными
"""

import numpy as np
import math

class ErrorFunction:
    """Класс для работы с функцией ошибки модели"""
    
    def __init__(self, function_type='quadratic'):
        """
        Инициализация функции ошибки
        
        Args:
            function_type: тип функции ('quadratic', 'sine', 'complex')
        """
        self.function_type = function_type
        self.function_calls = 0
        self.derivative_calls = 0
        
    def calculate_error(self, x):
        """
        Вычисление значения функции ошибки
        
        Args:
            x: значение параметра
            
        Returns:
            float: значение ошибки
        """
        self.function_calls += 1
        
        if self.function_type == 'quadratic':
            # f(x) = (x - 3)² + 2 - простая парабола с минимумом в x=3
            return (x - 3) ** 2 + 2
            
        elif self.function_type == 'sine':
            # f(x) = sin(x) + 0.1*x² - более сложная функция
            return math.sin(x) + 0.1 * x ** 2
            
        elif self.function_type == 'complex':
            # f(x) = (x-2)² * (x+1)² + 0.5*sin(2*x) - сложная функция с несколькими минимумами
            return (x - 2) ** 2 * (x + 1) ** 2 + 0.5 * math.sin(2 * x)
            
        elif self.function_type == 'exponential':
            # f(x) = exp(-0.5*x) + x²/10 - экспоненциальная функция
            return math.exp(-0.5 * x) + x ** 2 / 10
            
        else:
            raise ValueError(f"Неизвестный тип функции: {self.function_type}")
    
    def calculate_derivative(self, x, method='analytical'):
        """
        Вычисление производной функции ошибки
        
        Args:
            x: значение параметра
            method: метод вычисления ('analytical', 'numerical')
            
        Returns:
            float: значение производной
        """
        self.derivative_calls += 1
        
        if method == 'analytical':
            # Аналитическая производная
            if self.function_type == 'quadratic':
                # f'(x) = 2*(x-3)
                return 2 * (x - 3)
                
            elif self.function_type == 'sine':
                # f'(x) = cos(x) + 0.2*x
                return math.cos(x) + 0.2 * x
                
            elif self.function_type == 'complex':
                # f'(x) = 2*(x-2)*(x+1)² + 2*(x-2)²*(x+1) + cos(2*x)
                # Упрощенная производная для демонстрации
                return 2 * (x - 2) * (x + 1) ** 2 + 2 * (x - 2) ** 2 * (x + 1) + math.cos(2 * x)
                
            elif self.function_type == 'exponential':
                # f'(x) = -0.5*exp(-0.5*x) + x/5
                return -0.5 * math.exp(-0.5 * x) + x / 5
                
        else:
            # Численная производная (метод конечных разностей)
            h = 1e-7
            return (self.calculate_error(x + h) - self.calculate_error(x - h)) / (2 * h)
    
    def get_function_info(self):
        """Возвращает информацию о функции"""
        info = {
            'quadratic': {
                'name': 'Квадратичная функция',
                'formula': 'f(x) = (x-3)² + 2',
                'minimum': 3.0,
                'min_value': 2.0
            },
            'sine': {
                'name': 'Синусоидальная функция',
                'formula': 'f(x) = sin(x) + 0.1x²',
                'minimum': -0.5,
                'min_value': 0.0
            },
            'complex': {
                'name': 'Сложная функция',
                'formula': 'f(x) = (x-2)²(x+1)² + 0.5sin(2x)',
                'minimum': 0.5,
                'min_value': 0.0
            },
            'exponential': {
                'name': 'Экспоненциальная функция',
                'formula': 'f(x) = e^(-0.5x) + x²/10',
                'minimum': 1.0,
                'min_value': 0.0
            }
        }
        return info.get(self.function_type, info['quadratic'])
    
    def reset_counters(self):
        """Сброс счетчиков вызовов"""
        self.function_calls = 0
        self.derivative_calls = 0