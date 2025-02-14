from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Retrieve the API key from environment variables.
GOOGLE_API_KEY = os.getenv("GOOGLE_CLOUD_CHATBOT_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_CLOUD_CHATBOT_API_KEY environment variable not set")

# Set your Dialogflow project details.
PROJECT_ID = "fort-450921"
# For testing, we use a constant session ID; in production, generate a unique one per conversation.
SESSION_ID = "test-session"
LANGUAGE_CODE = "en-US"

# Construct the Dialogflow Detect Intent endpoint URL with your API key as a query parameter.
DIALOGFLOW_ENDPOINT = (
    f"https://dialogflow.googleapis.com/v2/projects/{PROJECT_ID}/agent/sessions/{SESSION_ID}:detectIntent?key={GOOGLE_API_KEY}"
)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Prepare the payload for Dialogflow.
    payload = {
        "queryInput": {
            "text": {
                "text": user_message,
                "languageCode": LANGUAGE_CODE
            }
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Send the request to Dialogflow's Detect Intent API.
        response = requests.post(DIALOGFLOW_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        # Extract the fulfillment text from the response.
        reply = result.get("queryResult", {}).get("fulfillmentText", "")
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
