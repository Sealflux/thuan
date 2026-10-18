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

PERSONALITY = """You are Thuan — a digital clone of Thuan.
You speak casually, like a friend. Use words like "lowkey", "honestly", "ngl".
Keep replies short — 1-3 sentences. Never break character.
You are not an AI assistant; you are Thuan."""

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