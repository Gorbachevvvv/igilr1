import math
import matplotlib.pyplot as plt
import numpy as np
from statistics import median, mode
import zipfile
import os
import sys


class AttributesCalculator:
    @staticmethod
    def calculate_dispersion(series):
        """Calculates the dispersion of a series."""
        average = sum(series) / len(series)
        elements_sum = sum(i * i for i in series)
        return elements_sum / len(series) - average ** 2


class Series:
    def __init__(self, x, eps):
        """Initializes Series object."""
        self._x = x
        self._eps = eps
        self._attribute_calculator = AttributesCalculator()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def eps(self):
        return self._eps

    @eps.setter
    def eps(self, value):
        self._eps = value

    def calculate_series(self):
        """Function to calculate Taylor series approximation."""
        series = []
        result = 1.0  # Start with the first term of the series (x^0 / 0!)
        n = 0
        term = 1.0  # First term (x^0 / 0!)

        while abs(term) > self._eps and n < 500:
            n += 1
            term = (self._x ** n) / math.factorial(n)
            result += term
            series.append(result)

        if n >= 500:
            print("Iterations > 500")

        print("\033[37m\033[1m----------------------------\033[00m")
        print("\033[37m\033[1mThe result:")
        print("----------------------------\033[00m")
        print(
            f"x = {self._x}, n = {n}, F(x) = {round(result, 10)}, Math F(x) = {round(math.exp(self._x), 10)}, eps = {self._eps}")
        print("\033[37m\033[1m----------------------------\033[00m")
        print("\033[37m\033[1mAdditional parameters:")
        print("----------------------------\033[00m")
        print(f"Arithmetic mean of sequence elements: {round(sum(series) / len(series), 10)}")
        print(f"Median of sequence elements: {median(series)}")
        try:
            print(f"Mode of sequence elements: {mode(series)}")
        except:
            print("Mode of sequence elements: No unique mode")
        dispersion = self._attribute_calculator.calculate_dispersion(series)
        print(f"Dispersion of sequence elements: {dispersion}")
        print(f"Sequence standard deviation: {math.sqrt(dispersion)}")

        return series, n


class PlotDrawer:
    def __init__(self, series, n, x_value):
        """Initializes PlotDrawer object."""
        self._series = series
        self._n = n
        self._x_value = x_value

    @property
    def series(self):
        return self._series

    @series.setter
    def series(self, value):
        self._series = value

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, value):
        self._n = value

    @property
    def x_value(self):
        return self._x_value

    @x_value.setter
    def x_value(self, value):
        self._x_value = value

    def show_plot(self):
        """Displays the plot of the function decomposition into a series."""
        x = np.linspace(-0.5, 2, 100)
        y1 = np.exp(x)
        y2 = [sum((xi ** i) / math.factorial(i) for i in range(self._n + 1)) for xi in x]

        plt.plot(x, y1, label='exp(x)', color='blue', linewidth=2)
        plt.plot(x, y2, label='Taylor Series', color='orange', linewidth=2)

        plt.legend()
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Comparison of exp(x) and its Taylor Series Approximation')
        plt.annotate(f'Approximation at x={self._x_value}', xy=(self._x_value, np.exp(self._x_value)),
                     xytext=(self._x_value + 0.5, np.exp(self._x_value) + 1),
                     arrowprops=dict(facecolor='black', shrink=0.05))
        plt.grid(True)

        figure = plt.gcf()
        figure.set_size_inches(10, 5)
        plt.savefig('task3/plots.png', dpi=100)
        plt.show()

    def save_plot(self, filename='task3/plots.png'):
        """Saves the plot to a file."""
        x = np.linspace(-0.5, 2, 100)
        y1 = np.exp(x)
        y2 = [sum((xi ** i) / math.factorial(i) for i in range(self._n + 1)) for xi in x]

        plt.plot(x, y1, label='exp(x)', color='blue', linewidth=2)
        plt.plot(x, y2, label='Taylor Series', color='orange', linewidth=2)

        plt.legend()
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Comparison of exp(x) and its Taylor Series Approximation')
        plt.annotate(f'Approximation at x={self._x_value}', xy=(self._x_value, np.exp(self._x_value)),
                     xytext=(self._x_value + 0.5, np.exp(self._x_value) + 1),
                     arrowprops=dict(facecolor='black', shrink=0.05))
        plt.grid(True)

        figure = plt.gcf()
        figure.set_size_inches(10, 5)
        plt.savefig(filename, dpi=100)


class Task3:
    """A class representing Task 3."""

    @staticmethod
    def complete_task():
        """Function to get input from the user and complete the task."""
        while True:
            try:
                x = float(input("Enter x value for decomposing the function into a Taylor series: "))
                eps = float(input("Enter eps value of the calculation accuracy: "))
                series = Series(x, eps)
                series_list, n = series.calculate_series()

                series_plot = PlotDrawer(series_list, n, x)
                series_plot.show_plot()
                series_plot.save_plot()
                Task3.archive_results()
                return
            except ValueError:
                print("Wrong input")

    @staticmethod
    def archive_results():
        """Archives the results file into a ZIP archive."""
        with zipfile.ZipFile('task3/results.zip', 'w') as z:
            z.write('task3/plots.png')


# Create directory for saving plots
os.makedirs('task3', exist_ok=True)


