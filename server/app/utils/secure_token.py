import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()
cipher_suite = Fernet(os.getenv("OAUTH_TOKEN_KEY"))


def encrypt_data(data):
    """Encrypt the data."""
    return cipher_suite.encrypt(data.encode())

def decrypt_data(encrypted_data):
    """Decrypt the data."""
    return cipher_suite.decrypt(encrypted_data).decode()


