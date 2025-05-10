from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json
    print("Slack event:", data)
    return jsonify({"ok": True})

@app.route("/")
def hello():
    return "Vanta Slack Bot is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
