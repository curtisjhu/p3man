from cryptography.fernet import Fernet
from .constant import secret_salt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from .db import connect
import base64

def getKey(password: str):
	c, conn = connect()
	c.execute("""
		SELECT username FROM user
		WHERE account = 'master';
	""")
	salt = c.fetchone()[0]
	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=salt,
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