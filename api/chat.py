from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Retrieve the API key from environment variables.
# Ensure that in your Vercel project settings (or local .env file) you define:
#   GOOGLE_CLOUD_CHATBOT_API_KEY = your_api_key_here
API_KEY = os.getenv("GOOGLE_CLOUD_CHATBOT_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_CLOUD_CHATBOT_API_KEY environment variable not set")

# Your Dialogflow project details:
PROJECT_ID = "fort-450921"
# For testing, you can use a constant session ID.
# In production, generate a unique session ID per conversation.
SESSION_ID = "test-session"
LANGUAGE_CODE = "en-US"

DIALOGFLOW_ENDPOINT = (
    f"https://dialogflow.googleapis.com/v2/projects/{PROJECT_ID}/agent/sessions/{SESSION_ID}:detectIntent"
)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    payload = {
        "queryInput": {
            "text": {
                "text": user_message,
                "languageCode": LANGUAGE_CODE
            }
        }
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(DIALOGFLOW_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        reply = result.get("queryResult", {}).get("fulfillmentText", "")
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
