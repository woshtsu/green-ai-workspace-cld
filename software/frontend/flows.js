/* Vista «Red de flujos»: dibuja el grafo radial y anima la propuesta ilustrativa de reubicación de carga. */
(function () {
  const $ = id => document.getElementById(id);
  const NS = 'http://www.w3.org/2000/svg';
  const svg = $('flows-svg');
  if (!svg) return;
  const reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const state = { nodes: [], racks: {}, flows: null, selected: null, playing: !reduceMotion, timer: null, busy: false, positions: null };
  const fmt = n => new Intl.NumberFormat('es-PE', { maximumFractionDigits: 1 }).format(n);
  const make = (tag, attrs = {}) => { const e = document.createElementNS(NS, tag); for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v); return e; };

  function drawWeb(layout) {
    const g = make('g', { 'aria-hidden': 'true' });
    [0.3, 0.52, 0.74, 0.97].forEach(f => g.append(make('circle', { cx: 450, cy: 450, r: 360 * f, class: 'web-ring' })));
    layout.racks.forEach((rack, i) => {
      const a = (-90 + i * layout.sector) * Math.PI / 180;
      g.append(make('line', { x1: 450, y1: 450, x2: 450 + 392 * Math.cos(a), y2: 450 + 392 * Math.sin(a), class: 'web-spoke' }));
      const mid = (-90 + i * layout.sector + layout.sector / 2) * Math.PI / 180;
      const label = make('text', { x: 450 + 418 * Math.cos(mid), y: 450 + 418 * Math.sin(mid) + 4, class: 'rack-label' });
      label.textContent = rack; g.append(label);
    });
    return g;
  }

  function currentNodes() {
    const rack = $('fc-rack').value;
    return rack ? state.nodes.filter(n => n.rack === rack) : state.nodes;
  }

  function render() {
    const nodes = currentNodes();
    const layout = GreenFlows.layoutRadial(state.nodes);
    state.positions = layout.positions;
    const result = GreenFlows.computeTransfers(nodes, { k: Number($('fc-k').value), maxFlows: Number($('fc-max').value) });
    state.flows = result;
    svg.replaceChildren(
      make('defs'), drawWeb(layout));
    const defs = svg.querySelector('defs');
    const flowsG = make('g');
    const nodesG = make('g');
    const selected = state.selected;
    const colorOf = id => getCpuColor(state.nodes.find(n => n.id === id)?.cpu ?? null);
    result.flows.forEach((flow, idx) => {
      const a = layout.positions.get(flow.from), b = layout.positions.get(flow.to);
      if (!a || !b) return;
      const gradId = `fg-${idx}`;
      const grad = make('linearGradient', { id: gradId, gradientUnits: 'userSpaceOnUse', x1: a.x, y1: a.y, x2: b.x, y2: b.y });
      grad.append(make('stop', { offset: '0%', 'stop-color': colorOf(flow.from) }), make('stop', { offset: '100%', 'stop-color': '#22d3ee' }));
      defs.append(grad);
      const d = GreenFlows.curvePath(a, b);
      const touches = selected && (flow.from === selected || flow.to === selected);
      const path = make('path', { d, class: `flow-line${selected ? (touches ? ' is-hot' : ' is-dim') : ''}`, style: `stroke:url(#${gradId})`, 'stroke-width': (1 + flow.amountPercent / 3).toFixed(2) });
      const tip = make('title'); tip.textContent = `${flow.from} → ${flow.to}: ${fmt(flow.amountPercent)} pp de CPU (propuesta)`; path.append(tip);
      flowsG.append(path);
      if (!reduceMotion && (!selected || touches)) {
        const dot = make('circle', { r: (2 + flow.amountPercent / 6).toFixed(1), class: 'flow-dot' });
        const anim = make('animateMotion', { dur: `${(3.2 + (idx % 5) * 0.5).toFixed(1)}s`, repeatCount: 'indefinite', path: d, begin: `${(idx * 0.37).toFixed(2)}s` });
        dot.append(anim); flowsG.append(dot);
      }
    });
    for (const n of state.nodes) {
      const p = layout.positions.get(n.id);
      const inScope = nodes.includes(n);
      const r = 9 + ((n.maxWatts || 450) / 800) * 7;
      const dot = make('circle', { cx: p.x, cy: p.y, r: r.toFixed(1), fill: getCpuColor(n.cpu), 'fill-opacity': inScope ? 0.92 : 0.18, stroke: 'rgba(255,255,255,.25)',
        class: `node-dot${result.sources.includes(n.id) && inScope ? ' is-source' : ''}${result.sinks.includes(n.id) && inScope ? ' is-sink' : ''}${selected === n.id ? ' is-selected' : ''}`,
        tabindex: '0', role: 'button', 'aria-label': `${n.id}, ${n.rack}, CPU ${n.cpu === null ? 'sin dato' : fmt(n.cpu) + ' %'}` });
      const title = make('title'); title.textContent = `${n.id} · ${n.rack} · CPU ${n.cpu === null ? 'sin dato' : fmt(n.cpu) + ' %'}`; dot.append(title);
      dot.addEventListener('click', () => select(n.id));
      dot.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); select(n.id); } });
      nodesG.append(dot);
      if (selected === n.id) { const t = make('text', { x: p.x, y: p.y - r - 6, class: 'node-label' }); t.textContent = n.id; nodesG.append(t); }
    }
    svg.append(flowsG, nodesG);
    if (!state.playing) svg.pauseAnimations && svg.pauseAnimations();

    const moved = result.flows.reduce((a, f) => a + f.amountPercent, 0);
    $('fs-flows').textContent = String(result.flows.length);
    $('fs-note').textContent = result.balanced ? 'Carga equilibrada' : (result.flows.length ? 'Propuestas de rebalanceo' : 'Sin propuestas con este criterio');
    $('fs-moved').textContent = `${fmt(moved)} pp`;
    $('fs-sources').textContent = String(result.sources.length);
    $('fs-sinks').textContent = String(result.sinks.length);
    $('fs-criterion').textContent = result.criterion;
    renderDetail();
  }

  function renderDetail() {
    const n = state.nodes.find(x => x.id === state.selected);
    $('fd-empty').hidden = !!n; $('fd-content').hidden = !n;
    if (!n) return;
    const flows = (state.flows?.flows || []);
    const out = flows.filter(f => f.from === n.id), inn = flows.filter(f => f.to === n.id);
    $('fd-id').textContent = n.id; $('fd-rack').textContent = n.rack;
    $('fd-cpu').textContent = n.cpu === null ? 'Sin dato' : `${fmt(n.cpu)} %`;
    $('fd-role').textContent = out.length ? 'Origen: cedería carga' : inn.length ? 'Destino: recibiría carga' : 'Sin cambios propuestos';
    const list = $('fd-flows'); list.replaceChildren();
    for (const f of out) { const li = document.createElement('li'); li.innerHTML = '<span></span><span class="out"></span>'; li.children[0].textContent = `→ ${f.to}`; li.children[1].textContent = `−${fmt(f.amountPercent)} pp`; list.append(li); }
    for (const f of inn) { const li = document.createElement('li'); li.innerHTML = '<span></span><span class="in"></span>'; li.children[0].textContent = `← ${f.from}`; li.children[1].textContent = `+${fmt(f.amountPercent)} pp`; list.append(li); }
    if (!out.length && !inn.length) { const li = document.createElement('li'); li.textContent = 'Este servidor no participa en la propuesta actual.'; list.append(li); }
  }

  function select(id) { state.selected = state.selected === id ? null : id; render(); }

  async function load() {
    if (state.busy) return;
    state.busy = true;
    clearTimeout(state.timer);
    const box = $('flows-problem');
    try {
      const [inventory, payload] = await Promise.all([loadRacksInventory(), fetchCurrentMetrics()]);
      const metrics = parseMetricsResponse(payload);
      state.nodes = inventory.nodes.map(n => ({ id: n.id, rack: n.rack, maxWatts: n.maxWatts, cpu: metrics.get(n.id)?.cpu ?? null }));
      const racks = [...new Set(state.nodes.map(n => n.rack))].sort();
      const sel = $('fc-rack');
      if (sel.options.length <= 1) racks.forEach(r => sel.append(new Option(r, r)));
      GreenUI.clearProblem(box);
      $('fd-updated').textContent = `Actualizado ${new Date().toLocaleTimeString()} · cada 15 s`;
      render();
    } catch (error) {
      const friendly = GreenErrors.fromException(error, 'metricas');
      GreenUI.renderProblem(box, friendly, { onRetry: load });
      $('fs-criterion').textContent = 'Sin datos por el momento.';
    } finally {
      state.busy = false;
      state.timer = setTimeout(load, 15000);
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    $('fc-k').addEventListener('input', () => { $('fc-k-out').textContent = Number($('fc-k').value).toFixed(1); if (state.nodes.length) render(); });
    $('fc-max').addEventListener('input', () => { $('fc-max-out').textContent = $('fc-max').value; if (state.nodes.length) render(); });
    $('fc-rack').addEventListener('change', () => state.nodes.length && render());
    $('fc-refresh').addEventListener('click', load);
    const play = $('fc-play');
    if (reduceMotion) { play.textContent = 'Animación desactivada'; play.disabled = true; }
    play.addEventListener('click', () => {
      state.playing = !state.playing;
      play.textContent = state.playing ? 'Pausar' : 'Reproducir';
      play.setAttribute('aria-pressed', String(state.playing));
      if (state.playing) svg.unpauseAnimations(); else svg.pauseAnimations();
    });
    window.addEventListener('pagehide', () => clearTimeout(state.timer));
    // app.js valida la sesión; esperamos a que exista antes de consultar
    const wait = setInterval(() => { if (typeof authenticatedFetch === 'function' && window.GREEN_AI_CONFIG) { clearInterval(wait); load(); } }, 150);
  });
})();
