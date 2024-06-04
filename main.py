import exponential
import count_numbers
import count_words
import find_comma
import find_longest_y
import list_operations
import count_lowercase
text_to_analyze = "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."

def task1():
    while True:
        try:
            x = float(input("Введите x: "))
            break
        except ValueError:
            print("ввод неверен")

    print("Вы ввели:", x)
    # Calling the function and printing the result
    print("e^{} = {:.10f}".format(x, exponential.e_to_the_x(x)))
def task2():
    result = count_numbers.count_non_negative_numbers()
    print("Number of non-negative numbers:", result)

def task3():
    result = count_lowercase.count_lowercase()

def task4():
    result = count_words.count_min_length_words(text_to_analyze)
    print("Number of words with minimum length:", result)

    result = find_comma.find_comma_followed_words(text_to_analyze)
    print("Words followed by a comma:", result)

    result = find_longest_y.find_longest_y_word(text_to_analyze)
    print("Longest word ending with 'y':", result)

def task5():
    # Input the list of floating-point numbers from the user
    my_list = list_operations.input_float_list()
    # Print the list
    list_operations.print_list(my_list)

    # Find the maximum absolute value
    max_abs_value = list_operations.find_max_abs_value(my_list)
    print("Maximum absolute value in the list:", max_abs_value)

    # Find the sum of elements between the first and second positive elements
    sum_between = list_operations.sum_between_positive(my_list)
    print("Sum of elements between the first and second positive elements:", sum_between)


def menu():
    while True:
        print("Выберите задачу для выполнения:")
        print("task1: Вычисление экспоненты")
        print("task2: Подсчет неотрицательных чисел")
        print("task3: Подсчитать количество слов, начинающихся со строчной буквы")
        print("task4: Определить, сколько слов имеют минимальную длину; вывести все слова, за которыми следует запятая; найти самое длинное слово, которое заканчивается на 'y'")
        print("task5: Найти максимальный по модулю элемент списка и сумму элементов списка, расположенных между первым и вторым положительными элементами")
        choice = input("Введите номер задачи (для выхода введите 'escape'): ")

        if choice == 'escape':
            break
        elif choice == '1':
            task1()
        elif choice == '2':
            task2()
        elif choice == '3':
            task3()
        elif choice == '4':
            task4()
        elif choice == '5':
            task5()
        else:
            print("Ошибка: неверный выбор")


# Вызов функции меню
menu()
