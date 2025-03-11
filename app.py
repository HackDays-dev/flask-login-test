from flask import Flask, request, jsonify, render_template
import time

app = Flask(__name__)

# Dummy user database
users = {"test": "1234"}

# Track login requests
request_logs = []

@app.route('/')
def home():
    return render_template("index.html")  # Serve the HTML page

@app.route('/login', methods=['POST'])
def login():
    global request_logs
    username = request.form.get("username")
    password = request.form.get("password")

    request_logs.append(time.time())

    # Simulate server slowdown under heavy load
    if len(request_logs) > 50:
        time.sleep(2)

    if username in users and users[username] == password:
        return jsonify({"status": "success", "message": "Login successful"}), 200
    return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
