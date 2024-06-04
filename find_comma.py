def find_comma_followed_words(text):
    words = text.split()
    return [word for word in words if word.endswith(',') and len(word) > 1]
