**Fase 1. Validación de la Rúbrica (Obligatoria)**

**Objetivo**

Determinar si el artículo cumple con los criterios mínimos de evaluación académica.

**Insumos**

* Artículo en inglés.
* Rúbrica de evaluación.

**Herramienta**

* Prompt de evaluación por rúbrica.

**Resultado esperado**

* Tabla de puntajes.
* Puntaje total.
* Criterios observados.
* Dictamen preliminar.

**Regla sugerida**

| **Resultado** | **Acción** |
| --- | --- |
| ≥ 85% | Pasa a Fase 2 |
| 70% - 84% | Correcciones menores |
| < 70% | Devolver para corrección |

**Fase 2. Revisión Científica y Lingüística del Artículo**

**Objetivo**

Evaluar la calidad real del paper más allá de la rúbrica.

**Insumos**

* Artículo en inglés.
* Informe del proyecto.

**Herramienta**

* Prompt de evaluación integral del artículo.

Aspectos críticos

Inglés académico

**Verificar:**

* Grammar
* Academic style
* Cohesion
* Coherence
* Native-like writing
* Technical vocabulary

Calidad científica

**Verificar:**

* Problema claramente definido.
* Objetivos.
* Metodología.
* Implementación.
* Resultados.
* Discusión.
* Conclusiones.

Cumplimiento CIIS

**Verificar presencia de:**

* Arquitectura Hexagonal.
* IA.
* Machine Learning.
* Reconocimiento de imágenes.
* Plataforma web.
* Plataforma móvil.
* Scrum-Kanban.
* PMV.

Resultado esperado

**Clasificación:**

* Excelente.
* Aceptable.
* Requiere correcciones.
* Crítico.

**Fase 3. Validación de Trazabilidad**

**Objetivo**

Confirmar que el artículo realmente se construyó a partir del informe.

**Insumos**

* Artículo en inglés.
* Informe en español.

**Herramienta**

* Prompt de trazabilidad artículo ↔ informe.

Aspectos a verificar

**Consistencia técnica**

* Problema.
* Objetivos.
* Arquitectura.
* Tecnologías.
* Metodología.

**Consistencia de resultados**

* Métricas.
* Tablas.
* Figuras.
* Conclusiones.

Detección de contenido inventado

**Buscar:**

* Resultados sin evidencia.
* Métricas inventadas.
* Arquitecturas no implementadas.
* Herramientas no mencionadas en el informe.

Resultado esperado

Porcentaje de trazabilidad.

**Escala sugerida**

| **Trazabilidad** | **Estado** |
| --- | --- |
| 90% - 100% | Correcta |
| 75% - 89% | Aceptable |
| 60% - 74% | Observada |
| < 60% | Rechazada |

**Fase 4. Decisión Final**

Combinar los resultados de las tres evaluaciones.

Criterio de ponderación

Rúbrica

40%

Calidad científica y lingüística

35%

Trazabilidad

25%

Visto Bueno

APROBADO

**Condiciones:**

* Rúbrica ≥ 85%
* Calidad científica Aceptable o superior
* Trazabilidad ≥ 85%

APROBADO CON OBSERVACIONES

**Condiciones:**

* Rúbrica ≥ 75%
* Correcciones menores de inglés o formato
* Trazabilidad ≥ 75%

REQUIERE CORRECCIONES IMPORTANTES

**Condiciones:**

* Rúbrica entre 60% y 74%
* Problemas de redacción científica
* Resultados insuficientes
* Trazabilidad parcial

NO APROBADO

**Condiciones:**

* Rúbrica < 60%
* Inglés deficiente
* Resultados sin evidencia
* Contenido inventado
* Trazabilidad insuficiente

**Flujo recomendado para cada estudiante**

1. Recibir artículo e informe.
2. Ejecutar el **Prompt de Rúbrica**.
3. Si aprueba el mínimo, ejecutar el **Prompt de Evaluación Integral**.
4. Ejecutar el **Prompt de Trazabilidad**.
5. Consolidar observaciones.
6. Emitir:
   * Puntaje de rúbrica.
   * Calidad científica.
   * Porcentaje de trazabilidad.
   * Dictamen final.
   * Lista priorizada de correcciones.

Con este flujo tendrás una evaluación bastante cercana a la que realizaría un comité académico antes de autorizar el envío del artículo a una conferencia como CIIS.