import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
VANTA_CLIENT_ID = os.environ["VANTA_CLIENT_ID"]
VANTA_CLIENT_SECRET = os.environ["VANTA_CLIENT_SECRET"]

def get_vanta_token():
    url = "https://api.vanta.com/oauth/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": VANTA_CLIENT_ID,
        "client_secret": VANTA_CLIENT_SECRET
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["access_token"]

def search_kb_articles(query):
    token = get_vanta_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = f"https://api.vanta.com/v1/knowledge-base/articles?query={query}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def send_slack_message(channel, text):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": channel,
        "text": text
    }
    requests.post(url, json=payload, headers=headers)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json

    # Slack verification challenge
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    # Handle app_mention event
    if "event" in data and data["event"]["type"] == "app_mention":
        event = data["event"]
        user_question = event.get("text", "").split(">")[-1].strip()  # Remove bot mention
        channel = event["channel"]

        try:
            results = search_kb_articles(user_question)
            articles = results.get("data", [])
            if articles:
                article = articles[0]
                title = article["attributes"]["title"]
                url = article["attributes"]["url"]
                send_slack_message(channel, f"🔍 I found something:\n*<{url}|{title}>*")
            else:
                send_slack_message(channel, "🤔 Sorry, I couldn't find anything relevant in the Knowledge Base.")
        except Exception as e:
            print("Error:", str(e))
            send_slack_message(channel, "⚠️ Something went wrong while searching Vanta. Please try again later.")

    return jsonify({"ok": True})

@app.route("/")
def index():
    return "VantaBot is up and running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))