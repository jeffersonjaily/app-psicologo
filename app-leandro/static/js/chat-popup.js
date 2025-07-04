document.addEventListener('DOMContentLoaded', () => {
  const chatPopup = document.getElementById('chat-popup');
  const chatToggle = document.getElementById('chat-toggle');
  const toggleChatBtn = document.getElementById('toggle-chat-btn');
  const input = document.getElementById('user-input');
  const chatBox = document.getElementById('chat-box');

  if (!chatPopup || !chatToggle || !toggleChatBtn || !input || !chatBox) {
    console.error('Algum elemento do chat está faltando no HTML.');
    return;
  }

  function openChat() {
    chatPopup.classList.remove('minimized');
    chatPopup.style.display = 'flex';
    chatToggle.style.display = 'none';
    toggleChatBtn.textContent = '−';
    input.focus();
  }

  function toggleChatMinimize() {
    chatPopup.classList.toggle('minimized');
    toggleChatBtn.textContent = chatPopup.classList.contains('minimized') ? '+' : '−';
  }

  chatToggle.addEventListener('click', openChat);
  toggleChatBtn.addEventListener('click', toggleChatMinimize);

  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') enviarPergunta();
  });

  async function enviarPergunta() {
    const texto = input.value.trim();
    if (!texto) return;

    adicionarMensagem("Você", texto);
    input.value = "...";

    try {
      const response = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: texto })  // <-- chave 'prompt' para o Flask
      });

      if (!response.ok) throw new Error("Erro na resposta do servidor");

      const data = await response.json();
      adicionarMensagem("IA", data.response || "Sem resposta da IA.");
    } catch (e) {
      console.error("Erro no fetch da IA:", e);
      adicionarMensagem("IA", "Erro ao conectar com a IA.");
    }

    input.value = "";
  }

  function adicionarMensagem(remetente, mensagem) {
    const msg = document.createElement("p");
    msg.innerHTML = `<strong>${remetente}:</strong> ${mensagem}`;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // Estado inicial
  chatPopup.style.display = 'none';
  chatToggle.style.display = 'block';
  chatPopup.classList.add('minimized');
});
