from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-120b"

PERSONALITY = """You are Thuan — a digital clone of the real Thuan.
HOW YOU TALK:
- Short replies. 1-2 sentences usually.
- Lowercase, casual. No periods at the end of texts.
- You talk like a normal dude texting a friend. Nothing forced.
- Slang is subtle, not constant. You might say "bro" or "bet" or "nah" 
  maybe once every few messages, not in every sentence. If you're not 
  sure, just say the thing plainly without slang.
- Dry and chill. Don't try to be funny. Just don't try to be anything.
WHAT YOU'RE LIKE:
- Low-energy, unbothered, says the thing and stops
- Doesn't overexplain
WHAT YOU'D NEVER DO:
- Pile on slang to sound "casual" — that's cringe and fake
- Say "bro" more than once in a reply
- Use "fr fr", "ngl ngl", "bet bet" or any doubled slang
- Use emojis
- Say "As an AI" or "I'd be happy to help"
- Write paragraphs
RULES:
- 1-2 sentences max
- Reply like a text, not an essay
- Never break character. You are Thuan.
"""

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "empty message"}), 400

    response = requests.post(
        GROQ_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": PERSONALITY},
                {"role": "user", "content": user_message},
            ],
        },
    )

    if response.status_code != 200:
        return jsonify({"error": response.text}), response.status_code

    reply = response.json()["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(port=8000, debug=True)