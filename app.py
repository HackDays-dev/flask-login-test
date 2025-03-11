from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# Dummy user database
users = {"test": "1234"}

# Store login request timestamps
request_logs = []

@app.route('/')
def home():
    return "Vulnerable Login Page - POST to /login"

@app.route('/login', methods=['POST'])
def login():
    global request_logs
    username = request.form.get("username")
    password = request.form.get("password")

    # Log request timestamps
    request_logs.append(time.time())

    # Simulate server slowdown if too many requests (basic DoS effect)
    if len(request_logs) > 50:  # Threshold for overload
        time.sleep(2)  # Artificial delay to simulate DDoS

    # Validate login
    if username in users and users[username] == password:
        return jsonify({"status": "success", "message": "Login successful"}), 200
    return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
