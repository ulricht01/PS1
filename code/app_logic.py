import random
import string

def generate_random_key(len=15):
    characters = string.ascii_letters + string.digits + string.punctuation
    key = ''.join(random.choice(characters) for _ in range(len))
    return key
