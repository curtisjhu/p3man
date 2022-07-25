import click
import os
from .db import conn

@click.command()
@click.password_option()
def setup(password):
    if not click.confirm(f"Do you want to create an account on 'master'?"):
        click.echo("Aborted")
        return

    
    with conn.cursor() as c:
        c.execute(""" CREATE TABLE IF NOT EXISTS user (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        account varchar(255) UNIQUE,
                        password varchar(255)
                    ) """)
        c.execute(""" 
                    INSERT INTO user (account, password)
                    VALUES ('master', %(password)s)
                """,
                {
                    "password": hashedpw
                })
        conn.commit()
    conn.close()


@click.command()
@click.password_option()
def update(password):
    
    with conn.cursor() as c:
        c.execute(""" 
                    UPDATE user
                    SET password= %(password)s
                    WHERE account = 'master'
                    """,
                    {
                        "password": hashedpw
                    })
        conn.commit()
        conn.close()

@click.command()
@click.password_option()
def remove_account(password):
    """ Removes all data, all passwords from device (irreversable) """
    if not click.confirm(f"Do you want to continue to delete ALL information on {os.getlogin()}?"):
        click.echo(click.style('Aborted', fg='blue'))
        return
    
    hashedpw = password

    with conn.cursor() as c:
        c.execute(""" 
                SELECT password FROM user WHERE password = %(password)s;
                """,
                {
                    "password": hashedpw
                })
        res = c.fetchone()
        if res == hashedpw:
            c.execute(f""" 
                    DROP DATABASE management;
                    """)
        else:
            click.echo(click.style('Aborted, wrong password', fg='blue'))
    conn.commit()
    conn.close()