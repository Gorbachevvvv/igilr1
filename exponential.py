def e_to_the_x(x, terms=10):
    result = 0  # Starting from zero
    factorial = 1  # Starting from one
    for n in range(terms):  # Repeating a certain number of times
        result += x ** n / factorial  # Adding a small part of the number to the result
        factorial *= (n + 1)  # Increasing the factorial at each step
    return result
