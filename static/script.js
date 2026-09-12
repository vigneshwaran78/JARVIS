const bubble = document.getElementById('jarvis-bubble');
const panel = document.getElementById('jarvis-panel');
const closeBtn = document.getElementById('jarvis-close');
const messages = document.getElementById('jarvis-messages');
const input = document.getElementById('jarvis-input');
const send = document.getElementById('jarvis-send');

function addMsg(role, text) {
  const div = document.createElement('div');
  div.className = 'msg ' + role;
  div.textContent = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;
  addMsg('user', text);
  input.value = '';
  const res = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: text })
  });
  const data = await res.json();
  addMsg('assistant', data.response || 'Error');
}

bubble.addEventListener('click', () => panel.classList.toggle('hidden'));
closeBtn.addEventListener('click', () => panel.classList.add('hidden'));
send.addEventListener('click', sendMessage);
input.addEventListener('keydown', (e) => { if (e.key === 'Enter') sendMessage(); });
