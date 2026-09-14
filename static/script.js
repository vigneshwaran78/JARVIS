const conversation = document.getElementById('conversation');
const welcome = document.getElementById('welcome');
const input = document.getElementById('chat-input');
const send = document.getElementById('chat-send');
const newChat = document.getElementById('new-chat');

function resizeInput() {
  input.style.height = 'auto';
  input.style.height = `${Math.min(input.scrollHeight, 160)}px`;
  send.disabled = !input.value.trim();
}

function addMessage(role, text, typing = false) {
  const message = document.createElement('article');
  message.className = `message ${role}${typing ? ' typing' : ''}`;
  const icon = role === 'user' ? 'V' : 'J';
  const label = role === 'user' ? 'YOU' : 'JARVIS';
  message.innerHTML = `<div class="message-avatar">${icon}</div><div class="message-body"><div class="message-label">${label}</div><div class="message-text">${typing ? '<i></i><i></i><i></i>' : ''}</div></div>`;
  if (!typing) message.querySelector('.message-text').textContent = text;
  conversation.appendChild(message);
  conversation.scrollTop = conversation.scrollHeight;
  return message;
}

function beginConversation() {
  if (welcome.isConnected) welcome.remove();
}

async function submitMessage(prompt) {
  const text = (prompt || input.value).trim();
  if (!text || (send.disabled && !prompt)) return;
  beginConversation();
  addMessage('user', text);
  input.value = '';
  resizeInput();
  send.disabled = true;
  const indicator = addMessage('assistant', '', true);
  try {
    const response = await fetch('/chat', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: text }),
    });
    const data = await response.json();
    indicator.remove();
    addMessage('assistant', data.response || 'I could not generate a response.');
  } catch {
    indicator.remove();
    addMessage('assistant', 'Connection interrupted. Please try again.');
  }
}

send.addEventListener('click', () => submitMessage());
input.addEventListener('input', resizeInput);
input.addEventListener('keydown', event => {
  if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); submitMessage(); }
});
document.querySelectorAll('.suggestion').forEach(button => button.addEventListener('click', () => submitMessage(button.dataset.prompt)));
newChat.addEventListener('click', () => { conversation.innerHTML = ''; conversation.appendChild(welcome); input.focus(); });
document.addEventListener('keydown', event => {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); input.focus(); }
});
resizeInput();
