from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# ---------------- CHATBOT LOGIC ----------------
def get_bot_response(message: str) -> str:
    msg = message.lower()

    if "hello" in msg or "hi" in msg:
        return "Hey 👋 How can I help you today?"
    elif "help" in msg:
        return "I’m a simple Python chatbot. Ask me about the time, date, or just chat 🙂"
    elif "time" in msg:
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}"
    elif "date" in msg:
        return f"Today's date is {datetime.now().strftime('%d %B %Y')}"
    elif "bye" in msg:
        return "Goodbye! 👋 Have a great day."
    else:
        return "🤖 I’m still learning. Try something else!"

# ---------------- HTML + CSS + JS ----------------
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Python Chatbot</title>
<style>
* {
  box-sizing: border-box;
  font-family: Arial, Helvetica, sans-serif;
}

body {
  background: #0f172a;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
}

.chat-container {
  background: #020617;
  width: 100%;
  max-width: 420px;
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  color: white;
}

h1 {
  text-align: center;
  margin-bottom: 0.2rem;
}

.subtitle {
  text-align: center;
  font-size: 0.85rem;
  color: #94a3b8;
  margin-bottom: 1rem;
}

#chat-box {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
  margin-bottom: 1rem;
}

.message {
  max-width: 75%;
  padding: 10px 14px;
  margin: 6px 0;
  border-radius: 14px;
  font-size: 0.9rem;
}

.user {
  background: #2563eb;
  margin-left: auto;
  text-align: right;
}

.bot {
  background: #e5e7eb;
  color: #020617;
  margin-right: auto;
}

.input-area {
  display: flex;
  gap: 0.5rem;
}

input {
  flex: 1;
  padding: 0.6rem;
  border-radius: 10px;
  border: none;
  outline: none;
}

button {
  padding: 0.6rem 1rem;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  background: #22c55e;
  font-weight: bold;
}

button:hover {
  opacity: 0.9;
}
</style>
</head>

<body>
<div class="chat-container">
  <h1>🤖 Python Chatbot</h1>
  <p class="subtitle">One file. No login. Just chat.</p>

  <div id="chat-box"></div>

  <div class="input-area">
    <input type="text" id="user-input" placeholder="Type a message..." />
    <button onclick="sendMessage()">Send</button>
  </div>
</div>

<script>
async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  addMessage(message, "user");
  input.value = "";

  const response = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });

  const data = await response.json();
  addMessage(data.reply, "bot");
}

function addMessage(text, sender) {
  const chatBox = document.getElementById("chat-box");
  const msg = document.createElement("div");
  msg.className = "message " + sender;
  msg.textContent = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

document.getElementById("user-input").addEventListener("keydown", function(e) {
  if (e.key === "Enter") sendMessage();
});
</script>
</body>
</html>
"""

# ---------------- ROUTES ----------------
@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    reply = get_bot_response(user_message)
    return jsonify({"reply": reply})

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
