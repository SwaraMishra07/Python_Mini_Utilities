#!/usr/bin/env python3
"""
CAPTCHA Generator Tool
Generates random text-based CAPTCHAs with customizable difficulty.
"""

import random
import string
import sys
from datetime import datetime


class CaptchaGenerator:
    """Generate text-based CAPTCHAs for verification purposes."""

    def __init__(self):
        """Initialize the CAPTCHA generator."""
        self.easy_chars = string.digits
        self.medium_chars = string.ascii_uppercase + string.digits
        self.hard_chars = string.ascii_letters + string.digits

        self.easy_patterns = [
            "{}{}{}{}",  # 4 digits
            "{}{}{}{}{}",  # 5 digits
        ]

        self.medium_patterns = [
            "{}{}{}",  # 3 alphanum
            "{}{}{}{}",  # 4 alphanum
            "{}{}{}{}{}",  # 5 alphanum
        ]

        self.hard_patterns = [
            "{}{}{}{}{}",  # 5 mixed
            "{}{}{}{}{}{}",  # 6 mixed
            "{}{}{}{}{}{}{}",  # 7 mixed
        ]

    def generate_captcha(self, difficulty="medium", length=None):
        """
        Generate a CAPTCHA string.

        Args:
            difficulty (str): 'easy', 'medium', or 'hard'
            length (int, optional): Specific length for CAPTCHA

        Returns:
            tuple: (captcha_text, display_format)
        """
        if difficulty == "easy":
            chars = self.easy_chars
            if length is None:
                length = random.randint(4, 5)
        elif difficulty == "medium":
            chars = self.medium_chars
            if length is None:
                length = random.randint(4, 5)
        else:  # hard
            chars = self.hard_chars
            if length is None:
                length = random.randint(5, 7)

        captcha = "".join(random.choice(chars) for _ in range(length))
        display = self._format_captcha(captcha, difficulty)

        return captcha, display

    def _format_captcha(self, captcha, difficulty):
        """
        Format CAPTCHA for display.

        Args:
            captcha (str): The CAPTCHA text
            difficulty (str): The difficulty level

        Returns:
            str: Formatted CAPTCHA for display
        """
        # Add visual distortion using ASCII art style
        separator = random.choice(["-", "_", ".", "~"])

        if difficulty == "easy":
            # Simple spaced format
            formatted = separator.join(captcha)
        elif difficulty == "medium":
            # Add some visual noise
            noise = random.choice(["*", "#", "@", "+"])
            parts = list(captcha)
            formatted = separator.join(parts)
            formatted = f"{noise} {formatted} {noise}"
        else:  # hard
            # More complex formatting with mixed case emphasis
            formatted = ""
            for i, char in enumerate(captcha):
                if i % 2 == 0:
                    formatted += char.upper()
                else:
                    formatted += char.lower()
                formatted += separator

        return formatted

    def verify_captcha(self, captcha, user_input, case_sensitive=False):
        """
        Verify user input against CAPTCHA.

        Args:
            captcha (str): The original CAPTCHA text
            user_input (str): User's input
            case_sensitive (bool): Whether to check case

        Returns:
            bool: True if match, False otherwise
        """
        if not case_sensitive:
            return captcha.lower() == user_input.lower()
        return captcha == user_input

    def generate_with_hint(self, difficulty="medium", length=None):
        """
        Generate CAPTCHA with a hint for display.

        Args:
            difficulty (str): 'easy', 'medium', or 'hard'
            length (int, optional): Specific length

        Returns:
            dict: Dictionary with captcha, hint, and display
        """
        captcha, display = self.generate_captcha(difficulty, length)

        hints = {
            "easy": f"Enter the {len(captcha)} numbers you see",
            "medium": f"Enter the {len(captcha)} alphanumeric characters (case-insensitive)",
            "hard": f"Enter the {len(captcha)} characters exactly as shown (case-sensitive)",
        }

        return {
            "captcha": captcha,
            "display": display,
            "hint": hints[difficulty],
            "length": len(captcha),
            "difficulty": difficulty,
        }


def print_banner():
    """Print the application banner."""
    print("=" * 50)
    print("        CAPTCHA GENERATOR")
    print("=" * 50)
    print()


def main():
    """Main function for interactive CAPTCHA generation."""
    gen = CaptchaGenerator()

    print_banner()
    print("Welcome to the CAPTCHA Generator!")
    print("This tool helps you generate random CAPTCHAs for verification.")
    print()

    while True:
        print("\nChoose difficulty level:")
        print("1. Easy (numbers only)")
        print("2. Medium (uppercase letters and numbers)")
        print("3. Hard (mixed case letters and numbers)")
        print("4. Custom (specify length)")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            result = gen.generate_with_hint("easy")
        elif choice == "2":
            result = gen.generate_with_hint("medium")
        elif choice == "3":
            result = gen.generate_with_hint("hard")
        elif choice == "4":
            try:
                length = int(input("Enter CAPTCHA length (4-10): ").strip())
                length = max(4, min(10, length))
                difficulty = input("Enter difficulty (easy/medium/hard): ").strip().lower()
                if difficulty not in ["easy", "medium", "hard"]:
                    difficulty = "medium"
                result = gen.generate_with_hint(difficulty, length)
            except ValueError:
                print("Invalid input. Using default settings.")
                result = gen.generate_with_hint("medium")
        elif choice == "5":
            print("\nThank you for using CAPTCHA Generator! Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")
            continue

        print("\n" + "=" * 50)
        print(f"Difficulty: {result['difficulty'].upper()}")
        print(f"CAPTCHA:    {result['display']}")
        print(f"Hint:       {result['hint']}")
        print("=" * 50)

        # Verification mode
        print("\n--- Verification Mode ---")
        user_input = input("Enter the CAPTCHA: ").strip()

        case_sensitive = result['difficulty'] == 'hard'
        if gen.verify_captcha(result['captcha'], user_input, case_sensitive):
            print("✓ Correct! Well done!")
        else:
            print(f"✗ Incorrect. The correct answer was: {result['captcha']}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting CAPTCHA Generator. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)
