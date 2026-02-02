def count_words(text):
    """
    Counts the number of words and characters (excluding extra spaces)
    in the given text.
    """

    # Handle empty input
    if not text.strip():
        return 0, 0

    # Clean text: remove leading/trailing spaces
    cleaned_text = text.strip()

    # Count words
    words = cleaned_text.split()

    # Count characters (excluding extra spaces at start/end)
    character_count = len(cleaned_text)

    return len(words), character_count


if __name__ == "__main__":
    text = input("Enter text: ")

    word_count, char_count = count_words(text)

    print(f"Words: {word_count}")
    print(f"Characters (excluding extra spaces): {char_count}")
