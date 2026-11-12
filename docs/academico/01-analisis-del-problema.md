# C1 · Análisis del problema (AG-T08 / AG-C08)

Base: `docs/historico/trabajos-desarrollados/1. Analisis del Problema.md` (sólido y prudente; se conserva su enfoque) y
la guía `guias/exportados_docente/1.Análisis del problema.md`.
**Correcciones respecto al trabajo previo:**
- Se añaden el **diagrama de Ishikawa** (6M) y los **ODS**, que exige `informeFinal.md`.
- Se reducen los problemas y objetivos específicos a **3, alineados a los PMV**.
- Se agrega un **análisis cuantitativo con datos verificables** (dataset sintético, declarado como tal).
- Se completa la referencia [4], que no tenía autores.

## 1. Contexto
Universidad Continental (Huancayo, Junín; educación superior). Servicios académicos y administrativos (Aula
Virtual, sistemas institucionales, laboratorios) sobre infraestructura de servidores y nube. Unidad de análisis:
los **workloads** y los recursos que consumen (CPU, memoria, almacenamiento y red). Actores directos: Dirección
de TI, responsables de laboratorio y administradores de infraestructura. Indirectos: estudiantes, docentes,
investigadores y personal administrativo.

## 2. Situación problemática (evidencia, sin proponer todavía la solución)
- **Institucional (pública, 2020):** el Aula Virtual pasó de unos 1 000 estudiantes simultáneos (hasta 10 000
  peticiones) a unos 8 000 en promedio (hasta 36 500 peticiones). La UC amplió hasta 4 veces la capacidad de
  servidor en AWS, triplicó el almacenamiento y contrató monitoreo 24/7. Muestra que la demanda varía y que la
  capacidad se adapta de forma reactiva; **no** prueba ineficiencia actual.
- **Global:** la IEA estima 415 TWh de consumo de los centros de datos en 2024 (~1,5 % del consumo eléctrico
  mundial) y ~945 TWh en 2030 [8]. Es contexto, no dato de la UC.
- **Literatura:** las cargas son temporales, no lineales y multirrecurso [1]–[3]. Decidir solo con el estado
  instantáneo de la CPU es insuficiente [3].
- **Vacío de información:** no se dispone de métricas institucionales de CPU, RAM ni energía. El acta con la
  Dirección de TI y el formulario de workloads (`TrabajosDesarrollados/Acta_…`, `Formulario_…`) son
  **instrumentos preparados**. Confirmar si se aplicaron y con qué respuestas; si no, declararlo.

## 3. Caracterización (AS-IS → TO-BE)
SIPOC: proveedores (áreas, usuarios, aplicaciones) → entradas (solicitudes, workloads, capacidad, métricas,
políticas, SLA) → proceso (demanda → monitoreo → evaluación → asignación/ajuste → ejecución → supervisión) →
salidas (servicio, recursos asignados, métricas, registros) → clientes (TI, estudiantes, docentes).
Punto crítico: **entre el monitoreo y la decisión de ajuste**, donde hoy la decisión es reactiva (supuesto por
validar). TO-BE: métricas → histórico → predicción → evaluación de restricciones (SLA/latencia) →
**recomendación** → revisión humana → ajuste autorizado → registro (modo *Recommendation-Only*).

## 4. Causas: Ishikawa (6M) sobre el efecto «adaptación reactiva o ineficiente de recursos a la demanda»
| Categoría | Causas (código del árbol del trabajo previo) |
|---|---|
| Método | Asignación basada en estado actual, reglas o umbrales fijos (CR1); decisiones sin pronóstico (CD2) |
| Medición | Sin medición energética directa por servidor (C6); histórico disperso o no integrado (CI4, CR2) |
| Máquina (infraestructura) | Capacidad provisionada que no sigue a la demanda (CD1); múltiples recursos que interactúan (CD3) |
| Mano de obra | Ajustes manuales y reactivos; el monitoreo 24/7 detecta pero no anticipa |
| Materiales (datos) | Series multivariables y no estacionarias (CI1, CI2); datos institucionales no disponibles |
| Medio (entorno) | Picos académicos (matrícula, exámenes, laboratorios); restricciones de SLA y seguridad que impiden mover cargas (CI3) |
Los 5 porqués del trabajo previo llegan a la causa raíz: **limitada integración de histórico y predicción en
la decisión de asignación** (CR2), manteniendo las restricciones de servicio.

## 5. Efectos
Usuarios: latencia, errores, menor disponibilidad en picos. Organización: capacidad ociosa o saturación, más
intervención manual. Ambiente: posible consumo superior al necesario, **solo afirmable con medición válida**.

## 6. Formulación (alineada a los 3 PMV)
- **Problema general:** ¿cómo apoyar decisiones anticipadas de asignación de recursos en una infraestructura
  universitaria frente a la variabilidad de la demanda, sin degradar el servicio y evaluando su efecto
  energético?
- **PE1 (PMV1):** ¿cómo observar y caracterizar, de forma continua y reproducible, la utilización
  multirrecurso de los workloads?
- **PE2 (PMV2):** ¿con qué error pueden modelos de ML anticipar la demanda de CPU frente a referencias simples
  (persistencia y media móvil) y convertirla en recomendaciones explicables y seguras?
- **PE3 (PMV3):** ¿en qué medida la estrategia predictiva modifica la utilización, el cumplimiento de SLA y la
  energía estimada frente a una línea base, en condiciones experimentales equivalentes?

## 7. Análisis cuantitativo
**A. Dataset sintético del proyecto** (`software/data-processing/datasets/raw/synthetic_greenai/BD_GreenAi.xlsx`,
100 000 registros de 50 servidores, 10/07/2026–17/09/2026; generado por script, **no son mediciones de la UC**).
Cifras calculadas el 2026-11-06 sobre la base SQLite del proyecto:
| Indicador | Valor |
|---|---|
| CPU media / mediana / p95 | 50,1 % / 50,1 % / 86,4 % (rango 5–99 %) |
| Tiempo con CPU < 30 % (baja utilización) | 24,6 % de los registros |
| Tiempo con CPU > 80 % (alta utilización) | 11,3 % de los registros |
| RAM media / p95 | 45,2 % / 81,7 % |
| Potencia media / p95 (columna `energia_watts`) | 318 W / 630 W (capacidad 450–800 W) |
| Registros con `cumple_sla = false` | 6,13 % |
Advertencia: `accion_recomendada = «Reducir Frecuencia»` aparece exactamente en el 11,3 % de los registros (los
de CPU > 80 %). La etiqueta la generó una regla del script y **no** debe usarse como verdad de terreno.

**B. Telemetría simulada en tiempo real** (`software/simulator`, 50 nodos del inventario): alimenta Prometheus y
el pipeline de predicción (`dataset-sim-001`, cadencia de 5 min).

**C. Indicadores a medir cuando haya datos institucionales:** CPU/RAM/red por nodo, p95/p99 de latencia,
throughput, % de violaciones de SLA, W/Wh por servidor, Wh por petición.

## 8. Objetivos (máx. 3, uno por PMV, con medida de éxito)
- **OG:** desarrollar y validar un prototipo que integre monitoreo, predicción de demanda computacional y
  recomendaciones explicables bajo supervisión humana.
- **OE1 (PMV1):** implementar la observabilidad de 50 nodos simulados con APIs y persistencia. *Mide:*
  métricas disponibles vía Gateway con autenticación, pruebas de contrato aprobadas.
- **OE2 (PMV2):** entrenar y comparar al menos 2 modelos de ML frente a 2 baselines y servir la predicción y la
  recomendación por API. *Mide:* MAE/RMSE/sMAPE del modelo frente al baseline en el mismo split temporal;
  latencia p95 de inferencia; recomendación con `executionAllowed=false`.
- **OE3 (PMV3):** comparar la estrategia predictiva frente a la línea base en escenarios equivalentes. *Mide:*
  utilización, SLA y energía **estimada** (o medida, si hay instrumentación), con su incertidumbre.

## 9. ODS
ODS 7 (energía asequible y no contaminante: eficiencia energética de TI), ODS 9 (industria, innovación e
infraestructura), ODS 12 (producción y consumo responsables) y ODS 13 (acción por el clima). El aporte a los
ODS 7 y 13 es potencial y depende de demostrar el ahorro con medición.

## 10. Restricciones
Datos institucionales no garantizados; sin medición energética directa; no tocar producción (solo
recomendaciones); seguridad (JWT, mínimo privilegio, secretos fuera del código); costo monetario cero; 16
semanas; equipo de 4.

## 11. Conclusión del análisis
La variabilidad temporal y multirrecurso de los workloads, junto con decisiones de capacidad reactivas,
justifica investigar si la predicción de corto plazo puede apoyar decisiones anticipadas. La evidencia actual
es contextual (UC 2020, IEA, literatura) y experimental con datos sintéticos o simulados. Por eso el proyecto
**no afirma ahorro energético** y lo deja como pregunta del PMV3 (PE3), condicionado a la medición.

## Referencias de este capítulo
Numeración del trabajo previo; formato completo y normalizado en `09-antecedentes-y-referencias.md`.
[4] completar autores: *Energy-aware systems for real-time job scheduling in cloud data centers: A deep
reinforcement learning approach*, Computers and Electrical Engineering, 2022, vol. 99, art. 107688,
DOI 10.1016/j.compeleceng.2022.107688. Verificar los autores en la fuente.
