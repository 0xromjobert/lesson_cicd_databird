
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

async function addMessage(event) {
  event.preventDefault();
  console.log("in the addmessenge event");
  const input = document.getElementById("content");
  const content = input.value;
  if (!content) return;

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content })
    });

    if (!response.ok) {
      throw new Error("Erreur lors de l'envoi du message.");
    }

    input.value = "";
    loadMessages();
  } catch (err) {
    alert(err.message || "Une erreur est survenue.");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("message-form").addEventListener("submit", addMessage);
  loadMessages();
});
