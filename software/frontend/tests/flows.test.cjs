const { test } = require('node:test');
const assert = require('node:assert/strict');
const F = require('../flows-logic.js');

const mk = (cpus, rack = i => `Rack-0${(i % 5) + 1}`) => cpus.map((cpu, i) => ({ id: `HW${String(i + 1).padStart(3, '0')}`, rack: rack(i), cpu }));

test('carga equilibrada (todos iguales): sin flujos y mensaje explícito', () => {
  const r = F.computeTransfers(mk(Array(50).fill(85)));
  assert.equal(r.balanced, true);
  assert.deepEqual(r.flows, []);
  assert.match(r.criterion, /equilibrada/);
});

test('extremos: la carga sale de los más cargados hacia los de menor uso y se conserva', () => {
  const r = F.computeTransfers(mk([95, 90, 50, 45, 70, 70, 70, 70]), { k: 0.5, maxFlows: 10 });
  assert.ok(r.flows.length >= 1);
  assert.equal(r.flows[0].from, 'HW001');
  assert.ok(['HW003', 'HW004'].includes(r.flows[0].to));
  const out = {}, inn = {};
  for (const f of r.flows) { out[f.from] = (out[f.from] || 0) + f.amountPercent; inn[f.to] = (inn[f.to] || 0) + f.amountPercent; }
  const nodes = Object.fromEntries(mk([95, 90, 50, 45, 70, 70, 70, 70]).map(n => [n.id, n.cpu]));
  for (const [id, v] of Object.entries(out)) assert.ok(v <= nodes[id] - r.mean + 0.11, `${id} no excede su exceso`);
  for (const [id, v] of Object.entries(inn)) assert.ok(v <= r.mean - nodes[id] + 0.11, `${id} no excede su holgura`);
});

test('nodos sin dato se ignoran y con menos de 2 válidos no hay propuesta', () => {
  assert.deepEqual(F.computeTransfers(mk([null, null, 50])).flows, []);
  const r = F.computeTransfers(mk([95, null, 20, 60, 60]), { k: 0.3 });
  assert.ok(r.flows.every(f => f.from !== 'HW002' && f.to !== 'HW002'));
});

test('límite de flujos y determinismo', () => {
  const cpus = Array.from({ length: 50 }, (_, i) => 20 + (i * 37) % 70);
  const a = F.computeTransfers(mk(cpus), { k: 0.1, maxFlows: 7 });
  const b = F.computeTransfers(mk(cpus), { k: 0.1, maxFlows: 7 });
  assert.ok(a.flows.length <= 7);
  assert.deepEqual(a, b);
  assert.ok(F.computeTransfers(mk(cpus), { k: 0.1, maxFlows: 40 }).flows.length > a.flows.length);
});

test('layoutRadial: 50 posiciones únicas y 5 sectores; curvePath devuelve una cuadrática', () => {
  const nodes = mk(Array(50).fill(50), i => `Rack-0${Math.floor(i / 10) + 1}`);
  const { positions, racks } = F.layoutRadial(nodes);
  assert.equal(positions.size, 50);
  assert.equal(racks.length, 5);
  const keys = new Set([...positions.values()].map(p => `${p.x.toFixed(2)},${p.y.toFixed(2)}`));
  assert.equal(keys.size, 50);
  assert.match(F.curvePath({ x: 0, y: 0 }, { x: 100, y: 100 }), /^M0\.0,0\.0 Q[\d.-]+,[\d.-]+ 100\.0,100\.0$/);
});
