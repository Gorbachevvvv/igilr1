import numpy as np
import matplotlib.pyplot as plt
import math
import sys
import os
from abc import ABC, abstractmethod

# Adding the current and parent directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from LR4.task import Task

class LoggingMixin:
    '''A mixin class for logging messages.'''
    def log(self, message):
        print(f"[LOG]: {message}")

# Task4 class inherits from Task (Inheritance)
class Task4(Task):
    """
    A class representing Task 4.
    Inherits from Task class.
    """
    @staticmethod
    def complete_task():
        '''Completes the task of creating and plotting a triangle.'''
        while True:
            try:
                a = float(input('Enter the length of the triangle side a: '))
                B = float(input('Enter the angle B in degrees: '))
                C = float(input('Enter the angle C in degrees: '))
                color = input('Enter the color of the triangle: ')
                name = input('Enter the name of the triangle: ')

                # Creating an instance of LoggingTriangle (Inheritance and mixin usage)
                triangle = LoggingTriangle(a, B, C, name, color)
                triangle.print_attributes()

                # Creating an instance of LoggingTriangleDrawer (Inheritance and mixin usage)
                triangle_drawer = LoggingTriangleDrawer(triangle)
                triangle_drawer.plot_triangle()
                return
            except ValueError:
                print("Wrong input")

class Triangle:
    '''A class representing a triangle.'''
    def __init__(self, a, B, C, name, color):
        '''Initializes a triangle with a given side and angles.'''
        self._a = a
        self._B = np.deg2rad(B)
        self._C = np.deg2rad(C)
        self._name = name
        self._color = color

    def calculate_coordinates(self):
        '''Calculates the coordinates of the vertices of the triangle.'''
        A = (0, 0)
        B = (self._a, 0)
        Cx = self._a - (self._a * math.cos(self._B))
        Cy = self._a * math.sin(self._B) / math.sin(self._B + self._C)
        C = (Cx, Cy)
        return np.array([A, B, C])

    def print_attributes(self):
        '''Prints attributes of the triangle.'''
        print('\033[37m\033[1mTriangle side a: {}, angle B: {}, angle C: {}, color: {}'.format(
            self._a, np.rad2deg(self._B), np.rad2deg(self._C), self._color))
        print("\033[00m")

# LoggingTriangle class inherits from Triangle and LoggingMixin (Multiple inheritance)
class LoggingTriangle(Triangle, LoggingMixin):
    '''A triangle class with logging capabilities.'''
    def __init__(self, a, B, C, name, color):
        # Using super() to call the initializer of the parent class Triangle
        super().__init__(a, B, C, name, color)
        self.log("Triangle created")

    def calculate_coordinates(self):
        '''Calculates the coordinates and logs the action.'''
        coordinates = super().calculate_coordinates()
        self.log("Coordinates calculated")
        return coordinates

    def print_attributes(self):
        '''Prints attributes and logs the action.'''
        super().print_attributes()
        self.log("Attributes printed")

class TriangleDrawer:
    '''A class responsible for drawing triangles.'''
    def __init__(self, triangle: Triangle):
        '''Initializes a TriangleDrawer with a given triangle.'''
        self._triangle = triangle

    def plot_triangle(self):
        '''Plots the triangle using matplotlib.'''
        coordinates = self._triangle.calculate_coordinates()
        A, B, C = coordinates

        plt.plot([A[0], B[0]], [A[1], B[1]], color=self._triangle._color)
        plt.plot([B[0], C[0]], [B[1], C[1]], color=self._triangle._color)
        plt.plot([C[0], A[0]], [C[1], A[1]], color=self._triangle._color)

        plt.fill([A[0], B[0], C[0]], [A[1], B[1], C[1]], self._triangle._color, alpha=0.3)

        plt.axis('equal')
        plt.xlabel('X')
        plt.ylabel('Y')

        plt.title(self._triangle._name, color=self._triangle._color, fontsize=20)
        figure = plt.gcf()
        figure.set_size_inches(10, 5)
        plt.savefig(r'task_triangle\triangle_plot.png', dpi=100)
        plt.show()

# LoggingTriangleDrawer class inherits from TriangleDrawer and LoggingMixin (Multiple inheritance)
class LoggingTriangleDrawer(TriangleDrawer, LoggingMixin):
    '''A triangle drawer class with logging capabilities.'''
    def __init__(self, triangle: LoggingTriangle):
        # Using super() to call the initializer of the parent class TriangleDrawer
        super().__init__(triangle)
        self.log("TriangleDrawer created")

    def plot_triangle(self):
        '''Plots the triangle and logs the action.'''
        super().plot_triangle()
        self.log("Triangle plotted")

# Ensure the directory for saving the plot exists
os.makedirs('task_triangle', exist_ok=True)
