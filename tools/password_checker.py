MIN_PASSWORD_LENGTH = 4


def validate_password_input(password):
    """
    Validate password input and return appropriate error messages.

    Args:
        password: The password string to validate.

    Returns:
        tuple: (is_valid, error_message). If valid, error_message is None.
    """
    if password is None:
        return False, "Password cannot be None. Please enter a password."

    if not isinstance(password, str):
        return False, "Password must be a string."

    if len(password) == 0:
        return False, "Password cannot be empty. Please enter a password."

    if password.isspace():
        return False, "Password cannot be only whitespace. Please enter a valid password."

    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Password is too short ({len(password)} characters). Please use at least {MIN_PASSWORD_LENGTH} characters."

    return True, None


def check_password_strength(password):
    """
    Check the strength of a password.

    Args:
        password: The password string to check.

    Returns:
        str: Password strength rating ("Weak", "Medium", or "Strong"),
             or an error message if the password is invalid.
    """
    # Validate input first
    is_valid, error_message = validate_password_input(password)
    if not is_valid:
        return error_message

    length_score = len(password) >= 8
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)

    score = sum([length_score, has_upper, has_lower, has_digit])

    if score <= 2:
        return "Weak"
    elif score == 3:
        return "Medium"
    else:
        return "Strong"


if __name__ == "__main__":
    pwd = input("Enter password: ")
    result = check_password_strength(pwd)
    print("Password strength:", result)
