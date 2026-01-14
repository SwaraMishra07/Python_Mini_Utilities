def check_password_strength(password):
    symbols="!@#$%^&*()_-+={}[]|/~`"
    length_score = len(password) >= 8
    #Empty or whitespaces check
    if not password or not password.strip():
        print("Password cannot be empty or only whitespaces!")
    
    #Password must contain atleast one digit
    if not any(char.isdigit()for char in password ):
            print("Password must conatin atleast one digit!")   

    #Password must be of minimum 8 charachters
    if len(password)<8:
        print("Password must of minimum 8 characters!")


    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    
    #Adding symbol check in Password
    has_symbol= any(char in symbols for char in password)

    score = sum([length_score, has_upper, has_lower, has_digit, has_symbol])


    if score <= 2:
        return "Weak"
    elif score == 3:
        return "Medium"
    else:
        return "Strong"
if __name__ == "__main__":
    pwd = input("Enter password: ")
    print("Password strength:", check_password_strength(pwd))
