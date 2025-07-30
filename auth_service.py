from firebase_init import db
from cryptography.fernet import Fernet

def register_user(username, password):
    user_key = Fernet.generate_key().decode()  # Generate encryption key
    db.collection('users').document(username).set({
        "password": your_password,
        "fernet_key": your_key,
    })
    return True

def get_user_key(username):
    doc = db.collection('users').document(username).get()
    if doc.exists:
        return doc.to_dict().get("fernet_key")
    return None
