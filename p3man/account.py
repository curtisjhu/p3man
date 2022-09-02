import click
import os
from .db import connect, genHash, verify
from cryptography.exceptions import InvalidKey
from .messages import Error, Success
from .constant import secret_salt
from .encryption import encrypt, decrypt

@click.command()
def setup():
    """ Setup up your account and master password """
    if not click.confirm(f"Do you want to create an account on 'master'?"):
        Error("Aborted!")
        return
    
    p = click.prompt("Your master password", hide_input=True)
    cp = click.prompt("Confirm your master password", hide_input=True)

    if p != cp:
        Error("Passwords do not match.")
        return

    hashpw = genHash(p)
    
    try:
        c, conn = connect()
        c.execute(""" CREATE TABLE IF NOT EXISTS user (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        account varchar(255),
                        username varchar(255),
                        password varchar(255)
                    ); """)
        c.execute(""" 
                    INSERT INTO user (account, username, password)
                    VALUES ('master', ?, ?);
                """, (secret_salt, hashpw,))
        conn.commit()
        conn.close()
        Success("Successful setup on 'master'")
    except:
        Error("An error occurred. Check if you already have a setup")


@click.command()
def reset():
    """ Reset your master password. """

    op = click.prompt("Old password", hide_input=True)
    verify(op)

    # try:
    c, conn = connect()
    np = click.prompt("New password", hide_input=True)
    npc = click.prompt("Confirm new password", hide_input=True)
    assert np == npc

    hashed_np = genHash(np)
    c.execute("SELECT * FROM user;")
    old_data = c.fetchall()
    
    c.execute("DROP TABLE user;")
    c.execute(""" CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    account varchar(255),
                    username varchar(255),
                    password varchar(255)
                ); 
            """)
    c.execute("""
                INSERT INTO user (account, username, password)
                VALUES ('master', ?, ?);
                """, (secret_salt, hashed_np,))

    for acc in old_data:
        print(acc[3])
        pp = decrypt(op, acc[3])
        acc[3] = encrypt(np, pp)
        c.execute("""
            INSERT INTO user (account, username, password)
            VALUES (?, ?, ?);
        """, (acc[1], acc[2], acc[3]))
    conn.commit()
    conn.close()
    Success()
    # except:
    #     Error()

@click.command()
def wipe():
    """ Removes all data, all passwords from device (irreversable) """
    if not click.confirm(f"Do you want to continue to delete ALL information on table?"):
        click.echo(click.style('Aborted', fg='red'))
        return

    p = click.prompt("Confirm with password", hide_input=True)
    verify(p)

    try:
        c, conn = connect()
        c.execute(f""" 
                DROP TABLE user;
                """)
        conn.commit()
        conn.close()
        Success("Successfully deleted table.")
    except:
        Error()


