import mysql.connector
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret_key_123"

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  
        database="user_db"
    )
    return conn

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/register")

@app.route('/')
def home():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)

        try:
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("User already exists! Try another username.", "danger")
                return redirect(url_for('register'))

            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_pw))
            db.commit()
            cursor.close()
            db.close()
            
            flash("Registration Successful! Now you can Login.", "success")
            return redirect(url_for('login')) 
            
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "danger")
            
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user and check_password_hash(user['password'], password):
            session['user'] = username
            flash("Login Successful!", "success")
            
            return redirect(url_for('login')) 
        else:
            flash("Invalid Username or Password!", "danger")
            return redirect(url_for('login'))
            
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return redirect(url_for('login'))

# ... (Logout and other code same) ...

@app.route('/logout')
def logout():
    session.pop('user', None) 
    flash("You have been logged out.", "info")
    return redirect(url_for('login')) 

if __name__ == '__main__':
    Timer(1, open_browser).start()
    
    app.run(debug=True, use_reloader=False)