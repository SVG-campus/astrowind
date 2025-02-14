from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name__)

# Retrieve the API key from environment variables.
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")

# Set your Dialogflow or OpenAI details:
PROJECT_ID = "fort-450921"
# For testing, using a constant session ID; in production, generate a unique session ID per conversation.
SESSION_ID = "test-session"
LANGUAGE_CODE = "en-US"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Use OpenAI ChatCompletion API with a system prompt to enforce Fort Bot's personality.
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                  "role": "system", 
                  "content": "You are Fort Bot, a friendly, helpful chatbot for a free non-profit. You assist users with educational and support-related inquiries and always refer to yourself as Fort Bot. If you detect illegal activity, inform the appropriate authorities."
                },
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=150,
        )
        reply = response.choices[0].message['content']
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
