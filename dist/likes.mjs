const COUNTER_API = 'https://countapi.mileshilliard.com/api/v1';

class CounterError extends Error {
  constructor(message, rejected = false) {
    super(message);
    this.rejected = rejected;
  }
}

export class ArticleLikes {
  constructor(key, { fetcher = (...args) => globalThis.fetch(...args), storage = null, locks = null, timeout = 8000 } = {}) {
    if (!/^[A-Za-z0-9_-]{1,100}$/.test(key)) throw new Error('Invalid counter key');
    this.key = key;
    this.storageKey = `cln:like:${key}`;
    this.fetcher = fetcher;
    this.storage = storage;
    this.locks = locks;
    this.timeout = timeout;
    this.memoryState = null;
    this.inFlight = null;
  }

  state() {
    try {
      const saved = this.storage?.getItem(this.storageKey);
      if (saved === 'liked' || saved === 'pending') return saved;
    } catch { /* Session memory still works when browser storage is unavailable. */ }
    return this.memoryState;
  }

  remember(state) {
    this.memoryState = state;
    try {
      if (state) this.storage?.setItem(this.storageKey, state);
      else this.storage?.removeItem(this.storageKey);
    } catch { /* Never require storage permission just to read the page. */ }
  }

  async request(action) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeout);
    try {
      const response = await this.fetcher(`${COUNTER_API}/${action}/${encodeURIComponent(this.key)}`, {
        method: 'GET', cache: 'no-store', credentials: 'omit', referrerPolicy: 'no-referrer', signal: controller.signal,
      });
      let data;
      try { data = await response.json(); }
      catch { throw new CounterError('Invalid counter response'); }
      if (action === 'get' && response.status === 404 && data.error === 'Key not found') return 0;
      if (!response.ok) throw new CounterError('Counter request rejected', response.status >= 400 && response.status < 500);
      const value = String(data.value ?? '');
      const count = Number(value);
      if (!/^\d+$/.test(value) || !Number.isSafeInteger(count)) throw new CounterError('Invalid counter value');
      return count;
    } finally {
      clearTimeout(timer);
    }
  }

  read() { return this.request('get'); }

  like() {
    if (this.inFlight) return this.inFlight;
    const submit = async () => {
      const saved = this.state();
      if (saved) return { count: await this.read(), state: saved };
      // Record an attempt before sending it; a lost reply must not cause an automatic second vote.
      this.remember('pending');
      try {
        const count = await this.request('hit');
        this.remember('liked');
        return { count, state: 'liked' };
      } catch (error) {
        if (error.rejected) this.remember(null);
        throw error;
      }
    };
    const operation = this.locks?.request ? this.locks.request(this.storageKey, submit) : submit();
    this.inFlight = operation.finally(() => { this.inFlight = null; });
    return this.inFlight;
  }
}

function mountLikes() {
  let storage = null;
  try { storage = window.localStorage; } catch { /* Storage is optional. */ }
  const groups = new Map();
  for (const widget of document.querySelectorAll('[data-like-key]')) {
    const key = widget.dataset.likeKey;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(widget);
  }
  for (const [key, widgets] of groups) {
    const counter = new ArticleLikes(key, { storage, locks: navigator.locks });
    let count = null;
    let busy = false;
    let message = '';
    let revision = 0;
    const pendingMessage = 'Your like may have been received. Reload to refresh the total.';
    function render() {
      const state = counter.state();
      for (const widget of widgets) {
        const button = widget.querySelector('[data-like-button]');
        button.disabled = busy || Boolean(state) || (count === null && !message);
        button.setAttribute('aria-pressed', String(state === 'liked'));
        widget.querySelector('[data-like-label]').textContent = busy ? 'Sending…' : state === 'liked' ? 'Liked' : state === 'pending' ? 'Pending' : count === null && message ? 'Retry' : 'Like';
        widget.querySelector('[data-like-count]').textContent = count === null ? '—' : count.toLocaleString('en-US');
        widget.querySelector('[data-like-unit]').textContent = count === 1 ? 'like' : 'likes';
        widget.querySelector('[data-like-status]').textContent = message;
      }
    }
    async function refresh() {
      const requestRevision = ++revision;
      try {
        const latest = await counter.read();
        if (requestRevision !== revision) return;
        count = latest;
        message = counter.state() === 'pending' ? pendingMessage : '';
      } catch {
        if (requestRevision !== revision) return;
        message = count === null ? 'Likes are temporarily unavailable. Please try again.' : 'Could not refresh the total.';
      }
      render();
    }
    async function submit() {
      if (busy || counter.state()) return;
      if (count === null) { await refresh(); return; }
      busy = true;
      message = '';
      ++revision;
      render();
      try {
        const result = await counter.like();
        count = result.count;
        message = result.state === 'pending' ? pendingMessage : '';
        if (result.state === 'liked') {
          for (const widget of widgets) widget.querySelector('[data-like-button]').classList.add('like-received');
        }
      } catch {
        message = counter.state() === 'pending' ? pendingMessage : 'Could not save your like. Please try again.';
      } finally {
        busy = false;
        render();
      }
    }
    for (const widget of widgets) widget.querySelector('[data-like-button]').addEventListener('click', submit);
    window.addEventListener('storage', event => { if (event.key === counter.storageKey) { render(); void refresh(); } });
    window.addEventListener('pageshow', event => { if (event.persisted) void refresh(); });
    document.addEventListener('visibilitychange', () => { if (!document.hidden && !busy) void refresh(); });
    render();
    void refresh();
  }
}

if (typeof document !== 'undefined') mountLikes();
