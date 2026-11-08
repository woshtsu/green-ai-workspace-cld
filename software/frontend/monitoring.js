let historyChart;
let catalog = [];
let refreshTimer;
let refreshing = false;
let lastHistory = null;
let tableRows = [];
const tableState = { query: '', sortKey: 'node', dir: 'asc', page: 1, size: 10 };
const compareIds = new Set();
const COMPARE_LIMIT = 5;
const LINE_COLORS = ['#06b6d4', '#a855f7', '#10b981', '#f59e0b', '#fb7185'];
const names = {'node.cpu.utilization':'CPU', 'node.memory.used':'Memoria utilizada', 'node.network.receive':'Red recibida', 'node.network.transmit':'Red transmitida', 'node.filesystem.used':'Filesystem utilizado'};
const $ = id => document.getElementById(id);
function put(id, text) { if ($(id)) $(id).textContent = text; }
function options(id, entries, selected) {
  $(id).replaceChildren(...entries.map(([value, label]) => new Option(label, value)));
  if (entries.some(([value]) => value === selected)) $(id).value = selected;
}
async function metricRequest(operation, params = {}) {
  const response = await authenticatedFetch(`${GATEWAY_BASE_URL}/api/monitoring/v1/metrics/${operation}?${new URLSearchParams(params)}`);
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    const id = response.headers.get('X-Request-Id');
    if (typeof GreenErrors !== 'undefined') throw GreenErrors.toError({ status: response.status, body, reference: id, context: 'metricas' });
    throw new Error(`${body.detail || 'No se pudieron consultar las métricas.'} (HTTP ${response.status})${id ? ' · Referencia: ' + id : ''}`);
  }
  return response.json();
}
const scaleOf = payload => (payload.unit === 'ratio' ? 100 : 1);
const unitText = payload => (payload.unit === 'ratio' ? '%' : payload.unit);
function fmtValue(value, payload) {
  if (value === null || value === undefined) return '—';
  const n = new Intl.NumberFormat('es-PE', { maximumFractionDigits: 1 }).format(value);
  return payload.unit === 'ratio' ? `${n} %` : `${n} ${payload.unit}`;
}

/* ---------- Resumen y tabla ---------- */
function renderSummary(payload) {
  const scale = scaleOf(payload);
  const stats = GreenAggregate.summarize(payload, scale, payload.unit === 'ratio' ? 80 : null);
  put('stat-mean', fmtValue(stats.mean, payload));
  put('stat-max', stats.max ? fmtValue(stats.max.value, payload) : '—');
  put('stat-max-note', stats.max ? stats.max.id : '');
  put('stat-min', stats.min ? fmtValue(stats.min.value, payload) : '—');
  put('stat-min-note', stats.min ? stats.min.id : '');
  put('stat-above', payload.unit === 'ratio' ? String(stats.above) : '—');
  put('stat-above-note', payload.unit === 'ratio' ? `de ${stats.valid} servidores con dato` : 'Solo aplica a porcentajes');
  $('stat-above-card')?.classList.toggle('stat--alert', payload.unit === 'ratio' && stats.above > 0);
}
function renderCurrent(payload) {
  put('summary-nodes', new Set(payload.series.map(s => JSON.stringify([s.resource.cluster, s.resource.id]))).size);
  const usable = payload.series.filter(s => s.samples.at(-1)?.quality === 'valid' && Number.isFinite(s.samples.at(-1)?.value)).length;
  put('summary-valid', `${usable} / ${payload.series.length}`);
  put('summary-origin', [...new Set(payload.series.map(s => GreenMetrics.origin(s.origin)))].join(' · ') || 'Sin datos');
  put('summary-quality', GreenMetrics.status(payload.dataStatus));
  renderSummary(payload);
  tableRows = payload.series.map(series => {
    const sample = series.samples.at(-1);
    const usableSample = sample && sample.quality === 'valid' && Number.isFinite(sample.value);
    return {
      cluster: series.resource.cluster, node: series.resource.id,
      iface: Object.entries(series.labels).map(([k, v]) => `${k}=${v}`).join(', ') || '—',
      value: usableSample ? sample.value : null, valueText: GreenMetrics.value(sample, payload.unit),
      origin: GreenMetrics.origin(series.origin), quality: sample?.quality || 'missing',
      time: sample ? new Date(sample.timestamp).toLocaleString() : 'Sin dato'
    };
  });
  put('current-status', tableRows.length ? GreenMetrics.status(payload.dataStatus) : 'Sin datos para estos filtros.');
  put('warnings', payload.warnings.join(' · '));
  renderTable();
}
function renderTable() {
  const view = GreenAggregate.pageRows(tableRows, tableState);
  tableState.page = view.page;
  $('metric-rows').replaceChildren(...view.rows.map(r => {
    const row = document.createElement('tr');
    [r.cluster, r.node, r.iface, r.valueText, r.origin, r.quality, r.time].forEach(value => {
      const cell = document.createElement('td'); cell.textContent = value; row.append(cell);
    });
    return row;
  }));
  put('table-count', tableRows.length ? `${tableRows.length} servidores` : '');
  put('pager-info', view.total ? `Mostrando ${view.from}–${view.to} de ${view.total}` : 'Sin resultados');
  put('pager-page', view.total ? `Página ${view.page} de ${view.pages}` : '');
  if ($('pager-prev')) $('pager-prev').disabled = view.page <= 1;
  if ($('pager-next')) $('pager-next').disabled = view.page >= view.pages;
  document.querySelectorAll('.data-table th[data-sort]').forEach(th => {
    th.setAttribute('aria-sort', th.dataset.sort === tableState.sortKey ? (tableState.dir === 'asc' ? 'ascending' : 'descending') : 'none');
  });
}
function initTable() {
  $('table-search')?.addEventListener('input', event => { tableState.query = event.target.value; tableState.page = 1; renderTable(); });
  $('pager-prev')?.addEventListener('click', () => { tableState.page -= 1; renderTable(); });
  $('pager-next')?.addEventListener('click', () => { tableState.page += 1; renderTable(); });
  document.querySelectorAll('.data-table th[data-sort]').forEach(th => {
    th.tabIndex = 0;
    const sort = () => {
      if (tableState.sortKey === th.dataset.sort) tableState.dir = tableState.dir === 'asc' ? 'desc' : 'asc';
      else { tableState.sortKey = th.dataset.sort; tableState.dir = th.dataset.sort === 'value' ? 'desc' : 'asc'; }
      tableState.page = 1; renderTable();
    };
    th.addEventListener('click', sort);
    th.addEventListener('keydown', event => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); sort(); } });
  });
}

/* ---------- Comparación de servidores ---------- */
function renderChips() {
  const holder = $('compare-chips');
  if (!holder) return;
  holder.replaceChildren(...[...compareIds].map(id => {
    const chip = document.createElement('span'); chip.className = 'chip';
    chip.append(document.createTextNode(id));
    const remove = document.createElement('button');
    remove.type = 'button'; remove.textContent = '×'; remove.setAttribute('aria-label', `Quitar ${id}`);
    remove.addEventListener('click', () => { compareIds.delete(id); renderChips(); if (lastHistory) drawHistory(lastHistory); });
    chip.append(remove); return chip;
  }));
}
function setCompare(ids) {
  compareIds.clear();
  ids.slice(0, COMPARE_LIMIT).forEach(id => compareIds.add(id));
  renderChips();
  if (lastHistory) drawHistory(lastHistory);
}
function initCompare() {
  const input = $('compare-input');
  if (!input) return;
  input.addEventListener('change', () => {
    const id = input.value.trim().toUpperCase();
    input.value = '';
    if (!id || !lastHistory) return;
    if (!lastHistory.series.some(s => s.resource.id.toUpperCase() === id)) { put('legend-note', `No hay datos para «${id}» con estos filtros.`); return; }
    const real = lastHistory.series.find(s => s.resource.id.toUpperCase() === id).resource.id;
    if (compareIds.size >= COMPARE_LIMIT && !compareIds.has(real)) { put('legend-note', `Puedes comparar hasta ${COMPARE_LIMIT} servidores a la vez.`); return; }
    compareIds.add(real); renderChips(); drawHistory(lastHistory);
  });
  $('compare-top')?.addEventListener('click', () => lastHistory && setCompare(GreenAggregate.rankNodes(lastHistory, 'top', COMPARE_LIMIT, scaleOf(lastHistory)).map(s => s.resource.id)));
  $('compare-bottom')?.addEventListener('click', () => lastHistory && setCompare(GreenAggregate.rankNodes(lastHistory, 'bottom', COMPARE_LIMIT, scaleOf(lastHistory)).map(s => s.resource.id)));
  $('compare-clear')?.addEventListener('click', () => setCompare([]));
}

/* ---------- Gráfico ---------- */
function drawHistory(payload) {
  lastHistory = payload;
  historyChart?.destroy();
  if (typeof Chart === 'undefined') { put('history-status', 'No se pudo cargar el gráfico. Los valores actuales siguen disponibles.'); return; }
  const scale = scaleOf(payload);
  const many = payload.series.length > 1;
  if ($('compare-bar')) $('compare-bar').hidden = !many;
  const datalist = $('compare-options');
  if (datalist) datalist.replaceChildren(...payload.series.map(s => { const o = document.createElement('option'); o.value = s.resource.id; return o; }));
  for (const id of [...compareIds]) if (!payload.series.some(s => s.resource.id === id)) compareIds.delete(id);
  renderChips();

  const stats = GreenAggregate.historyStats(payload, scale);
  const labels = stats.stamps.map(t => new Date(t).toLocaleTimeString());
  const datasets = [];
  if (many) {
    datasets.push(
      { label: 'Mínimo', data: stats.min, borderColor: 'rgba(6,182,212,0)', backgroundColor: 'transparent', pointRadius: 0, hideLegend: true, spanGaps: false },
      { label: 'Rango mín–máx', data: stats.max, borderColor: 'rgba(6,182,212,.35)', backgroundColor: 'rgba(6,182,212,.14)', fill: '-1', borderWidth: 1, pointRadius: 0, spanGaps: false },
      { label: 'Media del conjunto', data: stats.mean, borderColor: '#22d3ee', backgroundColor: '#22d3ee', borderWidth: 3, pointRadius: 0, tension: .25, spanGaps: false });
    let i = 0;
    for (const series of payload.series) {
      if (!compareIds.has(series.resource.id)) continue;
      const color = LINE_COLORS[(i += 1) % LINE_COLORS.length];
      datasets.push({ label: series.resource.id, data: GreenAggregate.alignedValues(series, stats.stamps, scale), borderColor: color, backgroundColor: color, borderWidth: 2, pointRadius: 0, tension: .2, spanGaps: false });
    }
  } else if (payload.series[0]) {
    const series = payload.series[0];
    datasets.push({ label: `${series.resource.id} · ${GreenMetrics.origin(series.origin)}`, data: GreenAggregate.alignedValues(series, stats.stamps, scale), borderColor: '#22d3ee', backgroundColor: '#22d3ee', borderWidth: 3, pointRadius: 0, tension: .25, spanGaps: false });
  }
  const muted = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim() || '#94a3b8';
  historyChart = new Chart($('history-chart'), {
    type: 'line',
    data: { labels, datasets },
    options: { responsive: true, maintainAspectRatio: false, animation: false, interaction: { mode: 'index', intersect: false },
      plugins: { legend: { position: 'bottom', labels: { color: muted, usePointStyle: true, boxWidth: 8, filter: item => !datasets[item.datasetIndex]?.hideLegend } },
        tooltip: { filter: item => !datasets[item.datasetIndex]?.hideLegend, callbacks: { label: ctx => `${ctx.dataset.label}: ${ctx.parsed.y === null ? '—' : ctx.parsed.y.toFixed(1)} ${unitText(payload)}` } } },
      scales: { x: { ticks: { color: muted, maxTicksLimit: 8 }, grid: { color: 'rgba(148,163,184,.08)' } },
        y: { title: { display: true, text: unitText(payload), color: muted }, ticks: { color: muted }, grid: { color: 'rgba(148,163,184,.1)' } } } }
  });
  put('chart-sub', many ? `Media, máximo y mínimo de ${payload.series.length} servidores` : 'Serie del servidor seleccionado');
  put('legend-note', many ? 'Media, máximo y mínimo calculados en pantalla a partir de las series recibidas. Añade servidores para compararlos.' : '');
  put('history-status', `${GreenMetrics.status(payload.dataStatus)} · ${new Date(payload.start).toLocaleString()} — ${new Date(payload.end).toLocaleString()} · ${payload.warnings.join(' · ')}`);
}

async function refreshMetrics() {
  if (refreshing) return;
  refreshing = true;
  clearTimeout(refreshTimer);
  $('refresh').disabled = true;
  for (const id of ['metric','cluster','node','period']) $(id).disabled = true;
  put('request-status', 'Consultando…');
  try {
    const metric = $('metric').value;
    const all = await metricRequest('current', {metric, resourceType:'node'});
    const oldCluster = $('cluster').value;
    options('cluster', [['','Todos los clústeres'], ...[...new Set(all.series.map(s => s.resource.cluster))].sort().map(c => [c,c])], oldCluster);
    const cluster = $('cluster').value;
    const oldNode = $('node').value;
    options('node', [['','Todos los servidores'], ...[...new Set(all.series.filter(s => !cluster || s.resource.cluster === cluster).map(s => s.resource.id))].sort().map(n => [n,n])], oldNode);
    const node = $('node').value;
    if (node && !cluster) {   // un servidor concreto implica su clúster (la predicción lo necesita)
      const owner = all.series.find(s => s.resource.id === node);
      if (owner) $('cluster').value = owner.resource.cluster;
    }
    const clusterNow = $('cluster').value;
    const params = {metric, resourceType:'node', ...(clusterNow ? {cluster: clusterNow} : {}), ...(node ? {resourceId:node} : {})};
    const current = clusterNow || node ? await metricRequest('current', params) : all;
    renderCurrent(current);
    const end = new Date();
    const start = new Date(end.getTime() - Number($('period').value) * 60000);
    let historyError;
    try {
      drawHistory(await metricRequest('history', {
        ...params,
        start:GreenMetrics.rfc3339Seconds(start),
        end:GreenMetrics.rfc3339Seconds(end),
        stepSeconds:'15'
      }));
    } catch (error) {
      historyError = error;
      historyChart?.destroy(); historyChart = null; lastHistory = null;
      put('history-status', `Histórico no disponible: ${error.message}`);
    }
    const definition = catalog.find(m => m.id === metric);
    if (definition) put('metric-description', `${definition.description} Unidad original: ${definition.unit}.`);
    put('request-status', historyError
      ? `Valores actuales disponibles · ${historyError.message}`
      : `Actualizado ${new Date().toLocaleTimeString()} · zona ${Intl.DateTimeFormat().resolvedOptions().timeZone}`);
  } catch (error) {
    tableRows = []; renderTable();
    for (const id of ['summary-nodes','summary-valid','stat-mean','stat-max','stat-min','stat-above']) put(id, '—');
    for (const id of ['summary-origin','summary-quality']) put(id, 'Sin consulta vigente');
    historyChart?.destroy(); historyChart = null; lastHistory = null;
    put('current-status','Consulta no disponible'); put('history-status','Consulta no disponible'); put('warnings','');
    put('request-status', error.message);
  } finally {
    refreshing = false;
    $('refresh').disabled = false;
    for (const id of ['metric','cluster','node','period']) $(id).disabled = false;
    refreshTimer = setTimeout(refreshMetrics, 30000);
  }
}
async function startMonitoring() {
  try {
    initTable(); initCompare();
    catalog = await metricRequest('catalog');
    options('metric', catalog.map(m => [m.id, names[m.id] || m.id]));
    $('refresh').onclick = refreshMetrics;
    for (const id of ['metric','cluster','node','period']) $(id).onchange = refreshMetrics;
    await refreshMetrics();
  } catch (error) { put('request-status',error.message); $('refresh').onclick = startMonitoring; }
}
window.addEventListener('pagehide', () => clearTimeout(refreshTimer));
