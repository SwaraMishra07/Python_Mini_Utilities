def count_words(text):
    """
    Counts the number of words and characters in the given text.

    Parameters:
        text (str): The input string provided by the user.

    Returns:
        tuple: A tuple containing:
            - int: Number of words in the text
            - int: Number of characters in the text
    """
    # Remove leading/trailing whitespace and split text into words
    words = text.strip().split()

    # Return word count and character count
    return len(words), len(text)


if __name__ == "__main__":
    # Take input from the user
    text = input("Enter text: ")

    # Get word count and character count
    word_count, char_count = count_words(text)

    # Display the results
    print(f"Words: {word_count}")
    print(f"Characters: {char_count}")
