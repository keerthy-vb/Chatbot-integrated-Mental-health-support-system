import hashlib

def generate_password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()  # Hash the password

def check_password_hash(hashed, password):
    return hashlib.sha256(password.encode()).hexdigest() == hashed