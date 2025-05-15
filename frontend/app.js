
const API_URL = "http://localhost:3001/messages";

async function loadMessages() {
  const res = await fetch(API_URL);
  const data = await res.json();
  const list = document.getElementById("messages");
  list.innerHTML = "";
  data.forEach(m => {
    const li = document.createElement("li");
    li.textContent = `${m.content} (${new Date(m.created_at).toLocaleString()})`;
    list.appendChild(li);
  });
}

async function addMessage() {
  const input = document.getElementById("content");
  const content = input.value;
  if (!content) return;

  await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content })
  });

  input.value = "";
  loadMessages();
}
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("message-form").addEventListener("submit", addMessage);
  loadMessages();
});
