import sqlite3
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os
from .messages import Error, ErrorWrongPassword
from cryptography.exceptions import InvalidKey
from .constant import secret_salt

def connect():
	conn = sqlite3.connect('management.db')
	c = conn.cursor()
	return c, conn

def genKDF():
	kdf = Scrypt(
		salt=secret_salt,
		length=32,
		n=2**14,
		r=8,
		p=1,
	)
	return kdf

def genHash(password):
	kdf = genKDF()
	return kdf.derive(bytes(password, "utf-8"))

def verify(password):
	try:
		c, conn = connect()
		c.execute("""
			SELECT password FROM user
			WHERE account = 'master';
		""")
		db_p = c.fetchone()[0]
		conn.commit()
		conn.close()

		kdf = genKDF()
		kdf.verify(bytes(password, 'utf-8'), db_p)
	except InvalidKey:
		raise ValueError("Wrong Password")
	except:
		raise Exception("Error")