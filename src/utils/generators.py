import random
import string


def generate_random_digit_char_string(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))
