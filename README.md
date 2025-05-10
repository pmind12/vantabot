# 🤖 VantaBot – Slack Security Knowledge Bot

**VantaBot** is a Slack-integrated assistant that helps employees get quick, accurate answers to security and compliance-related questions. It connects directly to your company's Knowledge Base in **Vanta**, so everyone can easily find relevant information without needing to ask the security team directly.

---

## 🧩 Features

- 💬 Ask questions in Slack (e.g. _"How do we handle data encryption?"_)
- 🔍 The bot queries your **Vanta Knowledge Base** articles via API
- 🧠 Optional: use OpenAI to improve natural language understanding
- ✅ Reduces repetitive questions to the security team
- 🔐 Keeps employees aligned with security and compliance practices

---

## 🚀 Deploying with Render.com

### 1. Prepare your repository

Your project should include:
- `app.py` – Flask-based backend
- `requirements.txt` – Python dependencies
- `Procfile` – startup command for Render
- `README.md` – this file

### 2. Deploy on Render

1. Sign up at [https://render.com](https://render.com)
2. Connect your GitHub repo
3. Create a new **Web Service**:
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `python app.py`
   - Select "Free" or "Starter" plan
   - Note your Render URL (e.g. `https://vanta-kb-bot.onrender.com`)

---

## 🔐 Slack Bot Configuration

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Create a new app
3. Under **OAuth & Permissions**, add these scopes:
   - `app_mentions:read`
   - `chat:write`
   - `commands` (optional for future slash commands)

4. Under **Event Subscriptions**:
   - Enable events
   - Set your Request URL: `https://<your-render-url>/slack/events`
   - Subscribe to: `app_mention`

5. Install the bot to your workspace and copy your `SLACK_BOT_TOKEN`

---

## 🔐 Vanta API Access

1. Log into your Vanta account
2. Go to **Settings > Developer Console**
3. Create an API key with access to your **Knowledge Base**
4. Store it securely as `VANTA_API_KEY` in Render's environment variables

---

## ⚙️ Environment Variables

| Variable Name       | Description                                      |
|---------------------|--------------------------------------------------|
| `SLACK_BOT_TOKEN`   | Your Slack Bot Token (`xoxb-...`)                |
| `VANTA_API_KEY`     | Vanta API key with read access to the KB         |
| `OPENAI_API_KEY`    | *(Optional)* For better NLP question handling    |

---

## 🛠️ Roadmap (Next Steps)

- ✅ Basic query handling from Slack
- 🧠 Add OpenAI integration for flexible language input
- 🧾 Handle article search and fallback gracefully
- 📚 Log most-asked questions for FAQ optimization

---

## 📎 Example Questions

- “How do we manage user access?”
- “What’s our data retention policy?”
- “Are we HIPAA compliant?”
- “How are backups encrypted?”

---

Made with ❤️ to help reduce repetitive security questions.
