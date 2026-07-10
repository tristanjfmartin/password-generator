import random
import string

def generate_password(length=12, use_upper=True, use_digits=True, use_symbols=True):
    characters = string.ascii_lowercase

    if use_upper:
        characters += string.ascii_uppercase

    if use_digits:
        characters += string.digits

    if use_symbols:
        characters += string.punctuation

    password = "".join(random.choice(characters) for _ in range(length))
    return password
