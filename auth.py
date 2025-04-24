# auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
import sqlite3

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')
bcrypt = Bcrypt()

# Initialize database connection
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT NOT NULL,
                       email TEXT UNIQUE NOT NULL,
                       password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Call the function to create the table
init_db()

@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Store in database
        conn = sqlite3.connect('database.db')
        # conn = sqlite3.connect('D:\ResumeAnalyzer\database.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                           (username, email, hashed_password))
            conn.commit()
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash('Email already exists. Please use a different email.', 'danger')
        finally:
            conn.close()

    return render_template('signup.html')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check database for user
        conn = sqlite3.connect('database.db')
        # conn = sqlite3.connect('D:\ResumeAnalyzer\database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()

        # Validate user credentials
        if user and bcrypt.check_password_hash(user[3], password):
            session['user_id'] = user[0]
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')

@auth_blueprint.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user_id from session
    return redirect(url_for('auth.login'))  # Redirect to login page

