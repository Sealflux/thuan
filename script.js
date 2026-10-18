const sendButton = document.getElementById("send-button");
const textInput = document.getElementById("text-input");
const messagesEl = document.getElementById("messages");
const loadingEl = document.getElementById("loading");

function addMessage(text, who) {
  const bubble = document.createElement("div");
  bubble.className = who; // "user" or "system"
  bubble.textContent = text;
  messagesEl.appendChild(bubble);
  bubble.scrollIntoView({ behavior: "smooth" });
}

function speak(text) {
    return new Promise((resolve, reject) => {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = "en-US";
        utterance.voice = speechSynthesis.getVoices().find(voice => voice.name === "Google US English") || null;
        utterance.onend = resolve;
        utterance.onerror = reject;
        utterance.rate = 1.0
        utterance.pitch = 1.0
        window.speechSynthesis.speak(utterance);
    })
}

function sendMessage() {
  const text = textInput.value.trim();
  if (!text) return; // empty message? do nothing
  addMessage(text, "user");
  textInput.value = ""; // clear the input
  showReply(text);
}

async function showReply(userText) {
  loadingEl.style.display = "block";

  try {
    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userText }),
    });

    const data = await response.json();
    loadingEl.style.display = "none";

    if (data.error) {
      addMessage("Error: " + data.error, "system");
      return;
    }

    addMessage(data.reply, "system");
    await speak(data.reply);
  } catch (err) {
    loadingEl.style.display = "none";
    addMessage("Couldn't reach the server. Is it running?", "system");
    console.error(err);
  }
}

sendButton.addEventListener("click", sendMessage);

textInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") sendMessage();
});