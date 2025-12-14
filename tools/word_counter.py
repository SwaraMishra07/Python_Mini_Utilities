""" A simple word counter tool that counts the number of words and characters in a given text. """
def count_words(text):
    words = text.strip().split()
    return len(words), len(text)


if __name__ == "__main__":
    text = input("Enter text: ")
    word_count, char_count = count_words(text)
    print(f"Words: {word_count}")
    print(f"Characters: {char_count}")

