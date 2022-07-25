import click
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64
from .db import conn
from .print import print_terminal

@click.command()
@click.option('--account', help='(opt) gmail, facebook, etc')
@click.argument('master_password')
def retrieve(account: str, master_password: str):

    account = account if account else ""
    with conn.cursor() as c:
        account.lower()
        c.execute(" SELECT account, password FROM user WHERE account = %(account)s LIMIT 1; ",
        {
            "account": account
        })
        pws = c.fetchall()
        print_terminal(pws)
    

    conn.close()

@click.command()
def list():
    with conn.cursor() as c:
        c.execute(" SELECT account, password FROM user")
        accounts = c.fetchall()
        print_terminal(accounts)
        conn.close()