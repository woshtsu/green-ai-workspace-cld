const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const racks = require('../racks.js');
const racksData = JSON.parse(
  fs.readFileSync(path.join(__dirname, '..', 'racks.json'), 'utf8')
);

test('conversión ratio→%: convierte correctamente ratios 0–1 a 0–100 y maneja valores ausentes', () => {
  assert.equal(racks.ratioToPercent(0), 0);
  assert.equal(racks.ratioToPercent(0.39), 39);
  assert.equal(racks.ratioToPercent(0.4), 40);
  assert.equal(racks.ratioToPercent(0.63), 63);
  assert.equal(racks.ratioToPercent(0.8), 80);
  assert.equal(racks.ratioToPercent(0.81), 81);
  assert.equal(racks.ratioToPercent(1.0), 100);

  // Valores ausentes, nulos o no finitos
  assert.equal(racks.ratioToPercent(null), null);
  assert.equal(racks.ratioToPercent(undefined), null);
  assert.equal(racks.ratioToPercent(NaN), null);
  assert.equal(racks.ratioToPercent(Infinity), null);
});

test('umbrales de color (39, 40, 80, 81): respeta los rangos verde <40 %, ámbar 40–80 %, rojo >80 %', () => {
  // < 40 %: verde (#10b981)
  assert.equal(racks.getCpuCategory(39), 'green');
  assert.equal(racks.getCpuColor(39), '#10b981');
  assert.equal(racks.getCpuCategory(0), 'green');
  assert.equal(racks.getCpuColor(0), '#10b981');

  // 40–80 %: ámbar (#f59e0b)
  assert.equal(racks.getCpuCategory(40), 'amber');
  assert.equal(racks.getCpuColor(40), '#f59e0b');
  assert.equal(racks.getCpuCategory(63), 'amber');
  assert.equal(racks.getCpuColor(63), '#f59e0b');
  assert.equal(racks.getCpuCategory(80), 'amber');
  assert.equal(racks.getCpuColor(80), '#f59e0b');

  // > 80 %: rojo (#ef4444)
  assert.equal(racks.getCpuCategory(81), 'red');
  assert.equal(racks.getCpuColor(81), '#ef4444');
  assert.equal(racks.getCpuCategory(100), 'red');
  assert.equal(racks.getCpuColor(100), '#ef4444');
});

test('nodo sin dato muestra «sin dato» y categoría/color neutro', () => {
  assert.equal(racks.formatCpu(null), 'Sin dato');
  assert.equal(racks.formatCpu(undefined), 'Sin dato');
  assert.equal(racks.formatCpu(NaN), 'Sin dato');
  assert.match(racks.formatCpu(null), /sin dato/i);

  assert.equal(racks.getCpuCategory(null), 'nodata');
  assert.equal(racks.getCpuCategory(undefined), 'nodata');
  assert.equal(racks.getCpuColor(null), '#64748b');

  // aria-label accesible para nodo sin dato
  const labelSinDato = racks.buildAriaLabel({ id: 'HW001', rack: 'Rack-01', cpu: null });
  assert.equal(labelSinDato, 'HW001, Rack-01, CPU Sin dato');
  assert.match(labelSinDato, /sin dato/i);

  // aria-label accesible para nodo con dato
  const labelConDato = racks.buildAriaLabel({ id: 'HW001', rack: 'Rack-01', cpu: 63 });
  assert.equal(labelConDato, 'HW001, Rack-01, CPU 63 %');
});

test('agrupación de 50 nodos en 5 racks: verifica inventario completo y uniforme', () => {
  assert.equal(racksData.nodes.length, 50);

  const grouped = racks.groupByRack(racksData.nodes);
  const rackNames = Object.keys(grouped).sort();

  assert.deepEqual(rackNames, ['Rack-01', 'Rack-02', 'Rack-03', 'Rack-04', 'Rack-05']);
  assert.equal(rackNames.length, 5);

  let totalCount = 0;
  for (const rack of rackNames) {
    assert.equal(grouped[rack].length, 10, `El ${rack} debe contener exactamente 10 servidores`);
    totalCount += grouped[rack].length;
  }
  assert.equal(totalCount, 50, 'El total de nodos agrupados debe ser 50');

  // Comprobar primer y último servidor
  assert.equal(grouped['Rack-01'][0].id, 'HW001');
  assert.equal(grouped['Rack-05'][9].id, 'HW050');
});

test('resumen correcto: calcula nodos >80 %, CPU media y rack más cargado', () => {
  const sampleNodes = [
    { id: 'HW001', rack: 'Rack-01', cpu: 85 },  // > 80 %
    { id: 'HW002', rack: 'Rack-01', cpu: 35 },  // < 40 % -> Media Rack-01: 60 %
    { id: 'HW011', rack: 'Rack-02', cpu: 90 },  // > 80 %
    { id: 'HW012', rack: 'Rack-02', cpu: 82 },  // > 80 % -> Media Rack-02: 86 %
    { id: 'HW021', rack: 'Rack-03', cpu: null } // Sin dato
  ];

  const summary = racks.computeSummary(sampleNodes);

  // 1. Nodos > 80 % CPU (HW001: 85, HW011: 90, HW012: 82)
  assert.equal(summary.highCpuCount, 3);

  // 2. CPU media ignorando nodos sin dato: (85 + 35 + 90 + 82) / 4 = 73 %
  assert.equal(summary.avgCpu, 73);
  assert.equal(summary.validNodesCount, 4);
  assert.equal(summary.totalNodes, 5);

  // 3. Rack más cargado: Rack-02 con 86 % de media vs Rack-01 con 60 %
  assert.equal(summary.busiestRack, 'Rack-02');
  assert.equal(summary.busiestRackAvg, 86);
});

test('resumen con nodos sin datos o lista vacía falla de forma segura', () => {
  const emptySummary = racks.computeSummary([]);
  assert.equal(emptySummary.highCpuCount, 0);
  assert.equal(emptySummary.avgCpu, null);
  assert.equal(emptySummary.busiestRack, null);

  const allNoData = [
    { id: 'HW001', rack: 'Rack-01', cpu: null },
    { id: 'HW002', rack: 'Rack-01', cpu: null }
  ];
  const noDataSummary = racks.computeSummary(allNoData);
  assert.equal(noDataSummary.highCpuCount, 0);
  assert.equal(noDataSummary.avgCpu, null);
  assert.equal(noDataSummary.busiestRack, null);
});

test('parseMetricsResponse y enriquecimiento con inventario real de 50 nodos', () => {
  const mockPayload = {
    series: [
      { resource: { id: 'HW001', cluster: 'sim-1' }, samples: [{ value: 0.85, quality: 'valid' }] },
      { resource: { id: 'HW002', cluster: 'sim-1' }, samples: [{ value: 0.35, quality: 'valid' }] },
      { resource: { id: 'HW011', cluster: 'sim-1' }, samples: [{ value: 0.95, quality: 'valid' }] },
      { resource: { id: 'HW012', cluster: 'sim-1' }, samples: [{ value: 0.10, quality: 'invalid' }] }
    ]
  };

  const metricsMap = racks.parseMetricsResponse(mockPayload);
  assert.equal(metricsMap.get('HW001').cpu, 85);
  assert.equal(metricsMap.get('HW001').cluster, 'sim-1');
  assert.equal(metricsMap.get('HW012').cpu, null); // muestra inválida queda en null

  const grouped = racks.groupByRack(racksData.nodes, metricsMap);
  const allNodes = Object.values(grouped).flat();

  assert.equal(allNodes.length, 50);
  const summary = racks.computeSummary(allNodes);

  assert.equal(summary.highCpuCount, 2); // HW001 (85 %) y HW011 (95 %)
  assert.equal(summary.validNodesCount, 3); // HW001, HW002, HW011
  assert.equal(summary.totalNodes, 50);
});
