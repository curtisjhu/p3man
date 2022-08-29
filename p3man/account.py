import click
import os
from .db import connect, genHash, verify
from cryptography.exceptions import InvalidKey
from .messages import Error, Success
from .constant import secret_salt

@click.command()
def setup():
    if not click.confirm(f"Do you want to create an account on 'master'?"):
        click.echo("Aborted")
        return
    
    p = click.prompt("Your master password", hide_input=True)
    hashpw = genHash(p)
    
    try:
        c, conn = connect()
        c.execute(""" CREATE TABLE IF NOT EXISTS user (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        account varchar(255) UNIQUE,
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
        Error("An error occurred. Check if you already have setup")


@click.command()
def reset():

    op = click.prompt("Old password", hide_input=True)
    verify(op)

    try:
        c, conn = connect()
        np = click.prompt("New password", hide_input=True)
        hashed_np = genHash(np)
        c.execute(""" 
                    UPDATE user
                    SET password=? 
                    WHERE account = 'master'
                    """,
                    (hashed_np,))
        conn.commit()
        conn.close()
        Success()
    except:
        Error()

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


