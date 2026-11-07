/* Lógica pura de la vista «Red de flujos»: propuesta ILUSTRATIVA de reubicación de carga y disposición radial.
   Se calcula en el navegador a partir de la CPU actual; el simulador no genera tráfico entre servidores. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.GreenFlows = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const ok = v => typeof v === 'number' && Number.isFinite(v);

  /** nodes: [{id, rack, cpu|null}] → { flows:[{from,to,amountPercent}], balanced, mean, std, sources, sinks, criterion } */
  function computeTransfers(nodes, opts = {}) {
    const k = ok(opts.k) ? opts.k : 0.5;
    const maxFlows = Number.isInteger(opts.maxFlows) ? opts.maxFlows : 20;
    const minAmount = ok(opts.minAmount) ? opts.minAmount : 0.3;
    const minStd = ok(opts.minStd) ? opts.minStd : 0.4;       // por debajo, se considera carga equilibrada
    const valid = (nodes || []).filter(n => n && n.id && ok(n.cpu));
    const empty = { flows: [], balanced: false, mean: null, std: null, sources: [], sinks: [], criterion: 'Sin datos suficientes.' };
    if (valid.length < 2) return empty;
    const mean = valid.reduce((a, n) => a + n.cpu, 0) / valid.length;
    const std = Math.sqrt(valid.reduce((a, n) => a + (n.cpu - mean) ** 2, 0) / valid.length);
    const criterion = `Origen: CPU > media + ${k.toFixed(1)}·σ; destino: CPU < media − ${k.toFixed(1)}·σ (media ${mean.toFixed(1)} %, σ ${std.toFixed(1)} pp).`;
    if (std < minStd) return { ...empty, balanced: true, mean, std, criterion: 'Carga equilibrada: no hay reubicaciones que proponer.' };

    const byId = (a, b) => a.id.localeCompare(b.id);
    const sources = valid.filter(n => n.cpu > mean + k * std).map(n => ({ id: n.id, rack: n.rack, left: n.cpu - mean })).sort((a, b) => b.left - a.left || byId(a, b));
    const sinks = valid.filter(n => n.cpu < mean - k * std).map(n => ({ id: n.id, rack: n.rack, left: mean - n.cpu })).sort((a, b) => b.left - a.left || byId(a, b));
    const srcInfo = sources.map(s => s.id), snkInfo = sinks.map(s => s.id);
    const flows = [];
    let i = 0, j = 0;
    while (i < sources.length && j < sinks.length && flows.length < maxFlows) {
      const amount = Math.min(sources[i].left, sinks[j].left);
      if (amount >= minAmount) flows.push({ from: sources[i].id, to: sinks[j].id, amountPercent: Math.round(amount * 10) / 10 });
      sources[i].left -= amount; sinks[j].left -= amount;
      if (sources[i].left < minAmount) i += 1;
      if (sinks[j].left < minAmount) j += 1;
    }
    return { flows, balanced: false, mean, std, sources: srcInfo, sinks: snkInfo, criterion };
  }

  /** Disposición radial: un sector de 360/racks grados por rack, dos anillos por sector. */
  function layoutRadial(nodes, { cx = 450, cy = 450, radius = 360 } = {}) {
    const racks = [...new Set(nodes.map(n => n.rack))].sort();
    const positions = new Map();
    const sector = 360 / Math.max(1, racks.length);
    racks.forEach((rack, ri) => {
      const members = nodes.filter(n => n.rack === rack).sort((a, b) => a.id.localeCompare(b.id));
      const center = -90 + ri * sector + sector / 2;
      const span = sector * 0.78;
      members.forEach((n, i) => {
        const perRing = Math.ceil(members.length / 2);
        const ring = i % 2;
        const slot = Math.floor(i / 2);
        const t = perRing > 1 ? slot / (perRing - 1) - 0.5 : 0;
        const angle = (center + t * span + (ring ? span / (perRing * 2) : 0)) * Math.PI / 180;
        const r = radius * (ring ? 0.74 : 0.97);
        positions.set(n.id, { x: cx + r * Math.cos(angle), y: cy + r * Math.sin(angle), angle, rack });
      });
    });
    return { positions, racks, sector };
  }

  /** Curva cuadrática que pasa cerca del centro (efecto «tela de araña»). */
  function curvePath(a, b, { cx = 450, cy = 450, pull = 0.55 } = {}) {
    const mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2;
    const qx = mx + (cx - mx) * pull, qy = my + (cy - my) * pull;
    return `M${a.x.toFixed(1)},${a.y.toFixed(1)} Q${qx.toFixed(1)},${qy.toFixed(1)} ${b.x.toFixed(1)},${b.y.toFixed(1)}`;
  }

  return { computeTransfers, layoutRadial, curvePath };
});
