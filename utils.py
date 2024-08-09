
import random
import string

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def generate_random_email():
    return f"{generate_random_string(10)}@example.com"

def generate_random_password():
    return generate_random_string(12)

def generate_random_name():
    return generate_random_string(8)

def generate_valid_ingredient_id():
    return f"valid_ingredient_id_{random.randint(1, 10)}"

def generate_invalid_ingredient_id():
    return f"invalid_ingredient_id_{random.randint(1, 10)}"
