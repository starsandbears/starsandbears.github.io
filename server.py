import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder=".")
CORS(app)

DATA_DIR = Path(__file__).parent / "data"
SUBSCRIBERS_FILE = DATA_DIR / "subscribers.json"


def _load_subscribers():
    if SUBSCRIBERS_FILE.exists():
        return json.loads(SUBSCRIBERS_FILE.read_text())
    return []


def _save_subscribers(subscribers):
    DATA_DIR.mkdir(exist_ok=True)
    SUBSCRIBERS_FILE.write_text(json.dumps(subscribers, indent=2))


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)


@app.route("/api/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    email = (data.get("email") or "").strip().lower()
    name = (data.get("name") or "").strip()
    interest = (data.get("interest") or "").strip()

    if not email or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return jsonify({"error": "A valid email address is required"}), 400

    subscribers = _load_subscribers()

    if any(s["email"] == email for s in subscribers):
        return jsonify({"message": "You're already subscribed! We'll keep you updated."}), 200

    subscribers.append({
        "email": email,
        "name": name,
        "interest": interest,
        "subscribed_at": datetime.now(timezone.utc).isoformat(),
    })
    _save_subscribers(subscribers)

    return jsonify({"message": "Welcome to the Stars&Bears community!"}), 201


@app.route("/api/subscribers", methods=["GET"])
def list_subscribers():
    """Admin endpoint — in production, protect this with auth."""
    subscribers = _load_subscribers()
    return jsonify({"count": len(subscribers), "subscribers": subscribers})


if __name__ == "__main__":
    app.run(debug=True, port=8080)
