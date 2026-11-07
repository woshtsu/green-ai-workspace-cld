/* ==================================================================
   PMV2 — Lógica pura y controladores visuales (HTML/JS estático)
   Green AI · Observatorio
   ================================================================== */

/**
 * Mapea errores de API a mensajes legibles para el usuario:
 * - INSUFFICIENT_DATA o INVALID_DATASET: «Datos insuficientes: el simulador necesita ~20 min de historial»
 * - 403: «Tu rol solo permite lectura»
 * - Otros: mensaje breve desde detail, message o code.
 */
function mapApiError(errorOrJson, status = null) {
  if (!errorOrJson && !status) return 'Error desconocido';

  const statusCode = status
    || (typeof errorOrJson === 'object' && errorOrJson !== null
        ? (errorOrJson.status || errorOrJson.statusCode)
        : null);

  if (statusCode === 403 || statusCode === '403') {
    return 'Tu rol solo permite lectura';
  }

  let code = '';
  let message = '';
  let detail = '';

  if (typeof errorOrJson === 'string') {
    message = errorOrJson;
  } else if (errorOrJson && typeof errorOrJson === 'object') {
    code = errorOrJson.code != null ? String(errorOrJson.code) : '';
    message = errorOrJson.message != null ? String(errorOrJson.message) : '';

    if (typeof errorOrJson.detail === 'string') {
      detail = errorOrJson.detail;
    } else if (errorOrJson.detail && typeof errorOrJson.detail === 'object') {
      if (Array.isArray(errorOrJson.detail)) {
        detail = errorOrJson.detail.map(d => d.msg || JSON.stringify(d)).join('; ');
      } else {
        code = code || (errorOrJson.detail.code ? String(errorOrJson.detail.code) : '');
        detail = errorOrJson.detail.message || errorOrJson.detail.detail || JSON.stringify(errorOrJson.detail);
      }
    }
  }

  const combined = `${code} ${message} ${detail}`.trim();

  // Comprobar 403 o restricciones de permisos
  if (code === '403' || combined.includes('403') || combined.toLowerCase().includes('permiso')) {
    return 'Tu rol solo permite lectura';
  }

  // Comprobar INSUFFICIENT_DATA o INVALID_DATASET
  if (
    code === 'INSUFFICIENT_DATA' ||
    code === 'INVALID_DATASET' ||
    detail === 'INSUFFICIENT_DATA' ||
    detail === 'INVALID_DATASET' ||
    message === 'INSUFFICIENT_DATA' ||
    message === 'INVALID_DATASET' ||
    /INSUFFICIENT_DATA|INVALID_DATASET/i.test(combined) ||
    combined.includes('ventana de CPU')
  ) {
    return 'Datos insuficientes: el simulador necesita ~20 min de historial';
  }

  // Otros: mensaje breve
  return detail || message || code || 'Error al procesar la solicitud';
}

/**
 * Formatea los datos de experiment.json para presentación accesible:
 * - Riesgo de SLA (baseline frente a Green AI)
 * - Energía modelada (baseline frente a Green AI y delta)
 * - Etiqueta «Datos simulados · energía modelada, no medida»
 */
function formatExperiment(data) {
  const disclaimer = 'Datos simulados · energía modelada, no medida';
  if (!data || typeof data !== 'object') {
    return {
      slaRiskBaseline: 'Sin dato',
      slaRiskGreenAi: 'Sin dato',
      slaDelta: 'Sin dato',
      energyBaseline: 'Sin dato',
      energyGreenAi: 'Sin dato',
      energyDelta: 'Sin dato',
      energyDeltaPct: 'Sin dato',
      disclaimer,
      model: '—',
      horizon: '—',
      intervals: 0
    };
  }

  const fmtPct = val => (val != null && Number.isFinite(val)) ? `${val.toFixed(2)} %` : '—';
  const fmtWh = val => (val != null && Number.isFinite(val)) ? `${val.toFixed(2)} Wh` : '—';
  const fmtDeltaWh = val => {
    if (val == null || !Number.isFinite(val)) return '—';
    const sign = val > 0 ? '+' : '';
    return `${sign}${val.toFixed(2)} Wh`;
  };
  const fmtDeltaPct = val => {
    if (val == null || !Number.isFinite(val)) return '—';
    const sign = val > 0 ? '+' : '';
    return `${sign}${val.toFixed(2)} %`;
  };

  const b = data.baseline_reactive || {};
  const g = data.green_ai_predictive || {};
  const d = data.delta_green_minus_baseline || {};

  return {
    slaRiskBaseline: fmtPct(b.sla_risk_pct),
    slaRiskGreenAi: fmtPct(g.sla_risk_pct),
    slaDelta: fmtDeltaPct(d.sla_risk_pct),
    energyBaseline: fmtWh(b.modeled_energy_wh),
    energyGreenAi: fmtWh(g.modeled_energy_wh),
    energyDelta: fmtDeltaWh(d.modeled_energy_wh),
    energyDeltaPct: fmtDeltaPct(d.modeled_energy_pct),
    disclaimer,
    model: data.model || '—',
    horizon: data.horizon || '—',
    intervals: b.intervals || g.intervals || 0
  };
}

/**
 * Construye la URL para el reporte de históricos:
 * GET {gatewayBaseUrl}/api/processing/v1/reports/historical-summary?format=json|csv
 */
function buildReportUrl(baseUrl, params = {}) {
  const cleanBase = (baseUrl || '').replace(/\/+$/, '');
  const endpoint = cleanBase.endsWith('/api/processing/v1/reports/historical-summary')
    ? cleanBase
    : `${cleanBase}/api/processing/v1/reports/historical-summary`;

  const searchParams = new URLSearchParams();

  const hwId = params.hardwareId || params.hardware_id;
  if (hwId) searchParams.set('hardwareId', hwId);

  const startVal = params.start || params.desde;
  if (startVal) searchParams.set('start', startVal);

  const endVal = params.end || params.hasta;
  if (endVal) searchParams.set('end', endVal);

  const format = params.format || 'json';
  searchParams.set('format', format);

  const qs = searchParams.toString();
  return qs ? `${endpoint}?${qs}` : endpoint;
}

/**
 * Formatea el resumen histórico de telemetría para mostrar en pantalla.
 */
function formatHistoricalSummary(data) {
  if (!data || typeof data !== 'object') return 'Sin datos en el reporte.';
  return JSON.stringify(data, null, 2);
}

/* ==================================================================
   CONTROLADORES DE INTERFAZ (DOM / RED)
   ================================================================== */

async function loadExperimentData(filePath = 'experiment.json') {
  const res = await fetch(filePath);
  if (!res.ok) {
    throw new Error(`No se pudo cargar ${filePath} (HTTP ${res.status})`);
  }
  return res.json();
}

async function fetchHistoricalSummary(baseUrl, params) {
  const url = buildReportUrl(baseUrl, { ...params, format: 'json' });
  const fetchFn = typeof authenticatedFetch === 'function' ? authenticatedFetch : fetch;
  const res = await fetchFn(url);
  const body = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(mapApiError(body, res.status));
    err.status = res.status;
    err.body = body;
    throw err;
  }
  return body;
}

async function downloadReportCsv(baseUrl, params) {
  const url = buildReportUrl(baseUrl, { ...params, format: 'csv' });
  const fetchFn = typeof authenticatedFetch === 'function' ? authenticatedFetch : fetch;
  const res = await fetchFn(url);
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    const err = new Error(mapApiError(body, res.status));
    err.status = res.status;
    err.body = body;
    throw err;
  }
  const blob = await res.blob();
  if (typeof window !== 'undefined' && window.URL && typeof window.URL.createObjectURL === 'function') {
    const blobUrl = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = blobUrl;
    a.download = `reporte_historico_${params.hardwareId || 'HW045'}_${params.start || params.desde || 'inicio'}_${params.end || params.hasta || 'fin'}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(() => window.URL.revokeObjectURL(blobUrl), 1000);
  }
  return blob;
}

// La API exige zona horaria: los <input type="date"> no la incluyen. Se interpretan en UTC.
function withTimezone(value, endOfDay) {
  if (/^\d{4}-\d{2}-\d{2}$/.test(value)) return `${value}T${endOfDay ? '23:59:59' : '00:00:00'}Z`;
  if (/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?$/.test(value)) return `${value.length === 16 ? value + ':00' : value}Z`;
  return value;
}

function renderExperimentCard(data) {
  const formatted = formatExperiment(data);

  const slaBaselineEl = document.getElementById('exp-sla-baseline');
  const slaGreenEl = document.getElementById('exp-sla-green');
  const slaDeltaEl = document.getElementById('exp-sla-delta');

  const energyBaselineEl = document.getElementById('exp-energy-baseline');
  const energyGreenEl = document.getElementById('exp-energy-green');
  const energyDeltaEl = document.getElementById('exp-energy-delta');

  const disclaimerEl = document.getElementById('experiment-disclaimer');

  if (slaBaselineEl) slaBaselineEl.textContent = formatted.slaRiskBaseline;
  if (slaGreenEl) slaGreenEl.textContent = formatted.slaRiskGreenAi;
  if (slaDeltaEl) slaDeltaEl.textContent = formatted.slaDelta;

  if (energyBaselineEl) energyBaselineEl.textContent = formatted.energyBaseline;
  if (energyGreenEl) energyGreenEl.textContent = formatted.energyGreenAi;
  if (energyDeltaEl) energyDeltaEl.textContent = `${formatted.energyDelta} (${formatted.energyDeltaPct})`;

  if (disclaimerEl) disclaimerEl.textContent = formatted.disclaimer;
}

async function initExperimentSection() {
  const statusEl = document.getElementById('experiment-status');
  try {
    const data = await loadExperimentData('experiment.json');
    renderExperimentCard(data);
    if (statusEl) statusEl.textContent = '';
  } catch (error) {
    if (statusEl) {
      statusEl.textContent = mapApiError(error);
      statusEl.className = 'pmv2-status status-error';
    }
  }
}

function initHistoricalReportForm() {
  const summaryBtn = document.getElementById('report-summary-btn');
  const csvBtn = document.getElementById('report-csv-btn');
  const statusEl = document.getElementById('report-status');
  const resultContainer = document.getElementById('report-summary-container');

  const getFormValues = () => {
    const hardwareId = document.getElementById('report-hardware-id')?.value?.trim() || 'HW045';
    const start = withTimezone(document.getElementById('report-start')?.value || '2026-07-10', false);
    const end = withTimezone(document.getElementById('report-end')?.value || '2026-07-11', true);
    return { hardwareId, start, end };
  };

  const getGatewayUrl = () => {
    return typeof GATEWAY_BASE_URL !== 'undefined'
      ? GATEWAY_BASE_URL
      : (window.GREEN_AI_CONFIG?.gatewayBaseUrl || 'http://127.0.0.1:8081');
  };

  if (summaryBtn) {
    summaryBtn.addEventListener('click', async () => {
      const { hardwareId, start, end } = getFormValues();
      summaryBtn.disabled = true;
      if (statusEl) {
        statusEl.textContent = 'Consultando resumen histórico…';
        statusEl.className = 'pmv2-status';
      }
      if (resultContainer) resultContainer.hidden = true;

      try {
        const data = await fetchHistoricalSummary(getGatewayUrl(), { hardwareId, start, end });
        if (resultContainer) {
          resultContainer.hidden = false;
          const pre = document.createElement('pre');
          pre.style.margin = '0';
          pre.style.whiteSpace = 'pre-wrap';
          pre.textContent = formatHistoricalSummary(data);
          resultContainer.replaceChildren(pre);
        }
        if (statusEl) {
          statusEl.textContent = 'Resumen cargado con éxito';
          statusEl.className = 'pmv2-status status-success';
        }
      } catch (error) {
        if (statusEl) {
          const errorMsg = mapApiError(error.body || error, error.status);
          statusEl.textContent = errorMsg;
          const isForbidden = errorMsg.includes('solo permite lectura') || error.status === 403;
          statusEl.className = isForbidden ? 'pmv2-status status-warning' : 'pmv2-status status-error';
        }
      } finally {
        summaryBtn.disabled = false;
      }
    });
  }

  if (csvBtn) {
    csvBtn.addEventListener('click', async () => {
      const { hardwareId, start, end } = getFormValues();
      csvBtn.disabled = true;
      if (statusEl) {
        statusEl.textContent = 'Descargando reporte CSV…';
        statusEl.className = 'pmv2-status';
      }

      try {
        await downloadReportCsv(getGatewayUrl(), { hardwareId, start, end });
        if (statusEl) {
          statusEl.textContent = 'CSV descargado con éxito';
          statusEl.className = 'pmv2-status status-success';
        }
      } catch (error) {
        if (statusEl) {
          const errorMsg = mapApiError(error.body || error, error.status);
          statusEl.textContent = errorMsg;
          const isForbidden = errorMsg.includes('solo permite lectura') || error.status === 403;
          statusEl.className = isForbidden ? 'pmv2-status status-warning' : 'pmv2-status status-error';
        }
      } finally {
        csvBtn.disabled = false;
      }
    });
  }
}

function initPmv2Section() {
  initHistoricalReportForm();
  initExperimentSection();
}

if (typeof window !== 'undefined') {
  window.GreenPMV2 = {
    mapApiError,
    formatExperiment,
    buildReportUrl,
    formatHistoricalSummary,
    loadExperimentData,
    fetchHistoricalSummary,
    downloadReportCsv,
    renderExperimentCard,
    withTimezone,
    initPmv2Section
  };

  window.mapApiError = mapApiError;
  window.formatExperiment = formatExperiment;
  window.buildReportUrl = buildReportUrl;

  document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('pmv2-section')) {
      initPmv2Section();
    }
  });
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    mapApiError,
    formatExperiment,
    buildReportUrl,
    formatHistoricalSummary,
    loadExperimentData,
    fetchHistoricalSummary,
    downloadReportCsv,
    renderExperimentCard,
    withTimezone,
    initPmv2Section
  };
}
