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

function sendMessage() {
  const text = textInput.value.trim();
  if (!text) return; // empty message? do nothing
  addMessage(text, "user");
  textInput.value = ""; // clear the input
  showReply();
}

function showReply() {
  loadingEl.style.display = "block";

  setTimeout(() => {
    loadingEl.style.display = "none";
    addMessage("I heard you. (AI coming soon.)", "system");
  }, 1200); // 1200ms = 1.2 seconds
}

sendButton.addEventListener("click", sendMessage);

textInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") sendMessage();
});