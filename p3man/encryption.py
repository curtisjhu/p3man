from cryptography.fernet import Fernet
from .constant import secret_salt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from .db import connect
import base64
from .constant import secret_salt

def getKey(password: str):
	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=secret_salt,
		iterations=390000,
	)
	hashed = kdf.derive(bytes(password, "utf-8"))
	return base64.urlsafe_b64encode(hashed)

def encrypt(master_password, account_password):
	key = getKey(master_password)
	f = Fernet(key)
	token = f.encrypt(bytes(account_password, "utf-8"))
	return token

def decrypt(master_password, token_password):
	key = getKey(master_password)
	f = Fernet(key)
	res = f.decrypt(token_password)
	return res.decode("utf-8")