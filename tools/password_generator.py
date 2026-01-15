import secrets as sc
import string

def generate_password():
    l = string.ascii_lowercase
    u = string.ascii_uppercase
    d = string.digits
    n = "!@#$%^&*()_-+="
    random_chars = []

    for chrs in [l, u, d, n]:
        for i in range(3 + sc.randbelow(3)):
            ch = sc.choice(chrs)
            random_chars.append(ch)
    
    sc.SystemRandom().shuffle(random_chars)
    password = ''.join(random_chars)
    return password

if __name__ == "__main__":
    print("Generated Password:", generate_password())