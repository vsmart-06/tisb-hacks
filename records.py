import sqlite3 as db

conn = db.connect("tisb-hacks/tisb-hacks.db")
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS user_details (
        username TEXT NOT NULL PRIMARY KEY,
        password TEXT NOT NULL,
        credits INTEGER NOT NULL
    )
''')
conn.commit()

def user_login(username: str, password: str):
    conn = db.connect("tisb-hacks/tisb-hacks.db")
    c = conn.cursor()
    c.execute(f"SELECT * FROM user_details WHERE username = '{username}' AND password = '{password}'")
    record = c.fetchone()
    if not record:
        c.close()
        conn.close()
        return False
    c.close()
    conn.close()
    return True

def user_signup(username: str, password: str):
    conn = db.connect("tisb-hacks/tisb-hacks.db")
    c = conn.cursor()
    c.execute(f"SELECT * FROM user_details WHERE username = '{username}'")
    record = c.fetchone()
    if not record:
        c.execute(f"INSERT INTO user_details VALUES ('{username}', '{password}', 100)")
        conn.commit()
        c.close()
        conn.close()
        return True
    c.close()
    conn.close()
    return False

def get_credits(username: str):
    conn = db.connect("tisb-hacks/tisb-hacks.db")
    c = conn.cursor()
    c.execute(f"SELECT credits FROM user_details WHERE username = '{username}'")
    creds = c.fetchone()[0]
    return creds

def change_credits(username: str, amount: int, add: bool):
    conn = db.connect("tisb-hacks/tisb-hacks.db")
    c = conn.cursor()
    c.execute(f"SELECT credits FROM user_details WHERE username = '{username}'")
    old_creds = c.fetchone()[0]
    if add:
        new_creds = old_creds + amount
    else:
        new_creds = old_creds - amount
    c.execute(f"UPDATE user_details SET credits = {new_creds} WHERE username = '{username}'")

c.close()
conn.close()