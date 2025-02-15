import logging
import os
from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file if present.
load_dotenv()

# Set up verbose logging with timestamps.
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

app = Flask(__name__)

# Retrieve the OpenAI API key from environment variables.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logging.error("OPENAI_API_KEY environment variable not set")
    raise ValueError("OPENAI_API_KEY environment variable not set")
else:
    logging.debug("OPENAI_API_KEY is set.")

# Configure OpenAI with your API key.
client = OpenAI(api_key=OPENAI_API_KEY)

# Browser-friendly GET route that serves a simple HTML page with a chatbox.
@app.route('/', methods=['GET'])
def index():
    html = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>Fort Chatbot</title>
        <style>
          body { font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 40px; }
          .container { max-width: 600px; margin: auto; background: #fff; padding: 20px; border-radius: 8px; }
          #chat-log { border: 1px solid #ccc; padding: 10px; height: 300px; overflow-y: auto; margin-bottom: 10px; background-color: #fafafa; }
          input[type="text"] { width: 80%; padding: 10px; }
          button { padding: 10px; }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>Fort Chatbot</h1>
          <div id="chat-log"></div>
          <form id="chat-form">
            <input type="text" id="chat-input" placeholder="Type your message..." autocomplete="off"/>
            <button type="submit">Send</button>
          </form>
        </div>
        <script>
          const chatForm = document.getElementById('chat-form');
          const chatInput = document.getElementById('chat-input');
          const chatLog = document.getElementById('chat-log');

          chatForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const message = chatInput.value;
            if (!message.trim()) return;
            // Append user's message to chat log.
            const userMsgElem = document.createElement('div');
            userMsgElem.className = 'text-right mb-2';
            userMsgElem.textContent = "You: " + message;
            chatLog.appendChild(userMsgElem);
            chatInput.value = '';

            try {
              const res = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
              });
              const data = await res.json();
              if (data.reply) {
                const botMsgElem = document.createElement('div');
                botMsgElem.className = 'text-left mb-2';
                botMsgElem.textContent = "Fort Bot: " + data.reply;
                chatLog.appendChild(botMsgElem);
              } else {
                const errorElem = document.createElement('div');
                errorElem.className = 'text-left mb-2 text-red-500';
                errorElem.textContent = "Error: " + (data.error || 'Unknown error');
                chatLog.appendChild(errorElem);
              }
            } catch (err) {
              const errorElem = document.createElement('div');
              errorElem.className = 'text-left mb-2 text-red-500';
              errorElem.textContent = "Error: " + err.message;
              chatLog.appendChild(errorElem);
            }
            chatLog.scrollTop = chatLog.scrollHeight;
          });
        </script>
      </body>
    </html>
    """
    return render_template_string(html)

# POST route to handle chat requests.
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    logging.debug("Received message: %s", user_message)

    if not user_message:
        logging.error("No message provided")
        return jsonify({"error": "No message provided"}), 400

    try:
        # Call OpenAI's ChatCompletion API with a system prompt to define Fort Bot's personality.
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Fort Bot, a friendly chatbot for a free non-profit organization called Fort. "
                        "Your goal is to help educate and support users. If you detect any illegal activity, inform the appropriate authorities. "
                        "Always refer to yourself as Fort Bot."
                    )
                },
                {"role": "user", "content": user_message}
            ],
            temperature=0.9,
            max_tokens=1500
        )
        reply = response.choices[0].message.content
        logging.debug("Reply extracted: %s", reply)
        return jsonify({"reply": reply})
    except Exception as e:
        logging.exception("Error during API call")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logging.info("Starting Fort Chatbot Flask server...")
    app.run(debug=True)
