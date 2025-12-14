def check_password_strength(password):
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
    print("Password strength:", check_password_strength(pwd))
