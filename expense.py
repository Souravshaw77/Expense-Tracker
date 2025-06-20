from db import connect
import pandas as pd
import sqlite3

def add_expense(date, category, amount, note):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (date, category, amount, note) VALUES (?, ?, ?, ?)",
                   (date, category, amount, note))
    conn.commit()
    conn.close()
    
def get_expenses():
     return []


def export_to_csv(filename="expenses_export.csv"):
    conn=connect()
    cursor=conn.cursor()
    cursor.execute("SELECT id,date,category,amount,note FROM expenses")
    rows=cursor.fetchall()
    conn.close()
    if not rows:
        print("No expenses recorded")
        return
    
    df=pd.DataFrame(rows,columns=["ID","DATE","CATEGORY","AMOUNT","NOTE"])
    df.to_csv(filename,index=False)
    print(f"Expenses exportd to'{filename}'successfully")
