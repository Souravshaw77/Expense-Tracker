import sqlite3

conn = sqlite3.connect("expenses.db")
c = conn.cursor()
c.execute("SELECT * FROM users")
print(c.fetchall())
conn.close()
