import sqlite3
import hashlib

def connect():
    return sqlite3.connect("expenses.db")

def create_user_table():
    with connect() as conn:
        c=conn.cursor()
        c.execute('''

      CREATE TABLE IF NOT EXISTS users(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL
                  
                  )
                  ''')
        conn.commit()

def create_table():
    conn=connect()
    cursor=conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS EXPENSES(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   date VARCHAR(100),
                   category VARCHAR(100),
                   amount REAL,
                   note TEXT
                   
                   )''')
    conn.commit()
    conn.close()
    print("✅ expenses table created or verified.")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    try:
        with connect() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                      (username, hash_password(password)))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

def validate_user(username, password):
    with connect() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", 
                  (username, hash_password(password)))
        return c.fetchone() is not None