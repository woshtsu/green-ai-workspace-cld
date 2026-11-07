const { test } = require('node:test');
const assert = require('node:assert/strict');
const E = require('../energy.js');

const series = (id, values) => ({
  resource: { type: 'node', cluster: 'c', id }, labels: {}, origin: 'simulated',
  samples: values.map((v, i) => ({ timestamp: `2026-11-07T00:00:0${i}Z`, value: v, quality: v === null ? 'missing' : 'valid' }))
});

test('modelPower: lineal entre reposo (40 % de P_max) y P_max; inválidos → null', () => {
  assert.equal(E.modelPower(0, 500), 200);
  assert.equal(E.modelPower(1, 500), 500);
  assert.equal(E.modelPower(0.5, 500), 350);
  assert.equal(E.modelPower(1.7, 500), 500);       // recorta a 1
  assert.equal(E.modelPower(null, 500), null);
  assert.equal(E.modelPower(0.5, 0), null);
});

test('buildPowerSamples: suma nodos y descarta instantes incompletos', () => {
  const payload = { series: [series('A', [0, 1, null]), series('B', [1, 1, 1])] };
  const r = E.buildPowerSamples(payload, { A: 500, B: 1000 });
  assert.equal(r.nodes, 2);
  assert.equal(r.samples.length, 2);               // el tercer instante no tiene A
  assert.equal(r.skipped, 1);
  assert.equal(r.samples[0].watts, 200 + 1000);
  assert.equal(r.samples[1].watts, 500 + 1000);
  assert.deepEqual(E.buildPowerSamples({ series: [series('Z', [0.5])] }, {}).samples, []);
});

test('el cuerpo generado cumple el contrato y el ejemplo también', () => {
  const payload = { series: [series('A', [0.2, 0.4, 0.6])] };
  const body = { origin: 'simulated', samples: E.buildPowerSamples(payload, { A: 500 }).samples };
  assert.deepEqual(E.validateEnergyBody(body), []);
  assert.deepEqual(E.validateEnergyBody(E.exampleBody()), []);
});

test('validateEnergyBody: detecta origen, muestras, zona horaria y campos extra', () => {
  assert.ok(E.validateEnergyBody({ origin: 'x', samples: [] }).length >= 2);
  assert.ok(E.validateEnergyBody({ origin: 'simulated', samples: [{ timestamp: '2026-10-28T00:00:00', watts: 1 }, { timestamp: '2026-10-28T00:05:00Z', watts: 2 }] })
    .some(e => /zona/.test(e)));
  assert.ok(E.validateEnergyBody({ origin: 'simulated', extra: 1, samples: E.exampleBody().samples }).some(e => /no permitido/.test(e)));
  assert.ok(E.validateEnergyBody({ origin: 'simulated', samples: E.exampleBody().samples, emissionFactorKgPerKwh: 0.3 }).some(e => /juntos/.test(e)));
});

test('withFactor: ambos o ninguno, sin factor por defecto', () => {
  const base = E.exampleBody();
  assert.equal(E.withFactor(base, '', '').emissionFactorKgPerKwh, undefined);
  assert.throws(() => E.withFactor(base, '0.2', ''), /fuente/);
  assert.throws(() => E.withFactor(base, '500', 'x'), /entre 0 y 100/);
  const ok = E.withFactor(base, '0.25', ' Operador 2025 ');
  assert.equal(ok.emissionFactorKgPerKwh, 0.25);
  assert.equal(ok.emissionFactorSource, 'Operador 2025');
});

test('equivalentHours', () => {
  assert.equal(E.equivalentHours(0.45, 450), 1);
  assert.equal(E.equivalentHours(null), null);
});
