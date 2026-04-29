from flask import Flask, jsonify, request, render_template_string
import webbrowser 
from threading import Timer

app = Flask(__name__) 

USER_DATA = {"admin": "password123"}

login_html = """
    <h2>Login Page</h2>
    <form method="POST">
        Username: <input type="text" name="username"><br><br>
        Password: <input type="password" name="password"><br><br>
        <input type="submit" value="Login">
    </form>
    <p style="color:red">{{ error }}</p>
"""
@app.route('/', methods=['GET','POST'])
def login():
    if request.method =='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USER_DATA and USER_DATA[username] == password:
            return f"<h1>Welcome {username}! Login Success.</h1>"
        else:
            return render_template_string(login_html, error="Invalid Credentials!")
    return render_template_string(login_html)
    
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    Timer(1.5,open_browser).start()
    app.run(debug=True, use_reloader=False)