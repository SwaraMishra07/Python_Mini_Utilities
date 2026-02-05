import sys

def count_words(text):
    """
    Counts the number of words and characters
    after cleaning extra spaces and newlines.
    """

    # Normalize whitespace (handles multi-line input)
    cleaned_text = " ".join(text.split())

    # Handle empty input
    if not cleaned_text:
        return 0, 0

    words = cleaned_text.split()
    character_count = len(cleaned_text)

    return len(words), character_count


if __name__ == "__main__":
    print("Enter text (Ctrl+D on Linux/macOS, Ctrl+Z then Enter on Windows):")

    # Read multi-paragraph input
    text = sys.stdin.read()

    word_count, char_count = count_words(text)

    if word_count == 0:
        print("❌ No input provided. Please enter valid input.")
    else:
        print(f"Words: {word_count}")
        print(f"Characters (excluding extra spaces): {char_count}")


