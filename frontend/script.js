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
function addMessage(text, sender, shouldSpeak = false) {
  const currentEmptyState = document.querySelector(".empty-state");
  if (currentEmptyState) {
    currentEmptyState.remove();
  }

  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  messageDiv.appendChild(bubble);
  chatWindow.appendChild(messageDiv);

  chatWindow.scrollTop = chatWindow.scrollHeight;

  if (sender === "agent" && shouldSpeak){
    speakText(text);
  }
}

// ---- Sending a message to the backend ----
async function sendMessage(text, isVoiceInput = false) {
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
      addMessage(data.reply, "agent" , isVoiceInput);
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
  event.preventDefault();
  const text = messageInput.value.trim();
  if (text === "") return;

  addMessage(text, "user");
  messageInput.value = "";
  sendMessage(text);
});

// ---- Menu dropdown ----
const menuBtn = document.getElementById("menu-btn");
const dropdownMenu = document.getElementById("dropdown-menu");
const menuTheme = document.getElementById("menu-theme");
const menuNewChat = document.getElementById("menu-new-chat");
const menuHistory = document.getElementById("menu-history");

menuBtn.addEventListener("click", (event) => {
  event.stopPropagation();
  dropdownMenu.classList.toggle("open");
});

document.addEventListener("click", () => {
  dropdownMenu.classList.remove("open");
});

// ---- Theme toggle ----
function applyTheme(theme) {
  document.body.classList.toggle("light-theme", theme === "light");
  localStorage.setItem("evomind_theme", theme);
}

const savedTheme = localStorage.getItem("evomind_theme") || "dark";
applyTheme(savedTheme);

menuTheme.addEventListener("click", () => {
  const isLight = document.body.classList.contains("light-theme");
  applyTheme(isLight ? "dark" : "light");
});

// ---- New chat (visual reset for now) ----
menuNewChat.addEventListener("click", () => {
  chatWindow.innerHTML = "";
  const freshEmptyState = document.createElement("div");
  freshEmptyState.className = "empty-state";
  freshEmptyState.innerHTML = `
    <p class="empty-title">New chat started</p>
    <p class="empty-sub">Note: EvoMind still remembers earlier facts from this session — full separate chat history is coming soon.</p>
  `;
  chatWindow.appendChild(freshEmptyState);
});

// ---- History (placeholder) ----
menuHistory.addEventListener("click", () => {
  alert("Chat history is coming soon — this will let you revisit past conversations once accounts are added.");
});

// ---- Voice recording (Speech-to-Text) ----
const micBtn = document.getElementById("mic-btn");
let mediaRecorder;
let audioChunks = [];
let isRecording = false;

micBtn.addEventListener("click", async () => {
  if (!isRecording) {
    // Start recording
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      audioChunks = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
        await sendAudioToBackend(audioBlob);
      };

      mediaRecorder.start();
      isRecording = true;
      micBtn.classList.add("recording");
    } catch (err) {
      addMessage("Microphone access denied or unavailable.", "error");
    }
  } else {
    // Stop recording
    mediaRecorder.stop();
    isRecording = false;
    micBtn.classList.remove("recording");
  }
});

async function sendAudioToBackend(audioBlob) {
  typingIndicator.classList.add("active");

  try {
    const formData = new FormData();
    formData.append("audio", audioBlob, "recording.webm");

    const response = await fetch("http://127.0.0.1:8000/transcribe", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    const transcribedText = data.text.trim();

    if (transcribedText) {
      addMessage(transcribedText, "user");
      await sendMessage(transcribedText, true);
    }
  } catch (err) {
    addMessage("Couldn't transcribe audio. Please try again.", "error");
    typingIndicator.classList.remove("active");
  }
}

// ---- Text-to-Speech (agent speaks its replies) ----
function speakText(text) {
  if (!window.speechSynthesis) return;

  window.speechSynthesis.cancel(); // stop any previous speech first
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = 1;
  utterance.pitch = 1;
  window.speechSynthesis.speak(utterance);
}



