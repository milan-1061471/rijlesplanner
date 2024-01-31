from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Geef een willekeurige sleutel op voor sessions

DATABASE = 'database.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + key

def verify_password(stored_password, provided_password, stored_salt):
    key = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), stored_salt, 100000)
    return key == stored_password

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user and verify_password(user[2], password, user[3]):
        # Inloggen gelukt, je kunt hier bijvoorbeeld een session gebruiken
        return 'Inloggen gelukt!'
    else:
        return 'Inloggen mislukt!'

@app.route('/admin')
def admin():
    # Voeg hier logica toe om te controleren of de gebruiker een admin is
    # Bijvoorbeeld: if current_user_is_admin():
    # Als niet, dan kun je een foutmelding of inlogscherm tonen

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()

    return render_template('admin.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    # Voeg hier logica toe om te controleren of de gebruiker een admin is
    # Bijvoorbeeld: if current_user_is_admin():
    # Als niet, dan kun je een foutmelding of inlogscherm tonen

    username = request.form['username']
    password = request.form['password']

    salted_password = hash_password(password)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, salt) VALUES (?, ?, ?)', (username, salted_password[32:], salted_password[:32]))
    conn.commit()
    conn.close()

    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
