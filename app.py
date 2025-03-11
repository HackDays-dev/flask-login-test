from flask import Flask, request, jsonify, render_template
import time

app = Flask(__name__)

# Dummy user database
users = {"test": "1234"}

# Store request logs { IP: [timestamps] }
request_logs = {}

# Request limit (requests per 10 seconds)
REQUEST_LIMIT = 20
BLOCK_DURATION = 60  # Block for 60 seconds

# Store blocked IPs { IP: unblock_time }
blocked_ips = {}

@app.route('/')
def home():
    return render_template("index.html")  # Serve the HTML page

@app.route('/login', methods=['POST'])
def login():
    global request_logs, blocked_ips

    ip = request.remote_addr  # Get user IP address
    current_time = time.time()

    # Check if IP is blocked
    if ip in blocked_ips and current_time < blocked_ips[ip]:
        return jsonify({"status": "fail", "message": "Too many requests. Try again later."}), 429

    # Track login attempts
    if ip not in request_logs:
        request_logs[ip] = []
    request_logs[ip].append(current_time)

    # Remove old requests (older than 10 sec)
    request_logs[ip] = [t for t in request_logs[ip] if current_time - t < 10]

    # If request count exceeds limit, block IP
    if len(request_logs[ip]) > REQUEST_LIMIT:
        blocked_ips[ip] = current_time + BLOCK_DURATION
        return jsonify({"status": "fail", "message": "Too many requests. You are temporarily blocked."}), 429

    # Validate login
    username = request.form.get("username")
    password = request.form.get("password")

    if username in users and users[username] == password:
        return jsonify({"status": "success", "message": "Login successful"}), 200
    return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
