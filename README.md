# thuan

A clone of me. Talks like me, sounds like me, answers like me.

Built for Terra - Hack Club

## What it does

- You type a message
- It replies in my personality (using OpenAi's flagship open-weight LLM with 120 billion parameters)
- It speaks the reply in my cloned voice (using Fish Audio)

## Try it yourself

You can absolutely clone this repo and make your own version. You'll need:

- **Groq API key** (free) — for the brain — https://console.groq.com
- **Fish Audio API key** (free tier) — for the voice — https://fish.audio

Both have free tiers that are enough for personal projects(Please don't spend money for no reason!)

## Setup

1. Clone the repo
git clone https://github.com/YOUR_USERNAME/thuan.git

2. Get API Keys
Put it in a .env file so you don't expose your api keys
3. Install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install flask flask-cors python-dotenv requests
4. Run the backend
python server.py
5. Run the frontend
Open index.html with LiveServer in VsCode



## How it works
The Browser takes in your reply/message, which then is fed into the model, afterwards, the model's reply is shown onto the screen alongwith the reply being fed into the voice model which then returns a mp3 which is then played.
The personality of the model and its rules is in server.py, you can naturally change it if you want to.
