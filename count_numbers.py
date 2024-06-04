def count_non_negative_numbers():
    count = 0  # Initialize count of non-negative numbers
    while True:  # Run an infinite loop
        while True:
            try:
                num = int(input("введите x: "))
                break  # Прерываем цикл, если ввод корректен
            except ValueError:
                print("неверный ввод")

        print("Вы ввели:", num)  # Take input from the user
        if num < 100:  # Check if the entered number is less than 100
            break  # If the number is less than 100, exit the loop
        if num >= 0:  # Check if the entered number is non-negative
            count += 1  # Increment count if the number is non-negative
    return count
