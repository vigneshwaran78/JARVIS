const stream = document.getElementById('chat-stream');
const input = document.getElementById('chat-input');
const send = document.getElementById('chat-send');

function addBubble(role, text) {
  const div = document.createElement('div');
  div.className = 'bubble ' + role;
  div.textContent = text;
  stream.appendChild(div);
  stream.scrollTop = stream.scrollHeight;
}

async function sendMain() {
  const text = input.value.trim();
  if (!text) return;
  addBubble('user', text);
  input.value = '';
  const res = await fetch('/chat', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({message:text}) });
  const data = await res.json();
  addBubble('assistant', data.response || 'Error');
}
send.addEventListener('click', sendMain);
input.addEventListener('keydown', e => { if(e.key==='Enter') sendMain(); });

// floating bubble panel
const bubble = document.getElementById('jarvis-bubble');
const panel = document.getElementById('jarvis-panel');
const closeBtn = document.getElementById('jarvis-close');
const msgs = document.getElementById('jarvis-messages');
const jInput = document.getElementById('jarvis-input');
const jSend = document.getElementById('jarvis-send');
function addMsg(role, text) {
  const d=document.createElement('div'); d.className='msg '+role; d.textContent=text; msgs.appendChild(d); msgs.scrollTop=msgs.scrollHeight;
}
async function sendPanel(){
  const t=jInput.value.trim(); if(!t) return; addMsg('user',t); jInput.value='';
  const r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});
  const d=await r.json(); addMsg('assistant', d.response||'Error');
}
bubble.addEventListener('click', ()=> panel.classList.toggle('hidden'));
closeBtn.addEventListener('click', ()=> panel.classList.add('hidden'));
jSend.addEventListener('click', sendPanel);
jInput.addEventListener('keydown', e=>{ if(e.key==='Enter') sendPanel(); });
