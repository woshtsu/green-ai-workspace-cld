/* Construcción y validación del cuerpo de /api/recommendations/v1/energy. Lógica pura.
   La potencia a partir de la CPU es un MODELO lineal (P = P_idle + (P_max − P_idle) × CPU), no una medición. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.GreenEnergy = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const IDLE_FRACTION = 0.4;           // fracción de P_max consumida en reposo (supuesto visible en la interfaz)
  const MAX_SAMPLES = 10000;
  const ok = v => typeof v === 'number' && Number.isFinite(v);

  function modelPower(cpuRatio, maxWatts, idleFraction = IDLE_FRACTION) {
    if (!ok(cpuRatio) || !ok(maxWatts) || maxWatts <= 0) return null;
    const idle = maxWatts * idleFraction;
    const clamped = Math.min(1, Math.max(0, cpuRatio));
    return idle + (maxWatts - idle) * clamped;
  }

  /** Suma la potencia modelada de todos los nodos de `payload` (CPU en ratio 0–1) en cada instante.
   *  Solo emite instantes en los que TODOS los nodos tienen dato válido, para no subestimar el total. */
  function buildPowerSamples(payload, maxWattsById, idleFraction = IDLE_FRACTION) {
    const series = (payload.series || []).filter(s => ok(maxWattsById[s.resource.id]));
    if (!series.length) return { samples: [], nodes: 0, skipped: 0 };
    const perStamp = new Map();
    for (const s of series) {
      for (const sample of s.samples) {
        if (sample.quality !== 'valid' || !ok(sample.value)) continue;
        const watts = modelPower(sample.value, maxWattsById[s.resource.id], idleFraction);
        if (watts === null) continue;
        const entry = perStamp.get(sample.timestamp) || { watts: 0, n: 0 };
        entry.watts += watts; entry.n += 1;
        perStamp.set(sample.timestamp, entry);
      }
    }
    const all = [...perStamp.entries()].sort((a, b) => a[0].localeCompare(b[0]));
    const full = all.filter(([, e]) => e.n === series.length);
    let samples = full.map(([timestamp, e]) => ({ timestamp, watts: Math.round(e.watts * 100) / 100 }));
    if (samples.length > MAX_SAMPLES) {
      const step = Math.ceil(samples.length / MAX_SAMPLES);
      samples = samples.filter((_, i) => i % step === 0);
    }
    return { samples, nodes: series.length, skipped: all.length - full.length };
  }

  function exampleBody() {
    const base = Date.UTC(2026, 9, 28, 0, 0, 0);
    const watts = [220, 240, 310, 380, 420, 410, 360, 300, 260, 240, 230, 225];
    return { origin: 'simulated',
      samples: watts.map((w, i) => ({ timestamp: new Date(base + i * 300000).toISOString().replace('.000Z', 'Z'), watts: w })) };
  }

  function withFactor(body, factor, source) {
    const hasF = factor !== '' && factor != null, hasS = String(source || '').trim() !== '';
    if (!hasF && !hasS) return { ...body };
    if (hasF !== hasS) throw new Error('Para calcular CO₂e indica el factor de emisión y su fuente (o deja ambos vacíos).');
    const n = Number(factor);
    if (!ok(n) || n < 0 || n > 100) throw new Error('El factor de emisión debe estar entre 0 y 100 kg CO₂e/kWh.');
    return { ...body, emissionFactorKgPerKwh: n, emissionFactorSource: String(source).trim().slice(0, 500) };
  }

  /** Comprueba el cuerpo contra el contrato (EnergyRequest). Devuelve lista de problemas (vacía si es válido). */
  function validateEnergyBody(body) {
    const errors = [];
    if (!body || typeof body !== 'object') return ['El contenido no es un objeto JSON.'];
    const allowed = new Set(['origin', 'samples', 'emissionFactorKgPerKwh', 'emissionFactorSource']);
    for (const k of Object.keys(body)) if (!allowed.has(k)) errors.push(`Campo no permitido: ${k}.`);
    if (!['observed', 'simulated', 'estimated'].includes(body.origin)) errors.push('"origin" debe ser observed, simulated o estimated.');
    if (!Array.isArray(body.samples)) errors.push('"samples" debe ser una lista.');
    else {
      if (body.samples.length < 2) errors.push('Se necesitan al menos 2 muestras.');
      if (body.samples.length > MAX_SAMPLES) errors.push(`Máximo ${MAX_SAMPLES} muestras.`);
      body.samples.slice(0, MAX_SAMPLES).forEach((s, i) => {
        if (!s || !Number.isFinite(Date.parse(s.timestamp)) || !/(Z|[+-]\d\d:?\d\d)$/.test(String(s.timestamp))) errors.push(`Muestra ${i + 1}: "timestamp" debe ser fecha ISO con zona (ej. 2026-10-28T00:00:00Z).`);
        if (!s || !ok(s.watts) || s.watts < 0) errors.push(`Muestra ${i + 1}: "watts" debe ser un número ≥ 0.`);
      });
    }
    const f = body.emissionFactorKgPerKwh, s = body.emissionFactorSource;
    if ((f != null) !== (s != null)) errors.push('El factor de emisión y su fuente van juntos.');
    if (f != null && (!ok(f) || f < 0 || f > 100)) errors.push('El factor de emisión debe estar entre 0 y 100.');
    return errors.slice(0, 8);
  }

  /** Horas que tardaría un servidor de `watts` en consumir `kwh`. */
  function equivalentHours(kwh, watts = 450) {
    return ok(kwh) && watts > 0 ? (kwh * 1000) / watts : null;
  }

  return { IDLE_FRACTION, MAX_SAMPLES, modelPower, buildPowerSamples, exampleBody, withFactor, validateEnergyBody, equivalentHours };
});
