def find_longest_y_word(text):
    words = text.split()
    y_words = [word for word in words if word.endswith('y')]
    if y_words:
        return max(y_words, key=len)
    else:
        return None
