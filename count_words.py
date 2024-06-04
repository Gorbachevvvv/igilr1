def count_min_length_words(text):
    words = text.split()
    min_length = min(len(word) for word in words)
    return sum(1 for word in words if len(word) == min_length)
