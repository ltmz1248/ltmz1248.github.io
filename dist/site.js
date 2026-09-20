(() => {
  const signalButton = document.querySelector('[data-signal]');
  const signalMessage = document.querySelector('[data-signal-message]');
  if (!signalButton || !signalMessage) return;
  let timer;
  function receiveSignal() {
    clearTimeout(timer);
    const enabled = !document.body.classList.contains('signal-active');
    document.body.classList.toggle('signal-active', enabled);
    signalButton.setAttribute('aria-pressed', String(enabled));
    signalMessage.textContent = enabled ? 'Signal 117 received. Welcome back, Spartan.' : '';
    if (enabled) timer = setTimeout(() => {
      document.body.classList.remove('signal-active');
      signalButton.setAttribute('aria-pressed', 'false');
      signalMessage.textContent = '';
    }, 6500);
  }
  signalButton.addEventListener('click', receiveSignal);
  let sequence = '';
  document.addEventListener('keydown', event => {
    if (event.ctrlKey || event.metaKey || event.altKey || event.target.isContentEditable || /INPUT|TEXTAREA|SELECT/.test(event.target.tagName)) return;
    if (event.key === 'Escape') {
      if (document.body.classList.contains('signal-active')) receiveSignal();
      return;
    }
    sequence = (sequence + event.key).slice(-3);
    if (sequence === '117') { receiveSignal(); sequence = ''; }
  });
})();
