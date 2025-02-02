from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Ensure you set your OpenAI API key in an environment variable.
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_message}],
            temperature=0.7,
            max_tokens=1500,
        )
        reply = response.choices[0].message['content']
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
