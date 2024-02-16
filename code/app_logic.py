import random
import string
import os
import hashlib
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

def generate_random_key(len=15):
    characters = string.ascii_letters + string.digits
    key = ''.join(random.choice(characters) for _ in range(len))
    return key

def hash_email(email):
    hashed_email = generate_password_hash(email, method='sha256')
    return hashed_email

def hash_klic(klic):
    hashed_klic = generate_password_hash(klic, method='sha256')
    return hashed_klic
    
class User(UserMixin):
    def __init__(self, email, ucitel=False):
        self.id = email
        self.jeUcitel = ucitel