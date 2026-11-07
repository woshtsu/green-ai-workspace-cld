const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const pmv2 = require('../pmv2.js');
const experimentData = JSON.parse(
  fs.readFileSync(path.join(__dirname, '..', 'experiment.json'), 'utf8')
);

// -------------------------------------------------------------
// 1. Mapeo de errores de API (Task 1a, 3b, 5)
// -------------------------------------------------------------
test('mapApiError: INSUFFICIENT_DATA muestra mensaje explicativo de ~20 min', () => {
  assert.equal(
    pmv2.mapApiError({ code: 'INSUFFICIENT_DATA' }),
    'Datos insuficientes: el simulador necesita ~20 min de historial'
  );
  assert.equal(
    pmv2.mapApiError({ detail: 'INSUFFICIENT_DATA' }),
    'Datos insuficientes: el simulador necesita ~20 min de historial'
  );
  assert.equal(
    pmv2.mapApiError({ message: 'INSUFFICIENT_DATA' }),
    'Datos insuficientes: el simulador necesita ~20 min de historial'
  );
  assert.equal(
    pmv2.mapApiError(new Error('Dataset falló: INSUFFICIENT_DATA')),
    'Datos insuficientes: el simulador necesita ~20 min de historial'
  );
  assert.equal(
    pmv2.mapApiError({ detail: { code: 'INSUFFICIENT_DATA' } }),
    'Datos insuficientes: el simulador necesita ~20 min de historial'
  );
});

test('mapApiError: INVALID_DATASET muestra mensaje explicativo de ~20 min', () => {
  assert.equal(
    pmv2.mapApiError({ code: 'INVALID_DATASET' }),
    'Datos insuficientes: el simulador necesita ~20 min de historial'
  );
  assert.equal(
    pmv2.mapApiError({ detail: 'INVALID_DATASET' }),
    'Datos insuficientes: el simulador necesita ~20 min de historial'
  );
  assert.equal(
    pmv2.mapApiError({ message: 'INVALID_DATASET' }),
    'Datos insuficientes: el simulador necesita ~20 min de historial'
  );
  assert.equal(
    pmv2.mapApiError(new Error('Dataset inválido: INVALID_DATASET')),
    'Datos insuficientes: el simulador necesita ~20 min de historial'
  );
});

test('mapApiError: error 403 muestra mensaje de rol solo lectura', () => {
  assert.equal(pmv2.mapApiError({}, 403), 'Tu rol solo permite lectura');
  assert.equal(pmv2.mapApiError({ status: 403 }), 'Tu rol solo permite lectura');
  assert.equal(pmv2.mapApiError({ statusCode: 403 }), 'Tu rol solo permite lectura');
  assert.equal(pmv2.mapApiError({ code: '403' }), 'Tu rol solo permite lectura');
  assert.equal(pmv2.mapApiError({ code: 403 }), 'Tu rol solo permite lectura');
  assert.equal(pmv2.mapApiError({ detail: 'Forbidden (HTTP 403)' }), 'Tu rol solo permite lectura');
  assert.equal(pmv2.mapApiError(new Error('Acceso denegado: 403')), 'Tu rol solo permite lectura');
  assert.equal(pmv2.mapApiError(new Error('Tu cuenta no tiene permiso')), 'Tu rol solo permite lectura');
});

test('mapApiError: otros errores muestran el mensaje breve', () => {
  assert.equal(
    pmv2.mapApiError({ detail: 'Hardware ID no encontrado' }),
    'Hardware ID no encontrado'
  );
  assert.equal(
    pmv2.mapApiError({ message: 'Fallo de conexión al gateway' }),
    'Fallo de conexión al gateway'
  );
  assert.equal(
    pmv2.mapApiError({ code: 'GATEWAY_TIMEOUT' }),
    'GATEWAY_TIMEOUT'
  );
  assert.equal(
    pmv2.mapApiError(new Error('Timeout de consulta')),
    'Timeout de consulta'
  );
  assert.equal(
    pmv2.mapApiError({ detail: [{ msg: 'Campo requerido: hardwareId' }] }),
    'Campo requerido: hardwareId'
  );
});

test('mapApiError: valores nulos o vacíos retornan mensaje por defecto', () => {
  assert.equal(pmv2.mapApiError(null), 'Error desconocido');
  assert.equal(pmv2.mapApiError(undefined), 'Error desconocido');
  assert.equal(pmv2.mapApiError({}), 'Error al procesar la solicitud');
});

// -------------------------------------------------------------
// 2. Formateo del experimento (Task 3c, 5)
// -------------------------------------------------------------
test('formatExperiment: formatea correctamente datos de experiment.json', () => {
  const result = pmv2.formatExperiment(experimentData);

  // Riesgo de SLA
  assert.equal(result.slaRiskBaseline, '3.97 %');
  assert.equal(result.slaRiskGreenAi, '3.97 %');
  assert.equal(result.slaDelta, '0.00 %');

  // Energía modelada
  assert.equal(result.energyBaseline, '5054.60 Wh');
  assert.equal(result.energyGreenAi, '5046.31 Wh');
  assert.equal(result.energyDelta, '-8.29 Wh');
  assert.equal(result.energyDeltaPct, '-0.16 %');

  // Etiqueta requerida
  assert.equal(result.disclaimer, 'Datos simulados · energía modelada, no medida');

  // Metadatos
  assert.equal(result.model, 'random_forest');
  assert.equal(result.horizon, '15m');
  assert.equal(result.intervals, 126);
});

test('formatExperiment: maneja datos nulos o vacíos sin lanzar excepciones', () => {
  const empty = pmv2.formatExperiment(null);
  assert.equal(empty.disclaimer, 'Datos simulados · energía modelada, no medida');
  assert.equal(empty.slaRiskBaseline, 'Sin dato');
  assert.equal(empty.energyBaseline, 'Sin dato');

  const partial = pmv2.formatExperiment({});
  assert.equal(partial.disclaimer, 'Datos simulados · energía modelada, no medida');
  assert.equal(partial.slaRiskBaseline, '—');
});

// -------------------------------------------------------------
// 3. Construcción de URL del reporte (Task 3b, 5)
// -------------------------------------------------------------
test('buildReportUrl: construye URL para formato JSON por defecto', () => {
  const url = pmv2.buildReportUrl('http://127.0.0.1:8081', {
    hardwareId: 'HW045',
    start: '2026-07-10',
    end: '2026-07-11'
  });

  assert.equal(
    url,
    'http://127.0.0.1:8081/api/processing/v1/reports/historical-summary?hardwareId=HW045&start=2026-07-10&end=2026-07-11&format=json'
  );
});

test('buildReportUrl: construye URL para formato CSV', () => {
  const url = pmv2.buildReportUrl('http://127.0.0.1:8081', {
    hardwareId: 'HW045',
    start: '2026-07-10',
    end: '2026-07-11',
    format: 'csv'
  });

  assert.equal(
    url,
    'http://127.0.0.1:8081/api/processing/v1/reports/historical-summary?hardwareId=HW045&start=2026-07-10&end=2026-07-11&format=csv'
  );
});

test('buildReportUrl: maneja alias desde y hasta y elimina barras finales de baseUrl', () => {
  const url = pmv2.buildReportUrl('http://127.0.0.1:8081///', {
    hardwareId: 'HW045',
    desde: '2026-07-10',
    hasta: '2026-07-11'
  });

  assert.equal(
    url,
    'http://127.0.0.1:8081/api/processing/v1/reports/historical-summary?hardwareId=HW045&start=2026-07-10&end=2026-07-11&format=json'
  );
});
