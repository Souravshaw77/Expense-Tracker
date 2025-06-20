import sqlite3

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Add 'note' column if it doesn't already exist
try:
    cursor.execute("ALTER TABLE EXPENSES ADD COLUMN note TEXT")
    print("Column 'note' added successfully.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("Column 'note' already exists.")
    else:
        raise

conn.commit()
conn.close()
