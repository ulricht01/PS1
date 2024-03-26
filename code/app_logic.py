import random
import string
import os
import hashlib
from werkzeug.utils import secure_filename
from flask_login import UserMixin, AnonymousUserMixin


def generate_random_key(len=8):
    characters = string.ascii_letters + string.digits
    characters = characters.replace('I', 'X').replace('l', 'Y')
    key = ''.join(random.choice(characters) for _ in range(len))
    return key

def hash_email(email):
    hashed_email = hashlib.sha256(email.encode('utf-8')).hexdigest()
    return hashed_email

def hash_klic(klic):
    hashed_klic = hashlib.sha256(klic.encode('utf-8')).hexdigest()
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


# Třída pro reprezentaci uživatele během běhu aplikace. Nezbytná pro metodu login_user, která přihlašuje uživatele do sessionu.
class User(UserMixin):
    def __init__(self, id, ucitel):
        self.id = id
        self.jeUcitel = ucitel

class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        self.jeUcitel = False

