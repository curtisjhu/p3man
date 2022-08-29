import click
import os
from .db import connect, verify
from .encryption import encrypt, decrypt
from .messages import Error, Success
from cryptography.exceptions import InvalidKey

@click.command()
@click.password_option()
def add(password:str):
    verify(password)
    account = click.prompt("Account (gmail, reddit, etc)").lower()
    username = click.prompt(f"Account username for {account}")
    account_password = click.prompt("Account password", hide_input=True)

    account_password = encrypt(password, account_password)

    try:
        c, conn = connect()
        c.execute("""
            INSERT INTO user (account, username, password)
            VALUES (?, ?, ?);
        """,
        (account, username, account_password))
        conn.commit()
        conn.close()
        Success()
    except:
        Error("An error occurred. Check if an account already exists")
    
@click.command()
@click.password_option()
def update(password:str):
    verify(password)
    account = click.prompt("Account (gmail, reddit, etc)").lower()
    np = click.prompt(f"New password for {account}", hide_input=True)

    np = encrypt(password, np)

    try:
        c, conn = connect()
        c.execute("""
            UPDATE user
            SET password = ?
            WHERE account = ?;
        """,
        (np, account))
        conn.commit()
        conn.close()
        Success(f"Successfully updated password for {account}")
    except:
        Error()

@click.command()
@click.password_option()
def get(password: str):
    verify(password)
    account = click.prompt("Account (gmail, reddit, facebook, etc)").lower()
    
    try:
        c, conn = connect()
        c.execute("""
            SELECT account, username, password FROM user 
            WHERE account = ?
            LIMIT 1; """,
        (account,))
        res = c.fetchone()
        click.echo(f"{res[0]} | {res[1]} | {decrypt(password, res[2])}")
        conn.commit()
        conn.close()
    except:
        Error()

@click.command()
@click.password_option()
def list(password):
    verify(password)

    try:
        c, conn = connect()
        c.execute("SELECT * FROM user;")
        res = c.fetchall()
        click.echo(res)
        conn.commit()
        conn.close()
    except:
        Error()
