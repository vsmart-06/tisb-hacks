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
c.execute('''
    CREATE TABLE IF NOT EXISTS lifts (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        path TEXT NOT NULL
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
    c.close()
    conn.close()
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
    conn.commit()
    c.close()
    conn.close()

def add_lift(username: str, origin: str, destination: str, path: str):
    conn = db.connect("tisb-hacks/tisb-hacks.db")
    c = conn.cursor()
    origin = origin.replace("'", "")
    destination = destination.replace("'", "")
    c.execute(f"INSERT INTO lifts (username, origin, destination, path) VALUES ('{username}', '{origin}', '{destination}', '{path}')")
    conn.commit()
    c.close()
    conn.close()

def get_lifts(id: int = None):
    conn = db.connect("tisb-hacks/tisb-hacks.db")
    c = conn.cursor()
    if not id:
        c.execute("SELECT * FROM lifts")
        lifts = c.fetchall()
    else:
        c.execute(f"SELECT * FROM lifts WHERE id = {id}")
        lifts = c.fetchone()
    c.close()
    conn.close()
    return lifts

c.close()
conn.close()