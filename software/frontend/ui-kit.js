/* Piezas de interfaz compartidas: botones «?», pestañas y paneles de aviso (espera/errores). Solo presentación. */
(function () {
  const doc = typeof document !== 'undefined' ? document : null;
  if (!doc) return;
  const HELP = () => window.GreenHelp || {};

  function el(tag, attrs = {}, ...kids) {
    const node = doc.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (v === false || v == null) continue;
      if (k === 'class') node.className = v; else node.setAttribute(k, v === true ? '' : v);
    }
    for (const kid of kids.flat()) node.append(kid instanceof Node ? kid : doc.createTextNode(String(kid)));
    return node;
  }

  /* ---------- Botones «?» ---------- */
  let pop = null, popOwner = null;
  function closePop() {
    if (!pop) return;
    pop.remove(); pop = null;
    if (popOwner) { popOwner.setAttribute('aria-expanded', 'false'); popOwner.focus({ preventScroll: true }); popOwner = null; }
  }
  function helpBody(entry) {
    const rows = [['Qué es', entry.what], ['Para qué sirve', entry.use], ['Cómo se mide', entry.how],
      ['Qué debes colocar', entry.input], ['Límites', entry.limits]].filter(r => r[1]);
    return rows.map(([label, text]) => el('div', { class: 'help-row' }, el('dt', {}, label), el('dd', {}, text)));
  }
  function openPop(button, key) {
    const entry = HELP()[key];
    if (!entry) return;
    const wasSame = popOwner === button;
    closePop();
    if (wasSame) return;
    const id = `help-${key}`;
    pop = el('div', { class: 'help-pop', role: 'dialog', 'aria-labelledby': `${id}-t`, tabindex: '-1', id },
      el('div', { class: 'help-pop-head' }, el('strong', { id: `${id}-t` }, entry.title),
        el('button', { class: 'help-close', type: 'button', 'aria-label': 'Cerrar ayuda' }, '×')),
      el('dl', { class: 'help-list' }, helpBody(entry)));
    pop.querySelector('.help-close').addEventListener('click', closePop);
    doc.body.append(pop);
    const r = button.getBoundingClientRect();
    const width = Math.min(360, window.innerWidth - 24);
    pop.style.width = `${width}px`;
    pop.style.left = `${Math.max(12, Math.min(r.left + window.scrollX - 12, window.scrollX + window.innerWidth - width - 12))}px`;
    pop.style.top = `${r.bottom + window.scrollY + 10}px`;
    button.setAttribute('aria-expanded', 'true');
    button.setAttribute('aria-controls', id);
    popOwner = button;
    pop.focus({ preventScroll: true });
  }
  function initHelp(root = doc) {
    root.querySelectorAll('[data-help-inline]').forEach(btn => {
      if (btn.dataset.wired) return;
      btn.dataset.wired = '1';
      btn.setAttribute('aria-expanded', 'false');
      btn.setAttribute('aria-haspopup', 'dialog');
      btn.addEventListener('click', event => { event.preventDefault(); event.stopPropagation(); openPop(btn, btn.dataset.helpInline); });
    });
    root.querySelectorAll('[data-help]').forEach(host => {
      if (host.querySelector(':scope > .help-btn')) return;
      const key = host.dataset.help;
      const entry = HELP()[key];
      if (!entry) return;
      const btn = el('button', { class: 'help-btn', type: 'button', 'aria-label': `Ayuda: ${entry.title}`,
        'aria-expanded': 'false', 'aria-haspopup': 'dialog' }, '?');
      btn.addEventListener('click', event => { event.stopPropagation(); openPop(btn, key); });
      host.append(btn);
    });
  }
  doc.addEventListener('keydown', event => { if (event.key === 'Escape' && pop) closePop(); });
  doc.addEventListener('click', event => { if (pop && !pop.contains(event.target) && !event.target.closest('.help-btn')) closePop(); });

  /* ---------- Pestañas ---------- */
  function initTabs(list) {
    const tabs = [...list.querySelectorAll('[role="tab"]')];
    const panels = tabs.map(t => doc.getElementById(t.getAttribute('aria-controls')));
    function select(index, { focus = false, push = true } = {}) {
      tabs.forEach((tab, i) => {
        const active = i === index;
        tab.setAttribute('aria-selected', String(active));
        tab.tabIndex = active ? 0 : -1;
        if (panels[i]) panels[i].hidden = !active;
      });
      if (focus) tabs[index].focus();
      if (push && tabs[index].dataset.tab) {
        try { history.replaceState(null, '', `#${tabs[index].dataset.tab}`); } catch { /* sin historial */ }
      }
      window.dispatchEvent(new CustomEvent('greenai:tab', { detail: { id: tabs[index].dataset.tab } }));
    }
    tabs.forEach((tab, i) => {
      tab.addEventListener('click', () => select(i));
      tab.addEventListener('keydown', event => {
        const keys = { ArrowRight: 1, ArrowLeft: -1 };
        if (event.key in keys) { event.preventDefault(); select((i + keys[event.key] + tabs.length) % tabs.length, { focus: true }); }
        if (event.key === 'Home') { event.preventDefault(); select(0, { focus: true }); }
        if (event.key === 'End') { event.preventDefault(); select(tabs.length - 1, { focus: true }); }
      });
    });
    const wanted = tabs.findIndex(t => `#${t.dataset.tab}` === location.hash);
    select(wanted >= 0 ? wanted : 0, { push: false });
    window.addEventListener('hashchange', () => {
      const i = tabs.findIndex(t => `#${t.dataset.tab}` === location.hash);
      if (i >= 0) select(i, { push: false });
    });
  }

  /* ---------- Avisos: espera / errores ---------- */
  const ICONS = { espera: '⏳', datos: '✎', permisos: '🔒', servicio: '☁', sesion: '🔑' };
  let countdownTimers = new WeakMap();
  function renderProblem(container, friendly, { onRetry = null, retrySeconds = 60 } = {}) {
    if (!container) return;
    clearProblem(container);
    const kind = friendly.tipo || 'servicio';
    const box = el('div', { class: `notice notice--${kind}`, role: kind === 'espera' ? 'status' : 'alert' },
      el('div', { class: 'notice-icon', 'aria-hidden': 'true' }, ICONS[kind] || '!'),
      el('div', { class: 'notice-body' },
        el('strong', { class: 'notice-title' }, friendly.titulo),
        el('p', { class: 'notice-text' }, friendly.mensaje)));
    const body = box.querySelector('.notice-body');
    if (kind === 'espera') body.append(el('div', { class: 'notice-bar', 'aria-hidden': 'true' }, el('span')));
    if (friendly.accion && onRetry) {
      const retry = el('button', { class: 'btn btn-secondary notice-retry', type: 'button' }, friendly.accion);
      retry.addEventListener('click', () => { clearProblem(container); onRetry(); });
      const hint = el('span', { class: 'notice-hint' });
      body.append(el('div', { class: 'notice-actions' }, retry, hint));
      if (kind === 'espera' || kind === 'servicio') {
        let left = retrySeconds;
        const tick = () => { hint.textContent = left > 0 ? `Intento sugerido en ${left} s` : 'Ya puedes reintentar'; left -= 1; };
        tick();
        const timer = setInterval(() => { if (!box.isConnected) { clearInterval(timer); return; } tick(); if (left < -1) clearInterval(timer); }, 1000);
        countdownTimers.set(container, timer);
      }
    }
    if (friendly.detalleTecnico) {
      body.append(el('details', { class: 'notice-tech' }, el('summary', {}, 'Detalles técnicos'), el('code', {}, friendly.detalleTecnico)));
    }
    container.append(box);
    container.hidden = false;
  }
  function clearProblem(container) {
    if (!container) return;
    const timer = countdownTimers.get(container);
    if (timer) clearInterval(timer);
    container.replaceChildren();
    container.hidden = true;
  }

  doc.addEventListener('DOMContentLoaded', () => {
    initHelp();
    doc.querySelectorAll('[role="tablist"][data-tabs]').forEach(initTabs);
  });
  window.GreenUI = { el, initHelp, initTabs, renderProblem, clearProblem };
})();
