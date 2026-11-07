/* ==================================================================
   RACKS CON CALOR — Lógica pura y controlador visual
   Green AI · Observatorio
   ================================================================== */

/**
 * Convierte un ratio de utilización (0..1) a porcentaje (0..100).
 * Retorna null si el valor es nulo, indefinido o no finito.
 */
function ratioToPercent(ratio) {
  if (ratio === null || ratio === undefined || !Number.isFinite(ratio)) {
    return null;
  }
  return ratio * 100;
}

/**
 * Formatea un valor de CPU (%) para visualización accesible.
 * Retorna 'Sin dato' si no hay dato válido.
 */
function formatCpu(cpuPercent) {
  if (cpuPercent === null || cpuPercent === undefined || !Number.isFinite(cpuPercent)) {
    return 'Sin dato';
  }
  return `${Math.round(cpuPercent)} %`;
}

/**
 * Categoría semántica según umbrales de utilización:
 * - < 40 %: 'green' (verde)
 * - 40 % .. 80 %: 'amber' (ámbar)
 * - > 80 %: 'red' (rojo)
 * - sin dato: 'nodata'
 */
function getCpuCategory(cpuPercent) {
  if (cpuPercent === null || cpuPercent === undefined || !Number.isFinite(cpuPercent)) {
    return 'nodata';
  }
  if (cpuPercent < 40) return 'green';
  if (cpuPercent <= 80) return 'amber';
  return 'red';
}

/**
 * Código de color hexadecimal para la celda según umbrales:
 * - < 40 %: #10b981 (verde neon)
 * - 40 % .. 80 %: #f59e0b (ámbar neon)
 * - > 80 %: #ef4444 (rojo neon)
 * - sin dato: #64748b (neutro)
 */
function getCpuColor(cpuPercent) {
  const category = getCpuCategory(cpuPercent);
  switch (category) {
    case 'green': return '#10b981';
    case 'amber': return '#f59e0b';
    case 'red': return '#ef4444';
    default: return '#64748b';
  }
}

/**
 * Construye la etiqueta accesible aria-label para una celda de servidor.
 * Formato requerido: «HW001, Rack-01, CPU 63 %» o «HW001, Rack-01, CPU Sin dato».
 */
function buildAriaLabel(node) {
  const cpuStr = formatCpu(node.cpu);
  return `${node.id}, ${node.rack}, CPU ${cpuStr}`;
}

/**
 * Agrupa una lista de nodos por rack ('Rack-01'..'Rack-05').
 * Permite inyectar métricas mediante un Map o diccionario (id -> { cpu, cluster, ... }).
 */
function groupByRack(nodes, metricsMap = null) {
  const grouped = {};
  if (!Array.isArray(nodes)) return grouped;

  for (const node of nodes) {
    const rack = node.rack || 'Rack-01';
    if (!grouped[rack]) grouped[rack] = [];

    let nodeMetric = null;
    if (metricsMap instanceof Map) {
      nodeMetric = metricsMap.get(node.id);
    } else if (metricsMap && typeof metricsMap === 'object') {
      nodeMetric = metricsMap[node.id];
    }

    const cpuVal = nodeMetric?.cpu !== undefined
      ? nodeMetric.cpu
      : (node.cpu !== undefined ? node.cpu : null);

    const clusterVal = nodeMetric?.cluster || node.cluster || null;

    grouped[rack].push({
      ...node,
      cpu: cpuVal,
      cluster: clusterVal
    });
  }

  return grouped;
}

/**
 * Calcula las 3 tarjetas de resumen superior:
 * - highCpuCount: nodos con CPU > 80 %
 * - avgCpu: CPU media de nodos con datos válidos (o null si no hay datos)
 * - busiestRack: rack con mayor promedio de CPU (o null)
 * - busiestRackAvg: promedio de CPU del rack más cargado (o null)
 */
function computeSummary(nodes) {
  if (!Array.isArray(nodes) || nodes.length === 0) {
    return {
      highCpuCount: 0,
      avgCpu: null,
      busiestRack: null,
      busiestRackAvg: null,
      validNodesCount: 0,
      totalNodes: 0
    };
  }

  const validNodes = nodes.filter(n => n.cpu !== null && Number.isFinite(n.cpu));
  const highCpuCount = validNodes.filter(n => n.cpu > 80).length;
  const avgCpu = validNodes.length > 0
    ? validNodes.reduce((acc, n) => acc + n.cpu, 0) / validNodes.length
    : null;

  const rackStats = {};
  for (const n of nodes) {
    const rack = n.rack;
    if (!rack) continue;
    if (!rackStats[rack]) rackStats[rack] = { sum: 0, count: 0 };
    if (n.cpu !== null && Number.isFinite(n.cpu)) {
      rackStats[rack].sum += n.cpu;
      rackStats[rack].count += 1;
    }
  }

  let busiestRack = null;
  let maxRackAvg = -1;
  for (const [rack, data] of Object.entries(rackStats)) {
    if (data.count > 0) {
      const avg = data.sum / data.count;
      if (avg > maxRackAvg) {
        maxRackAvg = avg;
        busiestRack = rack;
      }
    }
  }

  return {
    highCpuCount,
    avgCpu,
    busiestRack,
    busiestRackAvg: busiestRack ? maxRackAvg : null,
    validNodesCount: validNodes.length,
    totalNodes: nodes.length
  };
}

/**
 * Procesa la respuesta de métricas actuales del Gateway:
 * GET /api/monitoring/v1/metrics/current?metric=node.cpu.utilization
 * Devuelve un Map (nodeId -> { cpu (en %), cluster, timestamp, quality, origin }).
 */
function parseMetricsResponse(payload) {
  const map = new Map();
  if (!payload || !Array.isArray(payload.series)) return map;

  for (const series of payload.series) {
    const id = series.resource?.id;
    if (!id) continue;
    const lastSample = series.samples?.at(-1);
    const isValid = lastSample && lastSample.quality === 'valid' && Number.isFinite(lastSample.value);

    map.set(id, {
      cpu: isValid ? ratioToPercent(lastSample.value) : null,
      cluster: series.resource?.cluster || null,
      quality: lastSample?.quality || 'missing',
      origin: series.origin || 'simulated',
      timestamp: lastSample?.timestamp || null
    });
  }
  return map;
}

/* ==================================================================
   CONTROLADOR DEL NAVEGADOR (DOM / FETCH)
   ================================================================== */

let cachedRacksData = null;
let currentGroupedRacks = {};
let selectedNodeId = null;
let autoRefreshTimer = null;
let isRefreshing = false;
let lastPrediction = null;

function resolveApiError(err, status = null) {
  if (typeof mapApiError === 'function') {
    return mapApiError(err, status);
  }
  if (typeof window !== 'undefined' && window.GreenPMV2?.mapApiError) {
    return window.GreenPMV2.mapApiError(err, status);
  }
  try {
    const pmv2 = require('./pmv2.js');
    if (typeof pmv2.mapApiError === 'function') {
      return pmv2.mapApiError(err, status);
    }
  } catch (_e) {}

  if (!err && !status) return 'Error desconocido';
  const statusCode = status || (typeof err === 'object' && err !== null ? (err.status || err.statusCode) : null);
  if (statusCode === 403 || statusCode === '403') return 'Tu rol solo permite lectura';

  let code = '';
  let msg = '';
  let detail = '';
  if (typeof err === 'string') {
    msg = err;
  } else if (err && typeof err === 'object') {
    code = err.code != null ? String(err.code) : '';
    msg = err.message != null ? String(err.message) : '';
    if (typeof err.detail === 'string') {
      detail = err.detail;
    } else if (err.detail && typeof err.detail === 'object') {
      detail = Array.isArray(err.detail)
        ? err.detail.map(d => d.msg || JSON.stringify(d)).join('; ')
        : (err.detail.message || JSON.stringify(err.detail));
    }
  }
  const comb = `${code} ${msg} ${detail}`.trim();
  if (code === '403' || comb.includes('403') || comb.toLowerCase().includes('permiso')) {
    return 'Tu rol solo permite lectura';
  }
  if (
    code === 'INSUFFICIENT_DATA' || code === 'INVALID_DATASET' ||
    detail === 'INSUFFICIENT_DATA' || detail === 'INVALID_DATASET' ||
    msg === 'INSUFFICIENT_DATA' || msg === 'INVALID_DATASET' ||
    /INSUFFICIENT_DATA|INVALID_DATASET/i.test(comb) || comb.includes('ventana de CPU')
  ) {
    return 'Datos insuficientes: el simulador necesita ~20 min de historial';
  }
  return detail || msg || code || 'Error al procesar la solicitud';
}

async function loadRacksInventory() {
  if (cachedRacksData) return cachedRacksData;
  const res = await fetch('racks.json');
  if (!res.ok) throw new Error('No se pudo cargar racks.json.');
  cachedRacksData = await res.json();
  return cachedRacksData;
}

async function fetchCurrentMetrics() {
  const gatewayUrl = typeof GATEWAY_BASE_URL !== 'undefined'
    ? GATEWAY_BASE_URL
    : (window.GREEN_AI_CONFIG?.gatewayBaseUrl || 'http://127.0.0.1:8081').replace(/\/$/, '');
  const url = `${gatewayUrl}/api/monitoring/v1/metrics/current?metric=node.cpu.utilization`;

  const fetchFn = typeof authenticatedFetch === 'function' ? authenticatedFetch : fetch;
  const res = await fetchFn(url);
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Error al consultar métricas de CPU (HTTP ${res.status})`);
  }
  return res.json();
}

function renderSummaryCards(summary) {
  const highCpuEl = document.getElementById('kpi-high-cpu');
  const avgCpuEl = document.getElementById('kpi-avg-cpu');
  const busiestRackEl = document.getElementById('kpi-busiest-rack');
  const busiestNoteEl = document.getElementById('kpi-busiest-note');

  if (highCpuEl) highCpuEl.textContent = String(summary.highCpuCount);
  if (avgCpuEl) {
    avgCpuEl.textContent = summary.avgCpu !== null
      ? `${new Intl.NumberFormat('es-PE', { maximumFractionDigits: 1 }).format(summary.avgCpu)} %`
      : 'Sin dato';
  }
  if (busiestRackEl) {
    busiestRackEl.textContent = summary.busiestRack || 'Sin dato';
  }
  if (busiestNoteEl) {
    busiestNoteEl.textContent = summary.busiestRack
      ? `${formatCpu(summary.busiestRackAvg)} media`
      : 'Sin datos utilizables';
  }
}

function selectNode(node) {
  const isDifferentNode = selectedNodeId !== node.id;
  selectedNodeId = node.id;

  // Actualizar estado activo en los botones de celda
  document.querySelectorAll('.rack-node-cell').forEach(btn => {
    btn.classList.toggle('is-selected', btn.dataset.nodeId === node.id);
  });

  // Mostrar detalle en el panel lateral
  const placeholder = document.getElementById('detail-placeholder');
  const content = document.getElementById('detail-content');
  if (placeholder) placeholder.hidden = true;
  if (content) content.hidden = false;

  const idEl = document.getElementById('detail-id');
  const rackEl = document.getElementById('detail-rack');
  const hostnameEl = document.getElementById('detail-hostname');
  const cpuEl = document.getElementById('detail-cpu');
  const coresEl = document.getElementById('detail-cores');
  const wattsEl = document.getElementById('detail-watts');
  const predictStatusEl = document.getElementById('predict-status');
  const predictResultEl = document.getElementById('predict-result');
  const valEl = document.getElementById('predict-val');
  const timeEl = document.getElementById('predict-time');

  if (idEl) idEl.textContent = node.id;
  if (rackEl) rackEl.textContent = node.rack;
  if (hostnameEl) hostnameEl.textContent = node.hostname;

  if (cpuEl) {
    const category = getCpuCategory(node.cpu);
    cpuEl.textContent = formatCpu(node.cpu);
    cpuEl.className = `detail-cpu-val cpu-${category}`;
  }

  if (coresEl) coresEl.textContent = `${node.cpuCores} cores`;
  if (wattsEl) wattsEl.textContent = `${node.maxWatts} W`;

  // Si cambia de nodo, reiniciar estado de predicción.
  // Si sigue siendo el mismo y existe una predicción previa, conservarla.
  if (isDifferentNode) {
    lastPrediction = null;
    if (typeof GreenUI !== 'undefined') GreenUI.clearProblem(document.getElementById('predict-problem'));
    if (predictStatusEl) {
      predictStatusEl.textContent = '';
      predictStatusEl.className = 'detail-status';
    }
    if (predictResultEl) predictResultEl.hidden = true;
  } else if (lastPrediction && lastPrediction.nodeId === node.id) {
    if (predictStatusEl && lastPrediction.status) {
      predictStatusEl.textContent = lastPrediction.status;
      predictStatusEl.className = lastPrediction.statusClass || 'detail-status';
    }
    if (predictResultEl && lastPrediction.val) {
      if (valEl) valEl.textContent = lastPrediction.val;
      if (timeEl) timeEl.textContent = lastPrediction.time;
      predictResultEl.hidden = false;
    }
  }

  const predictBtn = document.getElementById('predict-15m-btn');
  if (predictBtn) {
    predictBtn.disabled = false;
    predictBtn.onclick = () => runNodePrediction(node);
  }
}

async function runNodePrediction(node) {
  const predictBtn = document.getElementById('predict-15m-btn');
  const statusEl = document.getElementById('predict-status');
  const resultBox = document.getElementById('predict-result');
  const valEl = document.getElementById('predict-val');
  const timeEl = document.getElementById('predict-time');

  if (resultBox) resultBox.hidden = true;
  if (typeof GreenUI !== 'undefined') GreenUI.clearProblem(document.getElementById('predict-problem'));

  // Comprobar rol del usuario (si es VIEWER, bloquear antes de llamar)
  const roleBadge = document.getElementById('user-role-badge');
  const role = roleBadge?.textContent?.trim().toUpperCase();
  if (role === 'VIEWER') {
    if (statusEl) {
      statusEl.textContent = 'Tu rol solo permite lectura';
      statusEl.className = 'detail-status status-warning';
    }
    lastPrediction = {
      nodeId: node.id,
      val: null,
      time: '',
      status: 'Tu rol solo permite lectura',
      statusClass: 'detail-status status-warning'
    };
    return;
  }

  if (predictBtn) predictBtn.disabled = true;
  if (statusEl) {
    statusEl.textContent = 'Estimando CPU a 15 min…';
    statusEl.className = 'detail-status';
  }

  try {
    const cluster = node.cluster || 'sim-run-1';
    let predictionFn = window.requestNodePrediction;
    if (typeof predictionFn !== 'function') {
      throw new Error('Función de predicción no disponible.');
    }

    const { result } = await predictionFn(cluster, node.id);

    const formattedVal = `${new Intl.NumberFormat('es-PE', { maximumFractionDigits: 1 }).format(result.value)} % · Estimado`;
    const formattedTime = `Horizonte: ${result.horizon || '15m'} · Para: ${new Date(result.predictedFor).toLocaleTimeString()}`;

    if (valEl) {
      valEl.textContent = formattedVal;
    }
    if (timeEl) {
      timeEl.textContent = formattedTime;
    }
    if (resultBox) resultBox.hidden = false;
    if (statusEl) {
      statusEl.textContent = 'Estimación completada con éxito';
      statusEl.className = 'detail-status status-success';
    }

    lastPrediction = {
      nodeId: node.id,
      val: formattedVal,
      time: formattedTime,
      status: 'Estimación completada con éxito',
      statusClass: 'detail-status status-success'
    };
  } catch (error) {
    const friendly = error.friendly || (typeof GreenErrors !== 'undefined' && ['TimeoutError', 'AbortError', 'TypeError'].includes(error.name) ? GreenErrors.fromException(error, 'prediccion') : null);
    const problemBox = document.getElementById('predict-problem');
    if (friendly && friendly.tipo !== 'permisos' && typeof GreenUI !== 'undefined' && problemBox) {
      if (statusEl) { statusEl.textContent = ''; statusEl.className = 'detail-status'; }
      GreenUI.renderProblem(problemBox, friendly, { onRetry: () => predictBtn && predictBtn.click() });
      lastPrediction = { nodeId: node.id, val: null, time: '', status: '', statusClass: 'detail-status' };
      return;
    }
    const errorMsg = resolveApiError(error);
    const isForbidden = errorMsg.includes('solo permite lectura')
      || error.status === 403
      || error.message?.includes('403');

    if (statusEl) {
      statusEl.textContent = errorMsg;
      statusEl.className = isForbidden ? 'detail-status status-warning' : 'detail-status status-error';
    }

    lastPrediction = {
      nodeId: node.id,
      val: null,
      time: '',
      status: errorMsg,
      statusClass: isForbidden ? 'detail-status status-warning' : 'detail-status status-error'
    };
  } finally {
    if (predictBtn) predictBtn.disabled = false;
  }
}

function renderRacksView(groupedRacks) {
  const container = document.getElementById('racks-container');
  if (!container) return;
  container.replaceChildren();

  const rackNames = Object.keys(groupedRacks).sort();

  for (const rackName of rackNames) {
    const nodes = groupedRacks[rackName] || [];
    const col = document.createElement('article');
    col.className = 'rack-column glass-panel';

    const header = document.createElement('div');
    header.className = 'rack-column-header';
    header.innerHTML = `
      <div class="rack-title-row">
        <h3>${rackName}</h3>
        <span class="rack-badge">${nodes.length} srv</span>
      </div>
    `;
    col.appendChild(header);

    const shelf = document.createElement('div');
    shelf.className = 'rack-shelf';
    shelf.setAttribute('role', 'group');
    shelf.setAttribute('aria-label', rackName);

    for (const node of nodes) {
      const cat = getCpuCategory(node.cpu);
      const ariaLabel = buildAriaLabel(node);
      const isSelected = selectedNodeId === node.id;

      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = `rack-node-cell cpu-${cat}${isSelected ? ' is-selected' : ''}`;
      btn.setAttribute('aria-label', ariaLabel);
      btn.dataset.nodeId = node.id;
      btn.innerHTML = `
        <span class="cell-id">${node.id}</span>
        <strong class="cell-val">${node.cpu !== null ? Math.round(node.cpu) + '%' : '—'}</strong>
      `;

      btn.addEventListener('click', () => {
        selectNode(node);
      });

      shelf.appendChild(btn);
    }

    col.appendChild(shelf);
    container.appendChild(col);
  }
}

async function refreshRacks() {
  if (isRefreshing) return;
  isRefreshing = true;
  clearTimeout(autoRefreshTimer);

  const refreshBtn = document.getElementById('refresh-racks-btn');
  const lastUpdateEl = document.getElementById('last-update');
  if (refreshBtn) refreshBtn.disabled = true;

  try {
    const inventory = await loadRacksInventory();
    let metricsMap = new Map();
    let metricsError = null;

    try {
      const payload = await fetchCurrentMetrics();
      metricsMap = parseMetricsResponse(payload);
    } catch (err) {
      metricsError = err;
      console.warn('No se pudieron obtener métricas en vivo:', err.message);
    }

    currentGroupedRacks = groupByRack(inventory.nodes || [], metricsMap);
    const allEnrichedNodes = Object.values(currentGroupedRacks).flat();
    const summary = computeSummary(allEnrichedNodes);

    renderSummaryCards(summary);
    renderRacksView(currentGroupedRacks);

    // Conservar el nodo seleccionado y el último resultado de predicción entre refrescos de 15 s
    // (no re-renderizar el panel si el nodo sigue seleccionado)
    if (selectedNodeId) {
      const updatedNode = allEnrichedNodes.find(n => n.id === selectedNodeId);
      if (updatedNode) {
        const cpuEl = document.getElementById('detail-cpu');
        if (cpuEl) {
          const category = getCpuCategory(updatedNode.cpu);
          cpuEl.textContent = formatCpu(updatedNode.cpu);
          cpuEl.className = `detail-cpu-val cpu-${category}`;
        }
        const predictBtn = document.getElementById('predict-15m-btn');
        if (predictBtn && !predictBtn.disabled) {
          predictBtn.onclick = () => runNodePrediction(updatedNode);
        }
      }
    }

    if (lastUpdateEl) {
      const timeStr = new Date().toLocaleTimeString();
      lastUpdateEl.textContent = metricsError
        ? `Inventario cargado · Métricas pendientes (${metricsError.message})`
        : `Actualizado ${timeStr} · cada 15 s`;
    }
  } catch (error) {
    if (lastUpdateEl) {
      lastUpdateEl.textContent = `Error al actualizar: ${error.message}`;
    }
  } finally {
    isRefreshing = false;
    if (refreshBtn) refreshBtn.disabled = false;
    autoRefreshTimer = setTimeout(refreshRacks, 15000);
  }
}

function initRacksView() {
  const refreshBtn = document.getElementById('refresh-racks-btn');
  if (refreshBtn) refreshBtn.addEventListener('click', refreshRacks);
  refreshRacks();
}

if (typeof window !== 'undefined') {
  window.addEventListener('pagehide', () => clearTimeout(autoRefreshTimer));
  document.addEventListener('DOMContentLoaded', () => {
    // Solo inicializar si estamos en la vista de racks (network.html)
    if (document.getElementById('racks-container')) {
      initRacksView();
    }
  });

  window.GreenRacks = {
    ratioToPercent,
    formatCpu,
    getCpuCategory,
    getCpuColor,
    buildAriaLabel,
    groupByRack,
    computeSummary,
    parseMetricsResponse,
    resolveApiError,
    mapApiError: resolveApiError,
    refreshRacks,
    initRacksView
  };
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    ratioToPercent,
    formatCpu,
    getCpuCategory,
    getCpuColor,
    buildAriaLabel,
    groupByRack,
    computeSummary,
    parseMetricsResponse,
    resolveApiError,
    mapApiError: resolveApiError
  };
}
