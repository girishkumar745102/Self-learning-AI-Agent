// EvoMind frontend logic — connects the chat UI to the FastAPI backend

// Backend URL (make sure your uvicorn server is running before opening this page)
const BACKEND_URL = "http://127.0.0.1:8000/chat";

// Grab the HTML elements we need to work with
const chatWindow = document.getElementById("chat-window");
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");
const typingIndicator = document.getElementById("typing-indicator");
const emptyState = document.getElementById("empty-state");
const sessionTag = document.getElementById("session-tag");

// ---- User ID handling ----
// Each browser gets its own random user_id, saved in localStorage.
// This is the "simple version" of multi-user support (no real login yet).
function getUserId() {
  let userId = localStorage.getItem("evomind_user_id");
  if (!userId) {
    userId = "user_" + Math.random().toString(36).substring(2, 12);
    localStorage.setItem("evomind_user_id", userId);
  }
  return userId;
}

const userId = getUserId();
sessionTag.textContent = "session · " + userId;

// ---- Adding messages to the chat window ----
function addMessage(text, sender) {
  // sender is "user", "agent", or "error"

  // Remove the empty state the first time a message is sent
  if (emptyState) {
    emptyState.remove();
  }

  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  messageDiv.appendChild(bubble);
  chatWindow.appendChild(messageDiv);

  // Auto-scroll to the latest message
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

// ---- Sending a message to the backend ----
async function sendMessage(text) {
  typingIndicator.classList.add("active");
  sendBtn.disabled = true;

  try {
    const response = await fetch(BACKEND_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, user_id: userId }),
    });

    const data = await response.json();

    if (data.reply) {
      addMessage(data.reply, "agent");
    } else if (data.error) {
      addMessage(data.error, "error");
    }
  } catch (err) {
    addMessage(
      "Couldn't reach EvoMind's backend. Check that the server is running.",
      "error"
    );
  } finally {
    typingIndicator.classList.remove("active");
    sendBtn.disabled = false;
  }
}

// ---- Handling the form submit (Send button or Enter key) ----
chatForm.addEventListener("submit", (event) => {
  event.preventDefault(); // stop the page from reloading
  const text = messageInput.value.trim();
  if (text === "") return;

  addMessage(text, "user");
  messageInput.value = "";
  sendMessage(text);
});