from db import create_table
from expense import add_expense,export_to_csv
from view import view_expense

def menu():
    while True:
        print("Add Your Expense 💰")
        choice=input("Choose an Option :")
        if choice == "1":
            date=input("Date DD-MM-YYYY")
            category=input("Enter your Category of Expense ")
            amount=input("Enter the  amount of transaction  ")
            note=input("Enter note about transaction")
            add_expense(date,category,amount,note)
            print("Expense added Succesfully ")
        elif choice=="2":
            view_expense()
        elif choice=="3":
            export_to_csv()
        elif choice=="4":
            break
        else:
            print("Invalid choice")


if __name__=="__main__":
    create_table()
    menu()