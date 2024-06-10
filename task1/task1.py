import csv
import pickle

class Teacher:
    """Represents a teacher with surname, class, and hours attributes."""

    def __init__(self, surname, class_assigned, hours):
        """Initializes a Teacher object with the given attributes."""
        self.surname = surname
        self.class_assigned = class_assigned
        self.hours = hours

    def __repr__(self):
        """Returns a string representation of the Teacher object."""
        return f"{self.surname}, Class: {self.class_assigned}, Hours: {self.hours}"


class School:
    """Represents a school with a collection of teachers."""

    def __init__(self):
        """Initializes a School object with an empty dictionary of teachers."""
        self.teachers = {}

    def add_teacher(self, teacher_id, teacher):
        """Adds a teacher to the school."""
        self.teachers[teacher_id] = teacher

    def teacher_load(self, surname):
        """Retrieves the load of a teacher by surname."""
        for teacher in self.teachers.values():
            if teacher.surname == surname:
                return teacher.hours
        return None

    def highest_load(self):
        """Determines which teacher has the highest load."""
        if not self.teachers:
            return None
        return max(self.teachers.values(), key=lambda teacher: teacher.hours)

    def lowest_load(self):
        """Determines which teacher has the lowest load."""
        if not self.teachers:
            return None
        return min(self.teachers.values(), key=lambda teacher: teacher.hours)

    def save_to_csv(self, filename):
        """Saves the school's teacher data to a CSV file."""
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for teacher_id, teacher in self.teachers.items():
                writer.writerow([teacher_id, teacher.surname, teacher.class_assigned, teacher.hours])

    def load_from_csv(self, filename):
        """Loads teacher data from a CSV file into the school."""
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                teacher_id, surname, class_assigned, hours = row
                self.add_teacher(teacher_id, Teacher(surname, class_assigned, int(hours)))

    def save_to_pickle(self, filename):
        """Saves the school's teacher data to a pickle file."""
        with open(filename, 'wb') as file:
            pickle.dump(self.teachers, file)

    def load_from_pickle(self, filename):
        """Loads teacher data from a pickle file into the school."""
        with open(filename, 'rb') as file:
            self.teachers = pickle.load(file)


class Task1:
    """Represents the main task for handling school management."""

    @staticmethod
    def complete_task():
        """Completes the task of managing school workload for teachers."""
        school = School()
        school.add_teacher(1, Teacher("Ivanov", "5A", 20))
        school.add_teacher(2, Teacher("Petrov", "6B", 15))
        school.add_teacher(3, Teacher("Sidorov", "7C", 25))
        school.add_teacher(4, Teacher("Gorbachev", "8D", 10))
        school.add_teacher(5, Teacher("Guseva", "9E", 30))

        # Saving to CSV and pickle files
        school.save_to_csv("task1/teachers.csv")
        school.save_to_pickle("task1/teachers.pickle")

        # Creating a new School object and loading data from files
        new_school = School()
        new_school.load_from_csv("task1/teachers.csv")
        print(new_school.teachers)

        new_school.load_from_pickle("task1/teachers.pickle")
        print(new_school.teachers)

        # Taking surname of the teacher from the keyboard
        surname = input("Enter the surname of the teacher: ")
        load = new_school.teacher_load(surname)
        if load is not None:
            print(f"{surname} has a load of {load} hours.")
        else:
            print(f"Teacher with surname {surname} not found.")

        # Determining the teachers with the highest and lowest load
        highest_load_teacher = new_school.highest_load()
        lowest_load_teacher = new_school.lowest_load()

        print(f"The teacher with the highest load is {highest_load_teacher.surname} with {highest_load_teacher.hours} hours.")
        print(f"The teacher with the lowest load is {lowest_load_teacher.surname} with {lowest_load_teacher.hours} hours.")


# Execute the task

