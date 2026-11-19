const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const a11y = require('../a11y.js');
const decisions = require('../decisions.js');
const pmv2 = require('../pmv2.js');
const read = f => fs.readFileSync(path.join(__dirname, '..', f), 'utf8');

const ID = '3f2b8c1e-5a4d-4e0f-9b1a-0c2d3e4f5a6b';
const REC = { recommendationId: ID, executionAllowed: false, status: 'eligible_for_review' };

// ---- U-02 tabla accesible ----
test('chartTableModel: mismas filas y columnas que los datasets del canvas', () => {
  const labels = ['10:00', '10:01', '10:02'];
  const datasets = [{ label: 'Media del conjunto', data: [10, null, 12.345] }, { label: 'HW001', data: [1, 2, 3] }];
  const m = a11y.chartTableModel({ caption: 'Evolución', labels, datasets, unit: '%', rowHeader: 'Hora' });
  assert.equal(m.caption, 'Evolución (unidad: %)');
  assert.deepEqual(m.columns.map(c => c.header), ['Hora', 'Media del conjunto', 'HW001']);
  assert.ok(m.columns.every(c => c.scope === 'col'));
  assert.equal(m.columns[1].unit, '%');
  assert.deepEqual(m.rows, [['10:00', '10.0', '1.0'], ['10:01', '—', '2.0'], ['10:02', '12.3', '3.0']]);
});

test('chartAriaLabel: describe series, unidad y no cuenta series ocultas en el nombre', () => {
  const t = a11y.chartAriaLabel({ title: 'evolución de la métrica', unit: '%', labels: ['a', 'b'],
    datasets: [{ label: 'Mínimo', data: [], hideLegend: true }, { label: 'Media', data: [] }] });
  assert.match(t, /en %/);
  assert.match(t, /2 series \(Media\), 2 instantes/);
  assert.match(t, /Ver datos en tabla/);
});

test('buildTable: caption, th con scope y celdas de datos', () => {
  const mk = tag => ({ tag, children: [], append(...c) { this.children.push(...c); }, set textContent(v) { this.text = v; } });
  const doc = { createElement: mk };
  const model = a11y.chartTableModel({ caption: 'C', labels: ['x'], datasets: [{ label: 'S', data: [5] }], unit: 'ms' });
  const table = a11y.buildTable(doc, model);
  const [cap, head, body] = table.children;
  assert.equal(cap.tag, 'caption');
  assert.equal(head.children[0].children[1].scope, 'col');
  assert.equal(head.children[0].children[1].text, 'S (ms)');
  const row = body.children[0].children;
  assert.equal(row[0].tag, 'th'); assert.equal(row[0].scope, 'row');
  assert.equal(row[1].tag, 'td'); assert.equal(row[1].text, '5.0');
});

test('dashboard: canvas con role=img y aria-label, y <details> «Ver datos en tabla»', () => {
  const html = read('dashboard.html');
  assert.match(html, /<canvas id="history-chart" role="img" aria-label="[^"]+"/);
  assert.match(html, /<summary>Ver datos en tabla<\/summary>/);
  assert.match(html, /src="a11y\.js"/);
  assert.match(html, /src="decisions\.js"/);
  assert.match(read('monitoring.js'), /GreenA11y\.attach/);
});

// ---- HU-13 PDF ----
test('buildReportUrl con format=pdf usa la misma ruta del gateway', () => {
  const url = pmv2.buildReportUrl('http://gw:8081/', { hardwareId: 'HW045', start: '2026-07-10T00:00:00Z', end: '2026-07-11T23:59:59Z', format: 'pdf' });
  assert.ok(url.startsWith('http://gw:8081/api/processing/v1/reports/historical-summary?'));
  assert.equal(new URL(url).searchParams.get('format'), 'pdf');
  assert.equal(new URL(url).searchParams.get('hardwareId'), 'HW045');
});

test('reportFileName y downloadReport: mismo patrón y errores que el CSV', async () => {
  assert.equal(pmv2.reportFileName({ hardwareId: 'HW045', start: 'a', end: 'b' }, 'pdf'), 'reporte_historico_HW045_a_b.pdf');
  global.authenticatedFetch = async url => { global.lastUrl = url; return { ok: false, status: 403, json: async () => ({}) }; };
  await assert.rejects(() => pmv2.downloadReportPdf('http://gw', { hardwareId: 'HW045' }), e => e.status === 403 && /solo permite lectura/.test(e.message));
  assert.match(global.lastUrl, /format=pdf/);
  await assert.rejects(() => pmv2.downloadReport('http://gw', {}, 'exe'), /no soportado/);
  delete global.authenticatedFetch;
});

test('dashboard: botón Descargar PDF junto al CSV', () => {
  const html = read('dashboard.html');
  assert.match(html, /id="report-csv-btn"[^>]*>Descargar CSV<\/button>\s*<button id="report-pdf-btn"[^>]*>Descargar PDF/);
});

// ---- HU-07 decisiones ----
test('decisionsPath exige UUID y apunta a la ruta del gateway', () => {
  assert.equal(decisions.decisionsPath(ID), `/api/recommendations/v1/recommendations/${ID}/decisions`);
  assert.throws(() => decisions.decisionsPath('../x'));
});

test('buildPayload: decision, comentario recortado y recomendación completa', () => {
  const p = decisions.buildPayload('APPROVED', '  ok  ', REC);
  assert.deepEqual(p, { decision: 'APPROVED', comment: 'ok', recommendation: REC });
  assert.equal(p.recommendation, REC);
  assert.equal('comment' in decisions.buildPayload('REJECTED', '   ', REC), false);
  assert.throws(() => decisions.buildPayload('MAYBE', '', REC));
  assert.throws(() => decisions.buildPayload('APPROVED', '', { ...REC, executionAllowed: true }));
});

test('validateComment: máximo 500 caracteres', () => {
  assert.equal(decisions.validateComment('a'.repeat(500)).ok, true);
  const bad = decisions.validateComment('a'.repeat(501));
  assert.equal(bad.ok, false); assert.match(bad.error, /500/);
  assert.throws(() => decisions.buildPayload('APPROVED', 'a'.repeat(501), REC), /500/);
});

test('canDecide oculta los botones a VIEWER y roles desconocidos', () => {
  assert.equal(decisions.canDecide('ADMIN'), true);
  assert.equal(decisions.canDecide('operator'), true);
  for (const r of ['VIEWER', 'PENDING', '', null, undefined]) assert.equal(decisions.canDecide(r), false);
});

test('friendlyError: 401/403/409/422 con mensaje amigable y sin códigos', () => {
  for (const s of [401, 403, 409, 422]) assert.ok(decisions.friendlyError(s, ''));
  assert.match(decisions.friendlyError(409), /Ya registraste/);
  assert.match(decisions.friendlyError(422, 'executionAllowed debe ser false'), /executionAllowed/);
  assert.equal(decisions.friendlyError(500), null);
});

test('isCurrent: una recomendación anterior deja de poder decidirse', () => {
  assert.equal(decisions.isCurrent(REC, REC), true);
  assert.equal(decisions.isCurrent(null, REC), false);
  assert.equal(decisions.isCurrent({ recommendationId: 'otra' }, REC), false);
});

test('lista de decisiones, aviso fijo y botones en el HTML', () => {
  assert.deepEqual(decisions.normalizeList({ decisions: [{ decisionId: '1' }] }), [{ decisionId: '1' }]);
  assert.deepEqual(decisions.normalizeList(null), []);
  assert.match(decisions.describe({ decision: 'REJECTED', decidedBy: 'u1', decidedByRole: 'OPERATOR', decidedAt: 't', comment: 'no' }), /Rechazada · u1 \(OPERATOR\) · t · «no»/);
  assert.equal(decisions.FIXED_NOTICE, 'Registrar una decisión no ejecuta ningún cambio');
  const html = read('dashboard.html');
  assert.ok(html.includes(decisions.FIXED_NOTICE));
  assert.match(html, /id="decision-approve"[^>]*>Aprobar/);
  assert.match(html, /id="decision-reject"[^>]*>Rechazar/);
  assert.match(html, /id="decision-comment" maxlength="500"/);
});

// ---- F-06 etiquetas modeladas ----
test('F-06: la UI etiqueta energía, potencia y CO2e como modelada/estimada', () => {
  const dash = read('dashboard.html');
  assert.match(dash, /Energía y CO₂e \(modeladas\)/);
  assert.match(dash, /Energía y CO₂e modeladas del periodo/);
  assert.match(read('network.html'), /Potencia máx\. \(modelada\)/);
  const ui = read('dashboard-ui.js');
  assert.match(ui, /card\('Energía \(modelada\)'/);
  assert.match(ui, /card\('CO₂e \(estimado\)'/);
  assert.match(read('recommendations.js'), /kWh \(modelada\)/);
});
