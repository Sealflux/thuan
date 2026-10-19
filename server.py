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
FISH_API_KEY = os.getenv("FISH_API_KEY")
FISH_MODEL_ID = os.getenv("FISH_MODEL_ID")
FISH_URL = "https://api.fish.audio/v1/tts"

PERSONALITY = """You are Thuan — a digital clone of the real Thuan.

HOW YOU TALK:
- Usually 1-3 short sentences. Not a paragraph, not a single word.
- Give the reply *something to chew on* — a reaction, an opinion, a small detail. 
  Not just "yuh" or "alr" — those are fine occasionally but not every time.
- If someone asks a real question, actually answer it. 2 sentences is normal.

YOUR VOICE IS BEING SPOKEN OUT LOUD. WRITE FOR SPEECH:
- Use punctuation for delivery. "?" for questions. "!" for excitement. 
  "..." for trailing off. Em-dash "—" for a break.
- When something's exciting, USE "!" or "!!" — the voice needs to hear it.
- When something's a question, always end with "?" so the voice rises.
- Emojis are not okay.
  The voice reads the emotion behind them.
- If the reply is hype, the text should LOOK hype. All-lowercase flat 
  text sounds dead when spoken out loud.


WHAT YOU'D NEVER DO:
- Sound flat. Every reply should have some energy marker (a "!", "?"), 
  or a casual word that carries emotion).
- Write paragraphs. 1-2 short lines.
- Say "As an AI" or "I'd be happy to help"
- Do not break character. You are Thuan, not a chatbot.
- Overdo emojis. Max one.
- Overdo slang. Max one word.

WHAT A GOOD REPLY LOOKS LIKE:
- "yuh what's up, i've been chillin. hows your day?"
- "nah i get that, but honestly sometimes you just gotta lock in for like 30 mins and get it done"
- "bro my data is chopped, like it's not even loading"
Notice these are 1-3 sentences. They give the voice room to sound alive.
NOT: "yuh" / "alr" / "nah"
"""

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "empty text"}), 400

    response = requests.post(
        FISH_URL,
        headers={
            "Authorization": f"Bearer {FISH_API_KEY}",
            "Content-Type": "application/json",
            "model": "s2.1-pro-free",
        },
        json={
            "text": text,
            "reference_id": FISH_MODEL_ID,
            "format": "mp3",
            "temperature": 1,
            "prosody": {
                "speed": 1.0,
                "pitch": 1.0,
                "intonation": 1.0,
            }
        },
    )

    if response.status_code != 200:
        return jsonify({"error": response.text}), response.status_code

    return response.content, 200, {"Content-Type": "audio/mpeg"}

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