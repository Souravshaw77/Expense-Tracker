from flask import Flask, render_template, request, redirect,session,flash,url_for
from functools import wraps
import sqlite3
from expense import add_expense, get_expenses 
from collections import defaultdict
import datetime
from view import get_all_expenses
from db import create_table,create_user_table,validate_user, register_user,connect
from werkzeug.security import generate_password_hash, check_password_hash




app = Flask(__name__)
app.secret_key = 'your_super_secret_key' 
create_table() 
create_user_table()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("Please log in to access this page.")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        password = generate_password_hash(request.form['password'])

        hashed_password = generate_password_hash(password)

        with sqlite3.connect('expenses.db') as conn:
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                flash('Registration successful. Please login.', 'success')
                return redirect('/login')
            except sqlite3.IntegrityError:
                flash('Username already exists.', 'danger')

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connect()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):  # user[2] is hashed password
            session['user'] = username
            flash("Logged in successfully.")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        date = request.form["date"]
        category = request.form["category"]
        amount = request.form["amount"]
        note = request.form["note"]
        
        print("Saving:", date, category, amount, note) 
        add_expense(date, category, amount, note)
        return redirect("/view")
    return render_template("add.html")

@app.route("/dashboard")
@login_required
def dashboard():
    expenses = get_all_expenses()

    if not expenses:
        return render_template("dashboard.html", labels=[], values=[], expenses=[])

    
    category_totals = defaultdict(float)
    for exp in expenses:
        category = exp[2]  
        amount = float(exp[3])  
        category_totals[category] += amount

    labels = list(category_totals.keys())
    values = list(category_totals.values())

    return render_template("dashboard.html", labels=labels, values=values, expenses=expenses)


@app.route("/view")
@login_required
def view():
    expenses = get_all_expenses()
    return render_template("view.html", expenses=expenses)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    conn = sqlite3.connect('expenses.db')
    c=conn.cursor()

    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = float(request.form['amount'])
        note = request.form['note']
        
        c.execute("UPDATE expenses SET date=?, category=?, amount=?, note=? WHERE id=?",
                  (date, category, amount, note, id))
        conn.commit()
        conn.close()
        return redirect('/view')

    
    c.execute("SELECT * FROM expenses WHERE id=?", (id,))
    expense = c.fetchone()
    conn.close()
    return render_template('edit.html', expense=expense)

@app.route('/delete/<int:id>')
@login_required
def delete_expense(id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/view')



    

if __name__ == "__main__":
    app.run(debug=True)
