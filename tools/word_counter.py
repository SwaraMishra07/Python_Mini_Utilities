
"""
tools.word_counter

This module provides a function to count the number of words and
characters in a given text string entered by the user.

"""


def count_words(text):
    """
    Count the number of words and characters in a given text string.

    The function removes leading and trailing whitespace using strip()
    and splits the text into words using split(), which separates the
    string based on any sequence of whitespace characters.

    Parameters:
        text (str): The input text string.

    Returns:
        tuple:
            - int: Number of words in the text.
            - int: Total number of characters in the text, including spaces.
    """
    
   
    words = text.strip().split()
    return len(words), len(text)


if __name__ == "__main__":
    """
    This takes a string data type input from the user and counts words and characters
    """
    text = input("Enter text: ")
    word_count, char_count = count_words(text)
    print(f"Words: {word_count}")
    print(f"Characters: {char_count}")

