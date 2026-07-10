import secrets
import string
from words import WORD_LIST


def generate_password(length=12, use_upper=True, use_digits=True, use_symbols=True):
    characters = string.ascii_lowercase

    if use_upper:
        characters += string.ascii_uppercase

    if use_digits:
        characters += string.digits

    if use_symbols:
        characters += string.punctuation

    password = "".join(secrets.choice(characters) for _ in range(length))
    return password


def generate_passphrase(word_count=5):
    return "-".join(secrets.choice(WORD_LIST) for _ in range(word_count))
