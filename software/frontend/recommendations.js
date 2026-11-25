/* Recommendations are proposals for human review. No infrastructure action is sent. */
function readDemoTelemetry(resource) {
  const timestamp = document.getElementById('policy-time').value;
  if (!timestamp) return null;
  const number = id => {
    const value = document.getElementById(id).value.trim();
    return value === '' ? null : Number(value);
  };
  return {resource, observedAt: new Date(timestamp).toISOString(),
    origin: document.getElementById('policy-origin').value,
    memoryPercent: number('policy-memory'), latencyP95Ms: number('policy-latency'),
    errorRatePercent: number('policy-errors')};
}

/* Muestra un error con el panel amigable si la interfaz lo soporta; si no, el mensaje de texto. */
function reportProblem(prefix, error, context, retry) {
  let friendly = error && error.friendly;
  if (!friendly && typeof GreenErrors !== 'undefined' && error && ['TimeoutError', 'AbortError', 'TypeError'].includes(error.name)) {
    friendly = GreenErrors.fromException(error, context);
  }
  const box = document.getElementById(`${prefix}-problem`);
  if (friendly && typeof GreenUI !== 'undefined' && box && typeof box.append === 'function') {
    put(`${prefix}-status`, '');
    GreenUI.renderProblem(box, friendly, { onRetry: retry });
    return;
  }
  put(`${prefix}-status`, friendly ? `${friendly.titulo}. ${friendly.mensaje}` : error.message);
}
function clearProblem(prefix) {
  const box = document.getElementById(`${prefix}-problem`);
  if (typeof GreenUI !== 'undefined' && box && typeof box.append === 'function') GreenUI.clearProblem(box);
}

/* ---------- HU-07: decisión humana (registro de auditoría; no ejecuta cambios) ---------- */
let currentRecommendation = null;
function currentRole() { return document.getElementById('user-role-badge')?.textContent?.trim().toUpperCase() || ''; }

async function decisionRequest(recommendationId, options = {}) {
  const response = await authenticatedFetch(`${GATEWAY_BASE_URL}${GreenDecisions.decisionsPath(recommendationId)}`, {
    ...options, signal: AbortSignal.timeout(35000) });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = typeof body.detail === 'string' ? body.detail : (body.message || '');
    const text = GreenDecisions.friendlyError(response.status, detail, currentRole())
      || (typeof GreenErrors !== 'undefined' ? GreenErrors.classify({status: response.status, body, context: 'recomendacion'}).mensaje : 'No se pudo completar la operación.');
    throw new Error(text);
  }
  return body;
}

function renderDecisions(list) {
  const ul = document.getElementById('decision-list');
  if (!ul) return;
  ul.replaceChildren(...(list.length ? list : [null]).map(d => {
    const li = document.createElement('li');
    li.textContent = d ? GreenDecisions.describe(d) : 'Sin decisiones registradas.';
    return li;
  }));
}

async function loadDecisions(recommendation) {
  try {
    renderDecisions(GreenDecisions.normalizeList(await decisionRequest(recommendation.recommendationId)));
  } catch (error) { put('decision-status', `No se pudo cargar la lista de decisiones. ${error.message}`); }
}

/* Muestra el panel solo para la recomendación vigente; VIEWER ve la lista pero no los botones. */
function showDecisionPanel(recommendation) {
  currentRecommendation = recommendation;
  const panel = document.getElementById('decision-panel');
  if (!panel || typeof GreenDecisions === 'undefined' || typeof document.createElement !== 'function') return;
  panel.hidden = !recommendation;
  put('decision-status', '');
  const comment = document.getElementById('decision-comment'); if (comment) comment.value = '';
  const actions = document.getElementById('decision-actions');
  if (actions) actions.hidden = !recommendation || !GreenDecisions.canDecide(currentRole());
  renderDecisions([]);
  if (recommendation) loadDecisions(recommendation);
}

async function submitDecision(decision) {
  const rec = currentRecommendation;
  if (!rec || !GreenDecisions.isCurrent(currentRecommendation, rec)) { put('decision-status', 'Evalúa la recomendación antes de decidir.'); return; }
  const buttons = ['decision-approve', 'decision-reject'].map(id => document.getElementById(id));
  buttons.forEach(b => { if (b) b.disabled = true; });
  try {
    const payload = GreenDecisions.buildPayload(decision, document.getElementById('decision-comment')?.value, rec);
    put('decision-status', 'Registrando decisión…');
    await decisionRequest(rec.recommendationId, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload) });
    if (currentRecommendation !== rec) return;   // los datos cambiaron mientras tanto
    put('decision-status', `Decisión registrada. ${GreenDecisions.FIXED_NOTICE}.`);
    await loadDecisions(rec);
  } catch (error) { put('decision-status', error.message); }
  finally { buttons.forEach(b => { if (b) b.disabled = false; }); }
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('decision-approve')?.addEventListener('click', () => submitDecision('APPROVED'));
  document.getElementById('decision-reject')?.addEventListener('click', () => submitDecision('REJECTED'));
  /* Si el usuario cambia los datos, la recomendación anterior deja de poder decidirse. */
  ['policy-memory', 'policy-latency', 'policy-errors', 'policy-time', 'policy-origin', 'cluster', 'node', 'policy-example', 'policy-now']
    .forEach(id => {
      const el = document.getElementById(id);
      if (!el) return;
      el.addEventListener(el.tagName === 'BUTTON' ? 'click' : 'input', () => { if (currentRecommendation) { showDecisionPanel(null); put('recommendation-status', 'Los datos cambiaron: evalúa de nuevo para poder decidir.'); } });
      if (el.tagName === 'SELECT') el.addEventListener('change', () => { if (currentRecommendation) { showDecisionPanel(null); put('recommendation-status', 'Los datos cambiaron: evalúa de nuevo para poder decidir.'); } });
    });
  const form = document.getElementById('recommendation-form');
  if (!form) return;
  const button = document.getElementById('recommend-button');
  let busy = false;
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (busy) return;
    const cluster = document.getElementById('cluster').value;
    const id = document.getElementById('node').value;
    put('recommendation-result', ''); clearProblem('recommendation'); showDecisionPanel(null);
    if (!cluster || !id) { put('recommendation-status', 'Selecciona un clúster y un nodo.'); return; }
    busy = true; button.disabled = true;
    try {
      const telemetry = readDemoTelemetry({type:'node', cluster, id});
      put('recommendation-status', 'Preparando predicción y evaluando restricciones…');
      const end = new Date(Date.now() - 30000);
      const params = new URLSearchParams({cluster, resourceId:id, stepSeconds:'15',
        start:GreenMetrics.rfc3339Seconds(new Date(end.getTime()-7200000)), end:GreenMetrics.rfc3339Seconds(end)});
      const dataset = await predictionRequest(`/api/processing/v1/prediction/dataset?${params}`);
      const result = await predictionRequest('/api/recommendations/v1/recommendations', {
        method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({dataset,telemetry})});
      const statuses = {not_evaluable:'No evaluable', blocked:'Bloqueada por restricciones', eligible_for_review:'Lista para revisión humana'};
      const actions = {none:'Sin propuesta', maintain:'Mantener capacidad', review_capacity_reduction:'Revisar posible reducción de capacidad', review_capacity_increase:'Revisar aumento de capacidad'};
      if (!statuses[result.status] || !actions[result.action] || result.executionAllowed !== false
          || result.resource?.id !== id || result.resource?.cluster !== cluster) throw new Error('Respuesta de recomendación inválida.');
      put('recommendation-status', `${statuses[result.status]} · ${cluster} / ${id}`);
      const labels = {prediction_freshness:'Vigencia de la predicción', telemetry_identity_and_freshness:'Recurso y vigencia de telemetría', memoryPercent:'Memoria', latencyP95Ms:'Latencia p95', errorRatePercent:'Errores'};
      const checks = {pass:'Cumple', fail:'Excede límite', unknown:'Sin evidencia suficiente'};
      put('recommendation-result', `${actions[result.action]}\n${result.checks.map(c => `${labels[c.name] || c.name}: ${checks[c.status] || c.status}`).join('\n')}\nLímites demo: CPU ${result.policy.cpuLowPercent}–${result.policy.cpuHighPercent} %, memoria ≤${result.policy.memoryMaxPercent} %, p95 ≤${result.policy.latencyP95MaxMs} ms, errores ≤${result.policy.errorRateMaxPercent} %.\n${result.warnings.join('\n')}\nReferencia: ${result.recommendationId}`);
      showDecisionPanel(result);
    } catch (error) { reportProblem('recommendation', error, 'recomendacion', () => button.click && button.click()); }
    finally { busy = false; button.disabled = false; }
  });
  const energyForm = document.getElementById('energy-form');
  let energyBusy = false;
  energyForm.addEventListener('submit', async event => {
    event.preventDefault();
    if (energyBusy) return;
    const file = document.getElementById('energy-file').files[0];
    if (!file) { put('energy-status', 'Elige un archivo JSON, o usa el simulador o el ejemplo.'); return; }
    if (file.size > 1500000) { put('energy-status', 'El archivo supera 1,5 MB.'); return; }
    energyBusy = true;
    document.getElementById('energy-button').disabled = true;
    put('energy-status', 'Integrando muestras de potencia…');
    try {
      let body = JSON.parse(await file.text());
      if (typeof GreenEnergy !== 'undefined') {
        body = GreenEnergy.withFactor(body, document.getElementById('energy-factor')?.value ?? '', document.getElementById('energy-factor-source')?.value ?? '');
      }
      const result = await predictionRequest('/api/recommendations/v1/energy', {
        method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
      if (!Number.isFinite(result.energyKwh) || result.energyKwh < 0
          || (result.co2eKg !== null && (!Number.isFinite(result.co2eKg) || result.co2eKg < 0))) throw new Error('Resultado de energía inválido.');
      if (typeof showEnergyResult === 'function') showEnergyResult(result);
      put('energy-status', `${result.energyKwh.toFixed(6)} kWh (modelada) · ${result.co2eKg === null ? 'CO₂e no evaluable: falta factor' : result.co2eKg.toFixed(6)+' kg CO₂e (estimado)'} · ${GreenMetrics.origin(result.origin)}\n${result.start} — ${result.end}\n${result.warnings.join(' ')}`);
    } catch (error) { if (error instanceof SyntaxError) put('energy-status', 'El archivo no es un JSON válido.'); else reportProblem('energy', error, 'energia', () => document.getElementById('energy-button').click && document.getElementById('energy-button').click()); }
    finally { energyBusy = false; document.getElementById('energy-button').disabled = false; }
  });
});
