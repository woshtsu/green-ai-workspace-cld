const { test } = require('node:test');
const assert = require('node:assert/strict');
const A = require('../aggregate.js');
const E = require('../friendly-errors.js');

const mk = (id, vals, quality = 'valid') => ({
  resource: { type: 'node', cluster: 'c', id }, labels: {}, origin: 'simulated',
  samples: vals.map((v, i) => ({ timestamp: `2026-11-07T00:00:0${i}Z`, value: v, quality: v === null ? 'missing' : quality }))
});

test('historyStats: media, máx, mín y p95 por instante, ignorando muestras no válidas', () => {
  const payload = { series: [mk('A', [0.2, 0.4]), mk('B', [0.6, null]), mk('C', [1.0, 0.8])] };
  const s = A.historyStats(payload, 100);
  assert.equal(s.stamps.length, 2);
  assert.ok(Math.abs(s.mean[0] - 60) < 1e-9);
  assert.equal(s.max[0], 100);
  assert.equal(s.min[0], 20);
  assert.equal(s.counts[1], 2);              // B no aporta en el instante 2
  assert.ok(Math.abs(s.mean[1] - 60) < 1e-9);
});

test('historyStats: instante sin datos válidos devuelve null (no inventa ceros)', () => {
  const s = A.historyStats({ series: [mk('A', [null])] }, 1);
  assert.equal(s.mean[0], null);
  assert.equal(s.max[0], null);
});

test('rankNodes: top y bottom por último valor, determinista y sin series sin dato', () => {
  const payload = { series: [mk('A', [0.5]), mk('B', [0.9]), mk('C', [0.1]), mk('D', [null])] };
  assert.deepEqual(A.rankNodes(payload, 'top', 2).map(s => s.resource.id), ['B', 'A']);
  assert.deepEqual(A.rankNodes(payload, 'bottom', 2).map(s => s.resource.id), ['C', 'A']);
  assert.equal(A.rankNodes(payload, 'top', 10).length, 3);
});

test('summarize: media, extremos y nodos sobre el umbral', () => {
  const payload = { series: [mk('A', [0.5]), mk('B', [0.9]), mk('C', [0.1])] };
  const r = A.summarize(payload, 100, 80);
  assert.equal(r.max.id, 'B');
  assert.equal(r.min.id, 'C');
  assert.equal(r.above, 1);
  assert.ok(Math.abs(r.mean - 50) < 1e-9);
  assert.equal(A.summarize({ series: [] }, 1).mean, null);
});

test('pageRows: pagina de 10, busca, ordena con sin-dato al final y limita la página', () => {
  const rows = Array.from({ length: 50 }, (_, i) => ({ node: `HW${String(i + 1).padStart(3, '0')}`, cluster: 'c', iface: '', value: i === 3 ? null : i }));
  const p1 = A.pageRows(rows, { size: 10 });
  assert.equal(p1.rows.length, 10);
  assert.equal(p1.total, 50);
  assert.equal(p1.pages, 5);
  assert.equal(`${p1.from}-${p1.to}`, '1-10');
  const found = A.pageRows(rows, { query: 'hw05' });
  assert.deepEqual(found.rows.map(r => r.node), ['HW050']);
  const desc = A.pageRows(rows, { sortKey: 'value', dir: 'desc', size: 3 });
  assert.deepEqual(desc.rows.map(r => r.value), [49, 48, 47]);
  const asc = A.pageRows(rows, { sortKey: 'value', dir: 'asc', size: 50 });
  assert.equal(asc.rows.at(-1).value, null);
  assert.equal(A.pageRows(rows, { page: 99, size: 10 }).page, 5);
});

test('errores amigables: espera, sesión, permisos, servicio y sin códigos en el texto principal', () => {
  const wait = E.classify({ status: 422, context: 'prediccion', body: { code: 'INSUFFICIENT_DATA' }, reference: 'abc-123' });
  assert.equal(wait.tipo, 'espera');
  assert.ok(!/422|HTTP|abc-123/.test(`${wait.titulo} ${wait.mensaje}`));
  assert.ok(/422/.test(wait.detalleTecnico) && /abc-123/.test(wait.detalleTecnico));
  assert.equal(E.classify({ status: 401, context: 'prediccion' }).tipo, 'sesion');
  assert.equal(E.classify({ status: 403 }).tipo, 'permisos');
  assert.equal(E.classify({ status: 504 }).tipo, 'servicio');
  assert.equal(E.classify({ status: null, networkError: true }).tipo, 'servicio');
  const rec = E.classify({ status: 422, context: 'recomendacion', body: { detail: 'memoryPercent debe ser ≤ 100' } });
  assert.equal(rec.tipo, 'datos');
  assert.match(rec.mensaje, /memoryPercent/);
  assert.equal(E.classify({ status: 422, context: 'recomendacion', body: { detail: { foo: 1 } } }).tipo, 'espera');
  assert.equal(E.fromException(Object.assign(new Error('x'), { name: 'TimeoutError' }), 'prediccion').tipo, 'servicio');
  const err = E.toError({ status: 403 });
  assert.ok(err.friendly && !/HTTP/.test(err.message));
});
