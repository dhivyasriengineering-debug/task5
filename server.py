from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Create the database file
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register_page')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return "User already exists! <a href='/register_page'>Try again</a>"

    hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return "Registration Successful! <a href='/'>Login now</a>"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        return f"<h1>Welcome {username}! Auth Successful.</h1>"
    
    return "<h1>Invalid Credentials! <a href='/'>Try again</a></h1>"

if __name__ == '__main__':
    app.run(debug=True)