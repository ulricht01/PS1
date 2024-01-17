import random
import string

def generate_random_key(len=15):
    characters = string.ascii_letters + string.digits + string.punctuation
    key = ''.join(random.choice(characters) for _ in range(len))
    return key

random_key = generate_random_key()
print(random_key) #prozatimní ukázání výsledku
