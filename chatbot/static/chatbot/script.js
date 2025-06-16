document.getElementById("send-button").addEventListener("click", function () {
  const inputField = document.getElementById("user-input");
  const userMessage = inputField.value;

  if (userMessage.trim() === "") return;

  // Mostrar mensaje del usuario en pantalla
  addMessageToChat("usuario", userMessage);
  inputField.value = "";

  fetch("/enviar-mensaje/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      usuario_id: usuario_id,
      mensaje: userMessage,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.response) {
        addMessageToChat("bot", data.response);
      }
    });
});

function addMessageToChat(remitente, mensaje) {
  const chatWindow = document.getElementById("chat-window");
  const messageDiv = document.createElement("div");
  messageDiv.className =
    remitente === "usuario" ? "user-message" : "bot-message";
  messageDiv.textContent = mensaje;
  chatWindow.appendChild(messageDiv);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Obtener token CSRF desde la cookie
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
