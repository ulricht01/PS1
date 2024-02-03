import random
import string
import os
import hashlib
from werkzeug.utils import secure_filename

def generate_random_key(len=8):
    characters = string.ascii_letters + string.digits
    characters = characters.replace('I', 'X').replace('l', 'Y')
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
    
def allowed_file(filename):
    allowed_extensions = {'py'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions