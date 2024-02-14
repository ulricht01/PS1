import random
import string
import os
import hashlib
from flask_login import UserMixin

def generate_random_key(len=15):
    characters = string.ascii_letters + string.digits
    key = ''.join(random.choice(characters) for _ in range(len))
    return key

def hash_email(email):
    hashed_email = hashlib.sha256(email.encode('utf-8')).hexdigest()
    return hashed_email

def verify_email(user_input_email, stored_hashed_email):
    hashed_input_email = hashlib.sha256(user_input_email.encode('utf-8')).hexdigest()
    if hashed_input_email == stored_hashed_email:
        return True
    else:
        return False
    
class User(UserMixin):
    def __init__(self, klic, ucitel=False):
        self.id = klic
        self.jeUcitel = ucitel