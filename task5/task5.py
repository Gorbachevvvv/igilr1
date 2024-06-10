import numpy as np
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from LR4.task import Task

class Matrix:
    def __init__(self, data):
        self.data = np.array(data)

    def sort_last_row(self):
        self.data[-1] = np.sort(self.data[-1])

    def get_last_row(self):
        return self.data[-1]

    def compute_median(self):
        # Медиана через стандартную функцию
        median_std = np.median(self.data[-1])

        # Медиана через программирование формулы
        sorted_row = np.sort(self.data[-1])
        n = len(sorted_row)
        if n % 2 == 1:
            median_formula = sorted_row[n // 2]
        else:
            median_formula = (sorted_row[n // 2 - 1] + sorted_row[n // 2]) / 2

        return median_std, median_formula


class Task5(Task):
    """
    A class representing Task 5.
    Inherits from Task class.
    """
    @staticmethod
    def complete_task():
        while True:
            try:
                # Запрос у пользователя количества строк и столбцов
                rows = int(input("Введите количество строк: "))
                cols = int(input("Введите количество столбцов: "))

                # Создание матрицы с случайными целочисленными значениями
                data = np.random.randint(0, 100, size=(rows, cols))

                # Создание объекта матрицы
                matrix = Matrix(data)

                print("\033[37m\033[1m--------------------------------\033[00m")
                print("\033[37m\033[1mЗадание варианта:\033[00m")
                print("\033[37m\033[1m--------------------------------\033[00m")
                print("Исходная матрица:")
                print(matrix.data)

                # Сортировка последней строки матрицы
                matrix.sort_last_row()
                print("Матрица с отсортированной последней строкой:")
                print(matrix.data)

                # Получение последней строки матрицы
                last_row = matrix.get_last_row()
                print("\nПоследняя строка матрицы:", last_row)

                # Вычисление медианы
                median_std, median_formula = matrix.compute_median()
                print("\nМедиана (стандартная функция):", median_std)
                print("Медиана (программирование формулы):", median_formula)

                # Примеры операций с массивами NumPy и математических/статистических функций:
                arr1 = np.array([[1, 2, 3], [4, 5, 6]])

                print("\033[37m\033[1m--------------------------------\033[00m")
                print("\033[37m\033[1mПримеры операций с массивами NumPy и математических/статистических функций:\033[00m")
                # 1. Создание массива. Функции array() и values().
                print("\033[37m\033[1m--------------------------------\033[00m")
                print("\033[37m\033[1m1. Создание массива. Функции array() и values():\033[00m")
                print("Исходный массив:\n", arr1)
                print("Массив через array():\n", np.array(arr1))
                print("Массив через values():\n", arr1)

                # 2. Функции создания массива заданного вида.
                print("\n\033[37m\033[1m2. Функции создания массива заданного вида:\033[00m")
                print("Массив из нулей:\n", np.zeros((2, 3)))
                print("Массив из единиц:\n", np.ones((2, 3)))
                print("Массив из заданного числа:\n", np.full((2, 3), 5))

                # 3. Индексирование массивов NumPy. Индекс и срез.
                print("\n\033[37m\033[1m3. Индексирование массивов NumPy. Индекс и срез:\033[00m")
                print("Элемент с индексом (1, 1): ", arr1[1, 1])
                print("Первая строка: ", arr1[0])
                print("Второй столбец: ", arr1[:, 1])
                print("Срез массива:\n", arr1[:, :2])

                # 4. Операции с массивами. Универсальные (поэлементные) функции.
                print("\n\033[37m\033[1m4. Операции с массивами. Универсальные (поэлементные) функции:\033[00m")
                print("Сложение:\n", arr1 + 1)
                print("Вычитание:\n", arr1 - 1)
                print("Умножение:\n", arr1 * 2)
                print("Деление:\n", arr1 / 2)
                print("Возведение в степень:\n", np.power(arr1, 2))
                print("Абсолютное значение:\n", np.abs(arr1))
                print("Синус:\n", np.sin(arr1))

                # Примеры других операций:
                print("\n\033[37m\033[1mПримеры других операций:\033[00m")
                # Среднее значение всех элементов массива
                mean_value = np.mean(arr1)
                # Коэффициент корреляции между двумя массивами
                corr_matrix = np.corrcoef(arr1, np.array([[2, 4, 6], [3, 5, 7]]))
                # Дисперсия значений массива
                variance_value = np.var(arr1)
                # Стандартное отклонение значений массива
                std_deviation = np.std(arr1)

                print("Среднее значение:", mean_value)
                print("Корреляционная матрица:\n", corr_matrix)
                print("Дисперсия:", variance_value)
                print("Стандартное отклонение:", std_deviation)
                return
            except ValueError:
                print("Wrong input")

# Task5.complete_task()
