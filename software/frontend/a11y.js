/* U-02: equivalente textual accesible de los gráficos Chart.js. Lógica pura (sin DOM) + render opcional. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.GreenA11y = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const isNum = v => typeof v === 'number' && Number.isFinite(v);

  /** Texto de una celda: número con 1 decimal, o «—» si no hay dato. */
  function cellText(value, decimals = 1) {
    return isNum(value) ? value.toFixed(decimals) : '—';
  }

  /** Modelo de tabla a partir de los MISMOS labels/datasets que recibe Chart.js.
   *  Devuelve {caption, columns:[{header, scope, unit}], rows:[[texto…]]} */
  function chartTableModel({ caption, labels = [], datasets = [], unit = '', rowHeader = 'Instante', decimals = 1 }) {
    const columns = [{ header: rowHeader, scope: 'col', unit: '' },
      ...datasets.map(d => ({ header: String(d.label), scope: 'col', unit }))];
    const rows = labels.map((label, i) => [String(label), ...datasets.map(d => cellText((d.data || [])[i], decimals))]);
    return { caption: unit ? `${caption} (unidad: ${unit})` : caption, columns, rows };
  }

  /** aria-label descriptivo del canvas. */
  function chartAriaLabel({ title, unit = '', labels = [], datasets = [] }) {
    const names = datasets.filter(d => !d.hideLegend).map(d => d.label).join(', ');
    const unitPart = unit ? ` en ${unit}` : '';
    return `Gráfico de líneas: ${title}${unitPart}. ${datasets.length} series${names ? ` (${names})` : ''}, ${labels.length} instantes. `
      + 'Los mismos datos están disponibles en la tabla «Ver datos en tabla».';
  }

  /** Construye <table> (scope en th, caption) con el documento dado. */
  function buildTable(doc, model) {
    const table = doc.createElement('table');
    table.className = 'data-table a11y-table';
    const cap = doc.createElement('caption'); cap.textContent = model.caption; table.append(cap);
    const head = doc.createElement('thead'); const hr = doc.createElement('tr');
    model.columns.forEach(c => {
      const th = doc.createElement('th'); th.scope = c.scope;
      th.textContent = c.unit ? `${c.header} (${c.unit})` : c.header; hr.append(th);
    });
    head.append(hr); table.append(head);
    const body = doc.createElement('tbody');
    model.rows.forEach(r => {
      const tr = doc.createElement('tr');
      r.forEach((text, i) => {
        const cell = doc.createElement(i === 0 ? 'th' : 'td');
        if (i === 0) cell.scope = 'row';
        cell.textContent = text; tr.append(cell);
      });
      body.append(tr);
    });
    table.append(body);
    return table;
  }

  /** Conecta canvas + <details> con tabla. Llamar cada vez que se redibuja el gráfico. */
  function attach(doc, canvas, details, tableHost, spec) {
    if (!canvas || !details || !tableHost) return;
    canvas.setAttribute('role', 'img');
    canvas.setAttribute('aria-label', chartAriaLabel(spec));
    const model = chartTableModel(spec);
    const render = () => tableHost.replaceChildren(buildTable(doc, model));
    details.hidden = false;
    details._render = render;
    if (details.open) render(); else tableHost.replaceChildren();
    if (!details._bound) { details._bound = true; details.addEventListener('toggle', () => { if (details.open && details._render) details._render(); }); }
  }

  function clear(canvas, details, tableHost) {
    if (canvas) { canvas.setAttribute('role', 'img'); canvas.setAttribute('aria-label', 'Gráfico sin datos disponibles.'); }
    if (details) { details.hidden = true; details._render = null; }
    if (tableHost) tableHost.replaceChildren();
  }

  return { cellText, chartTableModel, chartAriaLabel, buildTable, attach, clear };
});
