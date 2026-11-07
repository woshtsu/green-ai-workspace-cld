/* Interacciones del dashboard que no tocan contratos: instante «ahora», valores de ejemplo y las tres vías de energía. */
(function () {
  const $ = id => document.getElementById(id);
  const pad = n => String(n).padStart(2, '0');
  const localNow = () => { const d = new Date(); return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`; };
  const fmt = (n, digits = 2) => new Intl.NumberFormat('es-PE', { maximumFractionDigits: digits }).format(n);

  /* ---------- Recomendación: hora actual y ejemplo ---------- */
  function initRecommendationHelpers() {
    const time = $('policy-time');
    if (!time) return;
    let dirty = false;
    time.addEventListener('input', () => { dirty = true; });
    if (!time.value) time.value = localNow();
    $('policy-now')?.addEventListener('click', () => { time.value = localNow(); dirty = false; });
    $('policy-example')?.addEventListener('click', () => {
      $('policy-memory').value = '65'; $('policy-latency').value = '120'; $('policy-errors').value = '0.5';
      $('policy-origin').value = 'simulated'; time.value = localNow(); dirty = false;
    });
    window.addEventListener('greenai:tab', event => { if (event.detail.id === 'prediccion' && !dirty) time.value = localNow(); });
  }

  /* ---------- Energía ---------- */
  window.showEnergyResult = function showEnergyResult(result) {
    const box = $('energy-results');
    if (!box) return;
    const card = (label, value, note) => {
      const c = document.createElement('div'); c.className = 'result-card';
      const s = document.createElement('small'); s.textContent = label;
      const b = document.createElement('strong'); b.textContent = value;
      const n = document.createElement('span'); n.textContent = note || '';
      c.append(s, b, n); return c;
    };
    const minutes = Math.max(0, (Date.parse(result.end) - Date.parse(result.start)) / 60000);
    const hours = GreenEnergy.equivalentHours(result.energyKwh, 450);
    box.replaceChildren(
      card('Energía', `${fmt(result.energyKwh, 4)} kWh`, `Método: ${result.method || 'integración trapezoidal'}`),
      card('CO₂e', result.co2eKg === null || result.co2eKg === undefined ? 'No evaluable' : `${fmt(result.co2eKg, 4)} kg`,
        result.co2eKg === null || result.co2eKg === undefined ? 'Falta factor de emisión y su fuente' : `Factor ${fmt(result.emissionFactorKgPerKwh, 4)} kg/kWh · ${result.emissionFactorSource || ''}`),
      card('Periodo', `${fmt(minutes, 0)} min`, `${new Date(result.start).toLocaleString()} — ${new Date(result.end).toLocaleString()}`),
      card('Equivale a', hours === null ? '—' : `${fmt(hours, 1)} h`, 'de un servidor de 450 W a plena carga (kWh × 1000 ÷ 450)'),
      card('Procedencia', GreenMetrics.origin(result.origin), result.origin === 'simulated' ? 'Potencia modelada, no medida' : '')
    );
    if (result.warnings && result.warnings.length) {
      const w = document.createElement('p'); w.className = 'summary-note'; w.style.gridColumn = '1 / -1';
      w.textContent = result.warnings.join(' · '); box.append(w);
    }
    box.hidden = false;
  };

  async function postEnergy(body, label) {
    const status = $('energy-status');
    GreenUI.clearProblem($('energy-problem'));
    if ($('energy-results')) $('energy-results').hidden = true;
    const problems = GreenEnergy.validateEnergyBody(body);
    if (problems.length) { status.textContent = `No se puede calcular: ${problems[0]}`; return; }
    status.textContent = `${label}: integrando ${body.samples.length} muestras…`;
    try {
      const result = await predictionRequest('/api/recommendations/v1/energy', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
      if (!Number.isFinite(result.energyKwh) || result.energyKwh < 0) throw new Error('Resultado de energía inválido.');
      showEnergyResult(result);
      status.textContent = `${label}: ${fmt(result.energyKwh, 4)} kWh calculados. ${result.origin === 'simulated' ? 'Potencia modelada, no medida.' : ''}`;
    } catch (error) {
      reportProblem('energy', error, 'energia', () => $('energy-sim').click());
    }
  }

  function factorFields() {
    return GreenEnergy.withFactor({}, $('energy-factor').value, $('energy-factor-source').value);
  }

  function initEnergy() {
    if (!$('energy-sim')) return;
    $('idle-pct').textContent = String(Math.round(GreenEnergy.IDLE_FRACTION * 100));
    const withFactor = body => { try { return { ...body, ...factorFields() }; } catch (error) { $('energy-status').textContent = error.message; return null; } };

    $('energy-example').addEventListener('click', () => {
      const body = withFactor(GreenEnergy.exampleBody());
      if (body) postEnergy(body, 'Ejemplo');
    });
    $('energy-download').addEventListener('click', () => {
      const blob = new Blob([JSON.stringify(GreenEnergy.exampleBody(), null, 2)], { type: 'application/json' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob); a.download = 'potencia-ejemplo.json'; a.click();
      setTimeout(() => URL.revokeObjectURL(a.href), 2000);
    });
    $('energy-sim').addEventListener('click', async () => {
      const button = $('energy-sim');
      const factor = withFactor({});
      if (!factor) return;
      button.disabled = true;
      $('energy-status').textContent = 'Consultando la CPU del simulador…';
      GreenUI.clearProblem($('energy-problem'));
      try {
        const cluster = $('cluster').value;
        const node = $('node').value;
        const end = new Date();
        const start = new Date(end.getTime() - Number($('period').value) * 60000);
        const params = { metric: 'node.cpu.utilization', resourceType: 'node', ...(cluster ? { cluster } : {}), ...(node ? { resourceId: node } : {}),
          start: GreenMetrics.rfc3339Seconds(start), end: GreenMetrics.rfc3339Seconds(end), stepSeconds: '15' };
        const [history, rack] = await Promise.all([metricRequest('history', params), fetch('racks.json').then(r => r.json())]);
        const maxW = Object.fromEntries(rack.nodes.map(n => [n.id, n.maxWatts]));
        const built = GreenEnergy.buildPowerSamples(history, maxW);
        if (built.samples.length < 2) {
          $('energy-status').textContent = 'Aún no hay suficientes muestras del simulador para este periodo. Espera unos minutos o elige un periodo más largo.';
          return;
        }
        await postEnergy({ origin: 'simulated', samples: built.samples, ...factor },
          `Simulador (${built.nodes} servidores${built.skipped ? `, ${built.skipped} instantes incompletos omitidos` : ''})`);
      } catch (error) {
        reportProblem('energy', error, 'energia', () => $('energy-sim').click());
      } finally { button.disabled = false; }
    });
  }

  document.addEventListener('DOMContentLoaded', () => { initRecommendationHelpers(); initEnergy(); });
})();
