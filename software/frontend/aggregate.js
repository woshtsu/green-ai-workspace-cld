/* Agregación y paginación para la vista de métricas. Lógica pura (sin DOM).
   Los estadísticos (media, máx, mín, p95) se CALCULAN EN PANTALLA a partir de las series devueltas;
   no son métricas servidas por Monitoring. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.GreenAggregate = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const ok = v => typeof v === 'number' && Number.isFinite(v);

  function percentile(sorted, p) {
    if (!sorted.length) return null;
    const idx = (sorted.length - 1) * p;
    const lo = Math.floor(idx), hi = Math.ceil(idx);
    return sorted[lo] + (sorted[hi] - sorted[lo]) * (idx - lo);
  }

  function validValue(sample, scale) {
    return sample && sample.quality === 'valid' && ok(sample.value) ? sample.value * scale : null;
  }

  function nodeId(series) { return series.resource.id; }

  /** Estadísticos por instante entre todas las series. */
  function historyStats(payload, scale = 1) {
    const stamps = [...new Set(payload.series.flatMap(s => s.samples.map(x => x.timestamp)))].sort();
    const index = new Map(stamps.map((t, i) => [t, i]));
    const buckets = stamps.map(() => []);
    for (const series of payload.series) {
      for (const sample of series.samples) {
        const v = validValue(sample, scale);
        if (v !== null) buckets[index.get(sample.timestamp)].push(v);
      }
    }
    const pick = fn => buckets.map(b => (b.length ? fn(b) : null));
    return {
      stamps,
      mean: pick(b => b.reduce((a, c) => a + c, 0) / b.length),
      max: pick(b => Math.max(...b)),
      min: pick(b => Math.min(...b)),
      p95: pick(b => percentile([...b].sort((x, y) => x - y), 0.95)),
      counts: buckets.map(b => b.length)
    };
  }

  /** Serie → arreglo alineado con `stamps` (null si falta o no es válido). */
  function alignedValues(series, stamps, scale = 1) {
    const map = new Map(series.samples.map(s => [s.timestamp, s]));
    return stamps.map(t => validValue(map.get(t), scale));
  }

  function latest(series, scale = 1) {
    return validValue(series.samples[series.samples.length - 1], scale);
  }

  /** Series ordenadas por último valor. mode: 'top' (más cargados) | 'bottom' (menos cargados). */
  function rankNodes(payload, mode, n = 5, scale = 1) {
    const rows = payload.series
      .map(s => ({ series: s, value: latest(s, scale) }))
      .filter(r => r.value !== null);
    rows.sort((a, b) => (mode === 'bottom' ? a.value - b.value : b.value - a.value) || nodeId(a.series).localeCompare(nodeId(b.series)));
    return rows.slice(0, n).map(r => r.series);
  }

  /** Resumen del estado actual del conjunto. */
  function summarize(payload, scale = 1, threshold = null) {
    const vals = payload.series.map(s => ({ id: nodeId(s), v: latest(s, scale) })).filter(r => r.v !== null);
    if (!vals.length) return { count: payload.series.length, valid: 0, mean: null, max: null, min: null, above: 0 };
    const sum = vals.reduce((a, r) => a + r.v, 0);
    const max = vals.reduce((a, r) => (r.v > a.v ? r : a));
    const min = vals.reduce((a, r) => (r.v < a.v ? r : a));
    return {
      count: payload.series.length, valid: vals.length, mean: sum / vals.length,
      max: { id: max.id, value: max.v }, min: { id: min.id, value: min.v },
      above: threshold === null ? 0 : vals.filter(r => r.v > threshold).length
    };
  }

  /** Búsqueda + orden + paginación de filas de la tabla. */
  function pageRows(rows, { query = '', sortKey = 'node', dir = 'asc', page = 1, size = 10 } = {}) {
    const q = String(query).trim().toLowerCase();
    let list = q ? rows.filter(r => `${r.node} ${r.cluster} ${r.iface || ''}`.toLowerCase().includes(q)) : rows.slice();
    const sign = dir === 'desc' ? -1 : 1;
    list.sort((a, b) => {
      const x = a[sortKey], y = b[sortKey];
      if (ok(x) || ok(y)) {
        if (!ok(x)) return 1;          // sin dato siempre al final
        if (!ok(y)) return -1;
        return (x - y) * sign || String(a.node).localeCompare(String(b.node));
      }
      return String(x).localeCompare(String(y), 'es', { numeric: true }) * sign;
    });
    const total = list.length;
    const pages = Math.max(1, Math.ceil(total / size));
    const current = Math.min(Math.max(1, page), pages);
    const start = (current - 1) * size;
    return { rows: list.slice(start, start + size), total, pages, page: current,
      from: total ? start + 1 : 0, to: Math.min(start + size, total) };
  }

  return { percentile, historyStats, alignedValues, latest, rankNodes, summarize, pageRows };
});
