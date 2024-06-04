import random

def input_float_list():
    choice = input("Выберите метод ввода ('1' для ввода вручную, '2' для случайного ввода): ")

    if choice == '1':
        while True:
            try:
                elements = input("Введите числа с плавающей запятой, разделенные пробелами: ").split()
                float_list = [float(element) for element in elements]
                return float_list
            except ValueError:
                print("Ошибка: Пожалуйста, введите только числа с плавающей запятой!")

    elif choice == '2':
        size = int(input("Введите размер списка: "))
        float_list = [random.uniform(-100, 100) for _ in range(size)]
        return float_list

    else:
        print("Неверный выбор. Пожалуйста, введите '1' или '2'.")

def find_max_abs_value(float_list):
    return max(float_list, key=abs)

def sum_between_positive(float_list):
    first_positive_index = None
    second_positive_index = None

    for i, num in enumerate(float_list):
        if num > 0:
            if first_positive_index is None:
                first_positive_index = i
            elif second_positive_index is None:
                second_positive_index = i
                break

    if second_positive_index is None:
        return 0

    sum_between = sum(float_list[first_positive_index + 1:second_positive_index])
    return sum_between

def print_list(float_list):
    print("Список чисел с плавающей запятой:", float_list)

def task5():
    my_list = input_float_list()
    print_list(my_list)

    max_abs_value = find_max_abs_value(my_list)
    print("Максимальное абсолютное значение в списке:", max_abs_value)

    sum_between = sum_between_positive(my_list)
    print("Сумма элементов между первым и вторым положительными элементами:", sum_between)

