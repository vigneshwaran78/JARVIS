/**
 * JARVIS — STARK MARK VII INTELLIGENT INTERFACE SCRIPT
 * Handles markdown rendering, speech synthesis/recognition,
 * multi-theme switching, memory inspector, telemetry, and interactions.
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const conversation = document.getElementById('conversation');
  const welcome = document.getElementById('welcome');
  const chatInput = document.getElementById('chat-input');
  const chatSend = document.getElementById('chat-send');
  const newChatBtn = document.getElementById('new-chat');
  const timeGreeting = document.getElementById('time-greeting');
  const activeModelName = document.getElementById('active-model-name');
  const memoryCountBadge = document.getElementById('memory-count-badge');
  const themeBtn = document.getElementById('theme-btn');
  const ttsToggleBtn = document.getElementById('tts-toggle-btn');
  const ttsIcon = document.getElementById('tts-icon');
  const audioQuickToggle = document.getElementById('audio-quick-toggle');
  const voiceInputBtn = document.getElementById('voice-input-btn');
  const listeningWave = document.getElementById('listening-wave');
  const shareBtn = document.getElementById('share-btn');
  const mobileMenuBtn = document.getElementById('mobile-menu');
  const sidebar = document.getElementById('sidebar');
  const sidebarBackdrop = document.getElementById('sidebar-backdrop');
  const navChat = document.getElementById('nav-chat');
  const navMemory = document.getElementById('nav-memory');
  const navWorkspace = document.getElementById('nav-workspace');
  const memoryDrawer = document.getElementById('memory-drawer');
  const memoryCloseBtn = document.getElementById('memory-close-btn');
  const clearMemoryBtn = document.getElementById('clear-memory-btn');
  const memoryCardsContainer = document.getElementById('memory-cards-container');
  const memStatCount = document.getElementById('mem-stat-count');
  const workspaceModal = document.getElementById('workspace-modal');
  const workspaceCloseBtn = document.getElementById('workspace-close-btn');
  const toastContainer = document.getElementById('toast-container');
  const composerCmdBtn = document.getElementById('composer-cmd-btn');
  const diagModel = document.getElementById('diag-model');
  const diagSpeech = document.getElementById('diag-speech');

  // State
  let voiceReadoutEnabled = localStorage.getItem('jarvis-tts') === 'true';
  let isListening = false;
  let speechRecognition = null;
  let messageHistory = [];

  // 1. Dynamic Time-based Greeting
  function updateGreeting() {
    if (!timeGreeting) return;
    const hour = new Date().getHours();
    let greet = 'GOOD EVENING, VICKIE';
    if (hour >= 5 && hour < 12) greet = 'GOOD MORNING, VICKIE';
    else if (hour >= 12 && hour < 17) greet = 'GOOD AFTERNOON, VICKIE';
    timeGreeting.textContent = greet;
  }
  updateGreeting();

  // 2. Theme Management
  const themes = ['theme-obsidian', 'theme-arc', 'theme-crimson'];
  const themeNames = {
    'theme-obsidian': 'Stark Obsidian',
    'theme-arc': 'Arc Reactor (Cyan)',
    'theme-crimson': 'Mark Armor (Crimson)'
  };

  let savedTheme = localStorage.getItem('jarvis-theme') || 'theme-obsidian';
  if (!themes.includes(savedTheme)) savedTheme = 'theme-obsidian';
  document.body.className = savedTheme;

  function cycleTheme() {
    const currentIdx = themes.indexOf(document.body.className);
    const nextIdx = (currentIdx + 1) % themes.length;
    const nextTheme = themes[nextIdx];
    document.body.className = nextTheme;
    localStorage.setItem('jarvis-theme', nextTheme);
    showToast(`Theme switched to ${themeNames[nextTheme]}`);
  }
  if (themeBtn) themeBtn.addEventListener('click', cycleTheme);

  // 3. Toast Notifications
  function showToast(message, duration = 3000) {
    if (!toastContainer) return;
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<span style="color:var(--accent-primary)">⚡</span><span>${escapeHtml(message)}</span>`;
    toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      setTimeout(() => toast.remove(), 300);
    }, duration);
  }

  // 4. Markdown & Code Highlighting Parser
  function escapeHtml(str) {
    if (typeof str !== 'string') return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function renderContent(rawText) {
    // If Marked is available from CDN, use it
    if (typeof marked !== 'undefined') {
      try {
        const parsed = marked.parse(rawText, { gfm: true, breaks: true });
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = parsed;

        // Enhance pre code blocks with headers and copy buttons
        tempDiv.querySelectorAll('pre code').forEach((codeEl) => {
          const pre = codeEl.parentElement;
          const langMatch = (codeEl.className || '').match(/language-([a-zA-Z0-9_-]+)/);
          const lang = langMatch ? langMatch[1].toUpperCase() : 'CODE';

          // Apply highlight.js if available
          if (typeof hljs !== 'undefined') {
            try { hljs.highlightElement(codeEl); } catch (e) {}
          }

          const wrap = document.createElement('div');
          wrap.className = 'code-block-wrap';
          wrap.innerHTML = `
            <div class="code-header">
              <span>${lang}</span>
              <button class="copy-code-btn" type="button">📋 Copy Code</button>
            </div>
          `;
          pre.parentNode.insertBefore(wrap, pre);
          wrap.appendChild(pre);

          const copyBtn = wrap.querySelector('.copy-code-btn');
          copyBtn.addEventListener('click', () => {
            navigator.clipboard.writeText(codeEl.textContent).then(() => {
              copyBtn.textContent = '✓ Copied!';
              setTimeout(() => { copyBtn.textContent = '📋 Copy Code'; }, 2000);
            });
          });
        });

        return tempDiv.innerHTML;
      } catch (e) {
        console.error('Markdown rendering error, falling back:', e);
      }
    }

    // Fallback parser if offline or Marked fails
    let text = escapeHtml(rawText);
    // Code blocks
    text = text.replace(/```([a-zA-Z0-9_-]*)\n([\s\S]*?)```/g, (match, lang, code) => {
      const displayLang = lang ? lang.toUpperCase() : 'CODE';
      return `
        <div class="code-block-wrap">
          <div class="code-header">
            <span>${displayLang}</span>
            <button class="copy-code-btn" type="button" onclick="navigator.clipboard.writeText(this.closest('.code-block-wrap').querySelector('code').textContent).then(()=>{this.textContent='✓ Copied!';setTimeout(()=>this.textContent='📋 Copy Code',2000)})">📋 Copy Code</button>
          </div>
          <pre><code>${code.trim()}</code></pre>
        </div>
      `;
    });
    // Inline code
    text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
    // Bold
    text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    // Italics
    text = text.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    // Line breaks
    text = text.replace(/\n/g, '<br/>');
    return text;
  }

  // 5. Text-To-Speech (TTS)
  function updateTtsUi() {
    const icon = voiceReadoutEnabled ? '🔊' : '🔇';
    if (ttsIcon) ttsIcon.textContent = icon;
    if (audioQuickToggle) audioQuickToggle.textContent = icon;
    localStorage.setItem('jarvis-tts', voiceReadoutEnabled);
  }
  updateTtsUi();

  function toggleVoiceReadout() {
    voiceReadoutEnabled = !voiceReadoutEnabled;
    updateTtsUi();
    if (voiceReadoutEnabled) {
      showToast('Voice readout enabled');
      speakText("JARVIS audio system online.");
    } else {
      window.speechSynthesis.cancel();
      showToast('Voice readout muted');
    }
  }

  if (ttsToggleBtn) ttsToggleBtn.addEventListener('click', toggleVoiceReadout);
  if (audioQuickToggle) audioQuickToggle.addEventListener('click', toggleVoiceReadout);

  function speakText(text) {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel(); // Stop any previous speech
    const cleanText = text.replace(/```[\s\S]*?```/g, 'Code block omitted.')
                          .replace(/[#*`_~]/g, '')
                          .trim();
    if (!cleanText) return;

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 1.05;
    utterance.pitch = 1.0;

    // Try finding an English voice (e.g. Daniel, Google UK, Samantha)
    const voices = window.speechSynthesis.getVoices();
    const jarvisVoice = voices.find(v => v.name.includes('Daniel') || v.name.includes('Google UK') || (v.lang.startsWith('en') && v.name.includes('Natural')));
    if (jarvisVoice) utterance.voice = jarvisVoice;

    window.speechSynthesis.speak(utterance);
  }

  // 6. Speech-to-Text (STT)
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRecognition) {
    speechRecognition = new SpeechRecognition();
    speechRecognition.continuous = false;
    speechRecognition.interimResults = true;
    speechRecognition.lang = 'en-US';

    speechRecognition.onstart = () => {
      isListening = true;
      if (listeningWave) listeningWave.classList.remove('hidden');
      if (voiceInputBtn) voiceInputBtn.classList.add('mic-active');
    };

    speechRecognition.onresult = (event) => {
      let transcript = '';
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        transcript += event.results[i][0].transcript;
      }
      chatInput.value = transcript;
      resizeInput();
    };

    speechRecognition.onerror = (event) => {
      console.warn('Speech recognition error:', event.error);
      stopListening();
      if (event.error !== 'no-speech') {
        showToast(`Mic error: ${event.error}`);
      }
    };

    speechRecognition.onend = () => {
      stopListening();
      if (chatInput.value.trim()) {
        submitMessage();
      }
    };

    if (diagSpeech) diagSpeech.textContent = 'SpeechRecognition Online';
  } else {
    if (diagSpeech) diagSpeech.textContent = 'Not Supported';
    if (voiceInputBtn) voiceInputBtn.title = 'SpeechRecognition not supported in this browser';
  }

  function toggleListening() {
    if (!speechRecognition) {
      showToast('Speech-to-text is not supported in this browser.');
      return;
    }
    if (isListening) {
      speechRecognition.stop();
    } else {
      try {
        speechRecognition.start();
      } catch (e) {
        console.error('Speech recognition start failed:', e);
      }
    }
  }

  function stopListening() {
    isListening = false;
    if (listeningWave) listeningWave.classList.add('hidden');
    if (voiceInputBtn) voiceInputBtn.classList.remove('mic-active');
  }

  if (voiceInputBtn) voiceInputBtn.addEventListener('click', toggleListening);

  // 7. Input Auto-Resize & Sending
  function resizeInput() {
    chatInput.style.height = 'auto';
    chatInput.style.height = `${Math.min(chatInput.scrollHeight, 180)}px`;
    chatSend.disabled = !chatInput.value.trim();
  }

  chatInput.addEventListener('input', resizeInput);
  chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      submitMessage();
    }
  });

  // 8. Message Presentation
  function getTimeString() {
    const d = new Date();
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  function addMessage(role, text, typing = false) {
    const message = document.createElement('article');
    message.className = `message ${role}${typing ? ' typing' : ''}`;

    const icon = role === 'user' ? 'V' : 'J';
    const label = role === 'user' ? 'YOU' : 'JARVIS';
    const timeStr = getTimeString();

    let bubbleContent = '';
    if (typing) {
      bubbleContent = `
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
      `;
    } else {
      bubbleContent = renderContent(text);
    }

    let actionsHtml = '';
    if (!typing && role === 'assistant') {
      actionsHtml = `
        <div class="message-actions">
          <button class="msg-action-btn copy-msg-btn" title="Copy full response">📋 Copy</button>
          <button class="msg-action-btn speak-msg-btn" title="Read aloud">🔊 Listen</button>
        </div>
      `;
    }

    message.innerHTML = `
      <div class="message-avatar">${icon}</div>
      <div class="message-body">
        <div class="message-header">
          <span class="message-label">${label}</span>
          <span class="message-time">${timeStr}</span>
        </div>
        <div class="message-bubble">${bubbleContent}</div>
        ${actionsHtml}
      </div>
    `;

    // Wire message action buttons
    if (!typing && role === 'assistant') {
      const copyBtn = message.querySelector('.copy-msg-btn');
      if (copyBtn) {
        copyBtn.addEventListener('click', () => {
          navigator.clipboard.writeText(text).then(() => {
            copyBtn.textContent = '✓ Copied';
            setTimeout(() => { copyBtn.textContent = '📋 Copy'; }, 2000);
          });
        });
      }

      const speakBtn = message.querySelector('.speak-msg-btn');
      if (speakBtn) {
        speakBtn.addEventListener('click', () => {
          speakText(text);
        });
      }
    }

    conversation.appendChild(message);
    conversation.scrollTop = conversation.scrollHeight;
    return message;
  }

  function beginConversation() {
    if (welcome && welcome.isConnected) {
      welcome.remove();
    }
  }

  // 9. Send & Receive Message
  async function submitMessage(customPrompt) {
    const text = (customPrompt || chatInput.value).trim();
    if (!text) return;

    beginConversation();
    addMessage('user', text);
    messageHistory.push({ role: 'user', content: text });

    chatInput.value = '';
    resizeInput();
    chatSend.disabled = true;

    const typingIndicator = addMessage('assistant', '', true);

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });

      const data = await response.json();
      typingIndicator.remove();

      const reply = data.response || 'I could not generate a response.';
      addMessage('assistant', reply);
      messageHistory.push({ role: 'assistant', content: reply });

      // If voice readout is enabled, speak response
      if (voiceReadoutEnabled) {
        speakText(reply);
      }

      // Refresh memory counter
      fetchTelemetry();
    } catch (err) {
      typingIndicator.remove();
      const errReply = 'Connection interrupted or server error. Please retry.';
      addMessage('assistant', errReply);
      console.error('Chat error:', err);
    }
  }

  chatSend.addEventListener('click', () => submitMessage());

  // 10. Suggestions & Quick Chips
  document.querySelectorAll('.suggestion').forEach(button => {
    button.addEventListener('click', () => {
      const prompt = button.dataset.prompt;
      if (prompt) submitMessage(prompt);
    });
  });

  document.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const fillText = chip.dataset.fill;
      if (fillText) {
        chatInput.value = fillText;
        chatInput.focus();
        resizeInput();
      }
    });
  });

  // 11. New Conversation & Reset
  function resetChat() {
    conversation.innerHTML = '';
    conversation.appendChild(welcome);
    messageHistory = [];
    chatInput.value = '';
    resizeInput();
    chatInput.focus();
    updateGreeting();
  }
  if (newChatBtn) newChatBtn.addEventListener('click', resetChat);

  // 12. Telemetry & Memory API
  async function fetchTelemetry() {
    try {
      const res = await fetch('/api/status');
      if (res.ok) {
        const data = await res.json();
        if (data.model) {
          const shortName = data.model.split('/').pop().replace(':free', '');
          if (activeModelName) activeModelName.textContent = shortName;
          if (diagModel) diagModel.textContent = data.model;
        }
        if (typeof data.memory_count === 'number') {
          if (memoryCountBadge) memoryCountBadge.textContent = data.memory_count;
          if (memStatCount) memStatCount.textContent = data.memory_count;
        }
      }
    } catch (e) {
      console.warn('Telemetry fetch failed:', e);
    }
  }
  fetchTelemetry();

  // 13. Memory Drawer Management
  async function openMemoryDrawer() {
    if (!memoryDrawer) return;
    memoryDrawer.classList.add('open');
    memoryDrawer.setAttribute('aria-hidden', 'false');
    if (sidebarBackdrop) sidebarBackdrop.classList.add('active');

    // Fetch memory history
    try {
      const res = await fetch('/api/memory');
      if (res.ok) {
        const data = await res.json();
        const history = data.history || [];
        if (memStatCount) memStatCount.textContent = history.length;
        if (memoryCountBadge) memoryCountBadge.textContent = history.length;

        memoryCardsContainer.innerHTML = '';
        if (history.length === 0) {
          memoryCardsContainer.innerHTML = '<div class="empty-state">No remembered exchanges yet.</div>';
        } else {
          history.forEach(item => {
            const card = document.createElement('div');
            card.className = 'mem-card';
            card.innerHTML = `
              <span class="mem-card-role ${escapeHtml(item.role)}">${escapeHtml(item.role)}</span>
              <div class="mem-card-content">${escapeHtml(item.content)}</div>
            `;
            memoryCardsContainer.appendChild(card);
          });
        }
      }
    } catch (e) {
      console.error('Failed to load memory:', e);
      memoryCardsContainer.innerHTML = '<div class="empty-state">Failed to load memory history.</div>';
    }
  }

  function closeMemoryDrawer() {
    if (!memoryDrawer) return;
    memoryDrawer.classList.remove('open');
    memoryDrawer.setAttribute('aria-hidden', 'true');
    if (sidebarBackdrop && !sidebar.classList.contains('mobile-open')) {
      sidebarBackdrop.classList.remove('active');
    }
  }

  if (navMemory) navMemory.addEventListener('click', openMemoryDrawer);
  if (memoryCloseBtn) memoryCloseBtn.addEventListener('click', closeMemoryDrawer);

  if (clearMemoryBtn) {
    clearMemoryBtn.addEventListener('click', async () => {
      if (!confirm('Are you sure you want to clear JARVIS memory?')) return;
      try {
        const res = await fetch('/api/memory/clear', { method: 'POST' });
        const data = await res.json();
        if (data.success) {
          showToast('Memory successfully cleared');
          openMemoryDrawer();
          fetchTelemetry();
        }
      } catch (e) {
        showToast('Error clearing memory');
      }
    });
  }

  // 14. Workspace Modal Management
  function openWorkspaceModal() {
    if (workspaceModal) workspaceModal.classList.remove('hidden');
  }

  function closeWorkspaceModal() {
    if (workspaceModal) workspaceModal.classList.add('hidden');
  }

  if (navWorkspace) navWorkspace.addEventListener('click', openWorkspaceModal);
  if (workspaceCloseBtn) workspaceCloseBtn.addEventListener('click', closeWorkspaceModal);
  if (workspaceModal) {
    workspaceModal.addEventListener('click', (e) => {
      if (e.target === workspaceModal) closeWorkspaceModal();
    });
  }

  // 15. Nav Chat Button
  if (navChat) {
    navChat.addEventListener('click', () => {
      closeMemoryDrawer();
      closeWorkspaceModal();
      if (sidebar.classList.contains('mobile-open')) {
        closeMobileSidebar();
      }
    });
  }

  // 16. Mobile Sidebar
  function openMobileSidebar() {
    sidebar.classList.add('mobile-open');
    if (sidebarBackdrop) sidebarBackdrop.classList.add('active');
  }

  function closeMobileSidebar() {
    sidebar.classList.remove('mobile-open');
    if (sidebarBackdrop && (!memoryDrawer || !memoryDrawer.classList.contains('open'))) {
      sidebarBackdrop.classList.remove('active');
    }
  }

  if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
      if (sidebar.classList.contains('mobile-open')) closeMobileSidebar();
      else openMobileSidebar();
    });
  }

  if (sidebarBackdrop) {
    sidebarBackdrop.addEventListener('click', () => {
      closeMobileSidebar();
      closeMemoryDrawer();
    });
  }

  // 17. Share Button
  if (shareBtn) {
    shareBtn.addEventListener('click', () => {
      if (messageHistory.length === 0) {
        navigator.clipboard.writeText(window.location.href).then(() => {
          showToast('Page URL copied to clipboard!');
        });
      } else {
        const transcript = messageHistory.map(m => `${m.role.toUpperCase()}:\n${m.content}`).join('\n\n---\n\n');
        navigator.clipboard.writeText(transcript).then(() => {
          showToast('Conversation transcript copied to clipboard!');
        });
      }
    });
  }

  // 18. Composer Shortcut '+' Button
  if (composerCmdBtn) {
    composerCmdBtn.addEventListener('click', openWorkspaceModal);
  }

  // 19. Keyboard Shortcuts
  document.addEventListener('keydown', (e) => {
    // Cmd+K or Ctrl+K focuses input
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      chatInput.focus();
    }
    // Escape closes modals and drawers
    if (e.key === 'Escape') {
      closeMemoryDrawer();
      closeWorkspaceModal();
      closeMobileSidebar();
      stopListening();
    }
  });

  // Initial input resize
  resizeInput();
});
