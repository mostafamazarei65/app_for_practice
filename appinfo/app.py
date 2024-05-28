from os import getcwd
from flask import Flask, url_for, jsonify
from random import randrange
from datetime import datetime, timedelta
import socket

app = Flask(__name__)

app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

NUM_REQUESTS = 0
HEALTH_STATUS = 1

RANDOM_TARGET_POINT = randrange(100, 500)

try:
    with open(getcwd() + "/.appinfo") as f:
        APP_INFO = f.read().split(":")
except FileNotFoundError:
    APP_INFO = ["unknown_version", "unknown_commit"]

START_TIME = datetime.utcnow()

@app.before_request
def compute_request():
    global NUM_REQUESTS, HEALTH_STATUS
    if NUM_REQUESTS >= RANDOM_TARGET_POINT:
        HEALTH_STATUS = 0
    NUM_REQUESTS += 1

@app.route("/")
def index():
    return f"""<!DOCTYPE html>
<html>
    <body>
        <div id="main">
            <h1>Available endpoints:</h1>
            <ul>
                <li><a href="{url_for('appinfo')}">/appinfo</a></li>
                <li><a href="{url_for('livez')}">/livez</a></li>
                <li><a href="{url_for('readyz')}">/readyz</a></li>
            </ul>
            <a href="https://www.linkedin.com/in/mostafamazarei/">App</a>
        </div>
    </body>
</html>"""

@app.route("/livez")
def livez():
    """
    Endpoint to check application liveness.
    Use this endpoint in Kubernetes livenessProbe property.
    """
    if HEALTH_STATUS:
        return "up", 200
    return "down", 500

@app.route("/readyz")
def readyz():
    """
    Endpoint to check application readiness.
    Use this endpoint in Kubernetes readinessProbe property.
    """
    if HEALTH_STATUS:
        return "up", 200
    return "down", 500

@app.route("/appinfo")
def appinfo():
    """
    Endpoint of the application info and version.
    Showing current release and application target point and status.
    """
    uptime = datetime.utcnow() - START_TIME
    request_rate = NUM_REQUESTS / uptime.total_seconds() if uptime.total_seconds() > 0 else 0
    hostname = socket.gethostname()
    app_info = {
        "hostname": hostname,
        "app_version": APP_INFO[0].strip(),
        "git_commit": APP_INFO[1].strip(),
        "target_point": RANDOM_TARGET_POINT,
        "num_requests": NUM_REQUESTS,
        "health_status": HEALTH_STATUS,
        "uptime": str(uptime),
        "server_time": datetime.utcnow().isoformat() + "Z",
        "request_rate": request_rate
    }
    return jsonify(app_info), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
