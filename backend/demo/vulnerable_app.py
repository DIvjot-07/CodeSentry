import os
import hashlib
import sqlite3
import pickle
from flask import Flask, request, jsonify

app = Flask(__name__)

# Hardcoded secret
API_KEY = "sk-1234567890abcdef"
DB_PASSWORD = "admin123"


def get_db():
    return sqlite3.connect('users.db')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # SQL Injection vulnerability
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
    user = cursor.fetchone()
    return jsonify({"user": user})


@app.route('/hash', methods=['POST'])
def hash_password():
    password = request.form['password']
    # Weak cryptography
    hashed = hashlib.md5(password.encode()).hexdigest()
    return jsonify({"hash": hashed})


@app.route('/ping', methods=['POST'])
def ping():
    host = request.form['host']
    # Command injection
    result = os.system(f"ping -c 1 {host}")
    return jsonify({"result": result})


@app.route('/load', methods=['POST'])
def load_data():
    data = request.get_data()
    # Insecure deserialization
    obj = pickle.loads(data)
    return jsonify({"loaded": str(obj)})


if __name__ == '__main__':
    # Debug mode enabled
    app.run(debug=True)
