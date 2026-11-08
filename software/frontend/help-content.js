/* Textos de ayuda de los botones «?». Editables sin tocar la lógica.
   Cada entrada: title, what (qué es), use (para qué sirve), how (cómo se mide/calcula), input (qué escribir), limits (límites). */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.GreenHelp = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const SIM = 'Todos los datos de esta demostración son simulados.';
  return {
    summary: {
      title: 'Resumen del clúster',
      what: 'Cuatro cifras rápidas del estado actual de los servidores que estás mirando.',
      use: 'Detectar de un vistazo si el conjunto está tranquilo o saturado.',
      how: 'Se calculan en tu navegador con la última muestra válida de cada servidor (media, mayor y menor valor, y cuántos superan el 80 %).',
      limits: `${SIM} Las cifras se derivan de las series que devuelve Monitoring; no son métricas medidas aparte.`
    },
    'metrics-chart': {
      title: 'Evolución de la métrica',
      what: 'Cómo cambió la métrica elegida (CPU, memoria, red o disco) en el periodo seleccionado.',
      use: 'Ver tendencias y picos sin mirar los 50 servidores uno por uno.',
      how: 'La línea gruesa es la media de todos los servidores en cada instante; la franja sombreada va del mínimo al máximo. Puedes añadir hasta 5 servidores concretos para compararlos con esa franja.',
      input: 'Elige métrica, clúster y periodo arriba. Para comparar, añade servidores o usa «5 más cargados».',
      limits: `${SIM} Media, máximo y mínimo se calculan en pantalla; los huecos de datos se dejan vacíos, no se rellenan.`
    },
    'node-table': {
      title: 'Detalle por servidor',
      what: 'La última lectura de cada servidor, con su procedencia y calidad.',
      use: 'Localizar un servidor concreto o ver cuáles están más cargados.',
      how: 'Cada fila es la muestra más reciente. «Calidad: valid» significa que la lectura es utilizable.',
      input: 'Usa el buscador para filtrar por nombre (por ejemplo HW045) y pulsa un encabezado para ordenar.',
      limits: SIM
    },
    prediction: {
      title: 'Predicción de CPU',
      what: 'Una estimación de cuánta CPU usará un servidor dentro de 15 minutos.',
      use: 'Anticipar saturaciones antes de que ocurran.',
      how: 'Un modelo Random Forest recibe las últimas 2 horas de CPU de ese servidor y devuelve un porcentaje.',
      input: 'Elige un clúster y un servidor concretos arriba y pulsa el botón. Necesita unos 20 minutos de historial acumulado.',
      limits: 'Es experimental y se entrenó con datos sintéticos: no demuestra precisión ni ahorro energético. Si falta historial, solo hay que esperar.'
    },
    recommendation: {
      title: 'Recomendación con restricciones',
      what: 'Una propuesta de revisión de capacidad para un servidor, que respeta límites de memoria, latencia y errores.',
      use: 'Comprobar si sería razonable reducir o aumentar capacidad, siempre con una persona que decida.',
      how: 'Combina la CPU predicha con los valores que escribas y los compara con límites de demostración (CPU 30–80 %, memoria ≤ 85 %, latencia p95 ≤ 500 ms, errores ≤ 1 %).',
      input: 'Escribe la telemetría del servidor elegido. Si no tienes valores reales, usa los de ejemplo.',
      limits: 'Es una propuesta: no se ejecuta ningún cambio. Los límites son de demostración, no un SLA aprobado.'
    },
    'rec-memory': {
      title: 'Memoria (%)',
      what: 'Porcentaje de la memoria del servidor que está en uso.',
      how: 'Memoria usada ÷ memoria total × 100.',
      input: 'Un número entre 0 y 100. Ejemplo: 65. La política exige 85 o menos.',
      limits: 'Dato aportado por quien opera; no se verifica de forma independiente.'
    },
    'rec-latency': {
      title: 'Latencia p95 (ms)',
      what: 'El tiempo de respuesta que el 95 % de las peticiones no supera.',
      how: 'Se ordenan los tiempos de un periodo y se toma el valor del percentil 95.',
      input: 'Milisegundos, 0 o más. Ejemplo: 200. La política exige 500 o menos.',
      limits: 'Dato aportado por quien opera.'
    },
    'rec-errors': {
      title: 'Errores (%)',
      what: 'Porcentaje de peticiones que terminaron en error.',
      how: 'Peticiones con error ÷ peticiones totales × 100.',
      input: 'Un número entre 0 y 100. Ejemplo: 0,8. La política exige 1 o menos.',
      limits: 'Dato aportado por quien opera.'
    },
    'rec-time': {
      title: 'Instante de telemetría',
      what: 'El momento en que se tomaron los valores anteriores.',
      how: 'La recomendación solo considera vigentes datos de los últimos 5 minutos.',
      input: 'Pulsa «Usar ahora» para poner la hora actual.',
      limits: 'Si el instante es antiguo, la comprobación de vigencia queda sin evidencia.'
    },
    'rec-origin': {
      title: 'Procedencia declarada',
      what: 'Si los valores vienen de una medición real o de una simulación.',
      input: 'En esta demostración elige «Simulada».',
      limits: 'Se muestra en el resultado para que nadie confunda datos simulados con reales.'
    },
    report: {
      title: 'Reporte de históricos',
      what: 'Un resumen del historial de un servidor entre dos fechas, descargable en CSV.',
      use: 'Revisar el comportamiento pasado o llevar los datos a una hoja de cálculo.',
      how: 'Data Processing agrega los registros guardados del servidor en ese rango.',
      input: 'Código del servidor (por ejemplo HW045) y fechas desde/hasta. Las fechas se envían en UTC.',
      limits: 'Usa los registros históricos disponibles (datos sintéticos de la base de pruebas).'
    },
    experiment: {
      title: 'Baseline vs Green AI',
      what: 'Una comparación simulada entre una regla reactiva (baseline) y la política con predicción (Green AI).',
      use: 'Ver, con la misma carga, qué estrategia corre menos riesgo de incumplir el servicio y cuánta energía modelada usa.',
      how: 'Resultados de un experimento reproducible guardado en el proyecto (riesgo de SLA y energía modelada de cada estrategia).',
      limits: 'Simulación con energía modelada, no medida. No demuestra ahorro real: la diferencia puede ser mínima o nula.'
    },
    energy: {
      title: 'Energía y CO₂e del periodo',
      what: 'Cuánta energía (kWh) consumiría un servidor durante un periodo y cuánto CO₂e equivale.',
      use: 'Pasar de «CPU» a una cifra de energía comprensible.',
      how: 'Se integra la potencia en vatios a lo largo del tiempo (método del trapecio). El CO₂e = kWh × factor de emisión, pero solo se calcula si tú aportas el factor y su fuente.',
      input: 'Usa «Usar datos del simulador» (potencia modelada a partir de la CPU), carga el ejemplo o sube un JSON con "origin" y muestras {"timestamp","watts"}.',
      limits: 'Con datos simulados la potencia es MODELADA (P = P_idle + (P_max − P_idle) × CPU), no medida. No hay factor de emisión por defecto: debe salir de una fuente oficial del país y año.'
    },
    'energy-factor': {
      title: 'Factor de emisión',
      what: 'Los kilogramos de CO₂e que emite la red eléctrica por cada kWh consumido.',
      input: 'kg CO₂e/kWh y la fuente (por ejemplo, el informe oficial del operador eléctrico, con año). Ambos campos o ninguno.',
      limits: 'Sin factor, el CO₂e aparece como «no evaluable»; no inventamos uno.'
    },
    racks: {
      title: 'Racks con calor',
      what: 'Un mapa de los 50 servidores agrupados en 5 racks, coloreados por uso de CPU.',
      use: 'Encontrar zonas calientes de un vistazo.',
      how: 'Verde < 40 %, ámbar 40–80 %, rojo > 80 % con la CPU actual (se actualiza cada 30 s).',
      input: 'Haz clic en un servidor para ver su detalle y predecir su CPU.',
      limits: `${SIM} Con el escenario «high» casi todos quedan en rojo; es normal.`
    },
    flows: {
      title: 'Red de flujos',
      what: 'Un grafo de cómo podría repartirse la carga entre servidores: de los más cargados a los que tienen holgura.',
      use: 'Visualizar la idea de rebalanceo que propone Green AI.',
      how: 'Se calcula en tu navegador comparando la CPU de cada servidor con el promedio. Cada línea es una propuesta de mover carga; su grosor indica cuánta.',
      input: 'Ajusta la sensibilidad, el máximo de flujos y el rack. Pulsa un servidor para ver sus flujos.',
      limits: 'Es una propuesta ilustrativa sobre datos simulados. El simulador no genera tráfico real entre servidores y no se ejecuta ninguna acción.'
    }
  };
});
