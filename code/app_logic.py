import random
import string
import os
import hashlib
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import UserMixin


def generate_random_key(len=8):
    characters = string.ascii_letters + string.digits
    characters = characters.replace('I', 'X').replace('l', 'Y')
    key = ''.join(random.choice(characters) for _ in range(len))
    return key

def hash_email(email):
    hashed_email = generate_password_hash(email, method='sha256')
    return hashed_email

def hash_klic(klic):
    hashed_klic = generate_password_hash(klic, method='sha256')
    return hashed_klic
    
def verify_email(user_input_email, stored_hashed_email):
    hashed_input_email = hashlib.sha256(user_input_email.encode('utf-8')).hexdigest()
    if hashed_input_email == stored_hashed_email:
        return True
    else:
        return False
    
def allowed_file(filename):
    allowed_extensions = {'py'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def ziskat_typ_souboru(file_path):
    file_extension = os.path.splitext(file_path)[1]

    if file_extension == ".py":
        return "Python"
    else:
        return "N/A"
    
def ziskat_velikost_souboru(file_path):
    return os.path.getsize(file_path)


class User(UserMixin):
    def __init__(self, email, ucitel=False):
        self.id = email
        self.jeUcitel = ucitel
