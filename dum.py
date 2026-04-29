from flask import Flask, jsonify, request
import webbrowser 
from threading import Timer


app = Flask(__name__)


users = [
    {"id": 1, "name": "Arun"},
    {"id": 2, "name": "Priya"},
    {"id": 3, "name": "Arul"}
]




@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200


@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = {"id": len(users) + 1, "name": data['name']}
    users.append(new_user)
    return jsonify({"message": "User Added!", "user": new_user}), 201


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/users")

if __name__ == '__main__':
    Timer(1.5,open_browser).start()
    app.run(debug=True, use_reloader=False)