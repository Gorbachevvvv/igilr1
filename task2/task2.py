import re
import zipfile
import os


class TextAnalyzer:
    """A class for analyzing text files."""

    def __init__(self, filename):
        """Initializes the TextAnalyzer object."""
        self.filename = filename

    def read_text_from_file(self):
        """Reads the content of the text file."""
        with open(self.filename, 'r') as file:
            self.text = file.read()

    def count_sentences(self):
        """Counts the number of sentences in the text."""
        return len(re.findall(r'[.!?]', self.text))

    def count_sentence_types(self):
        """Counts the number of different types of sentences."""
        narrative = len(re.findall(r'[^.!?]*\.', self.text))
        interrogative = len(re.findall(r'[^.!?]*\?', self.text))
        imperative = len(re.findall(r'[^.!?]*!', self.text))
        return narrative, interrogative, imperative

    def average_sentence_length(self):
        """Calculates the average length of sentences."""
        sentences = re.findall(r'[^.!?]*[.!?]', self.text)
        words_per_sentence = [len(re.findall(r'\b\w+\b', sentence)) for sentence in sentences]
        return sum(words_per_sentence) / len(words_per_sentence)

    def average_word_length(self):
        """Calculates the average length of words."""
        words = re.findall(r'\b\w+\b', self.text)
        return sum(len(word) for word in words) / len(words)

    def count_smileys(self):
        """Counts the number of smiley faces in the text."""
        smiley_pattern = re.compile(r'[;:]-*[\(\[\]\)]+')
        smileys = re.findall(smiley_pattern, self.text)
        return len(smileys)

    def find_words_lowercase_punctuations(self):
        """Finds all words starting with a lowercase letter and all punctuations."""
        words = re.findall(r'\b[a-z]\w*\b', self.text)
        punctuations = re.findall(r'[^\w\s]', self.text)
        return words, punctuations

    def is_valid_mac_address(self):
        """Determines if a given string is a valid MAC address."""
        mac_pattern = re.compile(r'^([0-9]{2}:){5}[0-9A-Fa-f]{2}$')
        temp = self.text.split('\n')
        a = []
        for _ in temp:
            a.append(bool(re.match(mac_pattern, _)))
        print(a)
        return a

    def count_words(self):
        """Counts the number of words in the text."""
        words = re.findall(r'\b\w+\b', self.text)
        return len(words)

    def find_longest_word_and_position(self):
        """Finds the longest word in the text and its position."""
        words = re.findall(r'\b\w+\b', self.text)
        max_word = max(words, key=len)
        max_index = words.index(max_word) + 1
        return max_word, max_index

    def find_odd_words(self):
        """Finds words at odd positions in the text."""
        words = re.findall(r'\b\w+\b', self.text)
        odd_words = [word for idx, word in enumerate(words, start=1) if idx % 2 != 0]
        return odd_words

    def save_results(self, filename):
        """Saves analysis results to a text file."""
        with open(filename, 'w') as f:
            f.write(f"Number of sentences: {self.count_sentences()}\n")
            narrative, interrogative, imperative = self.count_sentence_types()
            f.write(f"Number of narrative sentences: {narrative}\n")
            f.write(f"Number of interrogative sentences: {interrogative}\n")
            f.write(f"Number of imperative sentences: {imperative}\n")
            f.write(f"Average sentence length: {self.average_sentence_length():.2f}\n")
            f.write(f"Average word length: {self.average_word_length():.2f}\n")
            f.write(f"Number of smileys: {self.count_smileys()}\n")
            words, punctuations = self.find_words_lowercase_punctuations()
            f.write(f"Words starting with lowercase: {words}\n")
            f.write(f"Punctuations: {punctuations}\n")
            longest_word, position = self.find_longest_word_and_position()
            f.write(f"Longest word: {longest_word}, Position: {position}\n")
            f.write(f"Odd words: {self.find_odd_words()}\n")
            f.write(f"Is correct: {self.is_valid_mac_address()}\n")

    def archive_results(self, filename):
        """Archives the results file into a ZIP archive."""
        with zipfile.ZipFile(filename, 'w') as z:
            z.write("task2/results.txt")

    def print_results(self):
        """Prints the analysis results to the console."""
        print(f"Number of sentences: {self.count_sentences()}")
        narrative, interrogative, imperative = self.count_sentence_types()
        print(f"Number of narrative sentences: {narrative}")
        print(f"Number of interrogative sentences: {interrogative}")
        print(f"Number of imperative sentences: {imperative}")
        print(f"Average sentence length: {self.average_sentence_length():.2f}")
        print(f"Average word length: {self.average_word_length():.2f}")
        print(f"Number of smileys: {self.count_smileys()}")
        words, punctuations = self.find_words_lowercase_punctuations()
        print(f"Words starting with lowercase: {words}")
        print(f"Punctuations: {punctuations}")
        longest_word, position = self.find_longest_word_and_position()
        print(f"Longest word: {longest_word}, Position: {position}")
        print(f"Odd words: {self.find_odd_words()}")
        # print(f"Is correct: {self.is_valid_mac_address(mac)}")


class Task2:
    """A class representing Task 2."""

    @staticmethod
    def complete_task():
        """Completes Task 2 by analyzing text data, printing results, saving results to a file, and archiving the results file."""
        filename = "task2/input.txt"

        analyzer = TextAnalyzer(filename)
        analyzer.read_text_from_file()
        analyzer.print_results()
        analyzer.save_results("task2/results.txt")
        analyzer.archive_results("task2/results.zip")
