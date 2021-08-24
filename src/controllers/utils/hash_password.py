from hashlib import pbkdf2_hmac
import binascii
from src.config import Configuration
from uuid import uuid4


def generate_salt():
    return str(uuid4())


def hash_password(password: str, salt: str):
    binary_hash = pbkdf2_hmac(Configuration.PASSWORD_HASH_FUNC,
                              password.encode(),
                              salt.encode(),
                              Configuration.PASSWORD_GENERATE_ITERATIONS)
    return binascii.hexlify(binary_hash).decode()
