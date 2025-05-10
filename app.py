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
        "client_secret": VANTA_CLIENT_SECRET,
        "scope": "knowledge-base:read"
    }

    print("🔐 Requesting Vanta token...", flush=True)
    try:
        response = requests.post(url, json=payload)
        print(f"📡 Vanta token response: {response.status_code} – {response.text}", flush=True)
        response.raise_for_status()
        token = response.json().get("access_token")
        if not token:
            raise ValueError("No access_token in Vanta response")
        print(f"🪪 Got Vanta access token: {token[:10]}...", flush=True)
        return token
    except Exception as e:
        print(f"❌ ERROR getting Vanta token: {e}", flush=True)
        raise

def search_kb_articles(query):
    print(f"🔍 Searching Vanta KB for: {query}", flush=True)
    try:
        token = get_vanta_token()
        headers = {
            "Authorization": f"Bearer {token}"
        }
        url = f"https://api.vanta.com/v1/knowledge-base/articles?query={query}"
        response = requests.get(url, headers=headers)
        print(f"📡 Vanta KB response: {response.status_code} – {response.text}", flush=True)
        response.raise_for_status()
        json_data = response.json()
        print(f"📄 Vanta articles JSON: {json_data}", flush=True)
        return json_data
    except Exception as e:
        print(f"❌ ERROR during Vanta KB query: {e}", flush=True)
        raise

def send_slack_message(channel, text):
    print(f"💬 Sending Slack message to {channel}: {text}", flush=True)
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": channel,
        "text": text
    }
    resp = requests.post(url, json=payload, headers=headers)
    print(f"📤 Slack response: {resp.status_code} – {resp.text}", flush=True)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    try:
        data = request.json
        print(f"📥 Incoming Slack event: {data}", flush=True)

        # Slack URL verification
        if "challenge" in data:
            return jsonify({"challenge": data["challenge"]})

        if "event" in data and data["event"]["type"] == "app_mention":
            event = data["event"]
            text = event.get("text", "")
            channel = event.get("channel", "")
            user_question = text.split(">")[-1].strip()
            print(f"🧠 Parsed question: '{user_question}' from channel {channel}", flush=True)

            try:
                results = search_kb_articles(user_question)
                articles = results.get("data", [])
                if articles:
                    article = articles[0]
                    title = article["attributes"]["title"]
                    url = article["attributes"]["url"]
                    response_text = f"🔍 I found something:\n*<{url}|{title}>*"
                else:
                    response_text = "🤔 Sorry, I couldn't find anything relevant in the Knowledge Base."
            except Exception as e:
                print(f"❌ Error while querying Vanta: {e}", flush=True)
                response_text = "⚠️ Something went wrong while searching Vanta. Please try again later."

            send_slack_message(channel, response_text)

    except Exception as e:
        print(f"❌ Unexpected error in /slack/events: {e}", flush=True)

    return jsonify({"ok": True})

@app.route("/")
def index():
    return "VantaBot is up and running!"

if __name__ == "__main__":
    print("🚀 Starting VantaBot server...", flush=True)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
