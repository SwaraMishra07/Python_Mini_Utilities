import secrets as sc
import string

def generate_password():
    l = string.ascii_lowercase
    u= string.ascii_uppercase
    d = string.digits
    n = "!@#$%^&*()_-+="

    random_chars =  [sc.choice(l) for i in range(3+sc.randbelow(3))] + [sc.choice(u) for i in range(3+sc.randbelow(3))] + [sc.choice(n) for i in range(2+sc.randbelow(3))] + [sc.choice(d) for i in range(2+sc.randbelow(3))]
    sc.SystemRandom().shuffle(random_chars)
    password = ''.join(random_chars)
    return password

if __name__ == "__main__":
    print("Generated Password:", generate_password())