# C3 · El ingeniero y la sociedad (AG-I01 / AG-I02)

Base: `guias/TrabajosDesarrollados/3. El Ingeniero y la sociedad.md` y la guía `3.El Ingeniero y la Sociedad.md`.
**Correcciones al trabajo previo:**
1. Se retira el «ahorro del 15 %» (sin experimento).
2. Se retiran el apagado de servidores y Kubernetes, que no existen: el sistema **solo recomienda**.
3. Se corrige la afirmación de que no hay datos personales. La telemetría no los contiene, pero el **registro
   y la autenticación de usuarios sí** (correo, nombre y rol en Supabase Auth).
4. Se incorporan los riesgos reales detectados en la revisión técnica.

## 1. Contexto y partes interesadas
| Stakeholder | Interés | Impacto | Necesidad |
|---|---|---|---|
| Dirección de TI UC | Alto | Alto | Información anticipada sin riesgo para producción |
| Administradores de infraestructura | Alto | Alto | Recomendaciones explicables, control final humano |
| Estudiantes y docentes (usuarios indirectos) | Medio | Alto | Servicios disponibles en picos (matrícula, exámenes) |
| Directivos | Medio | Medio | Indicadores de eficiencia y sostenibilidad verificables |
| Docente asesor / ICACIT | Alto | Medio | Evidencia trazable |
| Equipo de proyecto (4) | Alto | Alto | Alcance viable en 16 semanas y a costo cero |

## 2. Impactos (con lo que realmente se puede afirmar hoy)
| Dimensión | Positivo (potencial) | Negativo / riesgo | Evidencia actual | Cómo medirlo |
|---|---|---|---|---|
| Social | Anticipar picos y reducir degradación del servicio | Recomendación errónea que reduzca capacidad en un pico | Solo recomendación (`executionAllowed=false`) | % de recomendaciones rechazadas por la política; violaciones de SLA en el experimento PMV3 |
| Económico | Menor capacidad ociosa; costo de desarrollo S/ 0 con software libre | Horas del equipo; tiempo de operación del modelo | Presupuesto (`04-` §6) | Costo por hora de operación; capacidad ociosa evitada |
| Ambiental | Reducción de energía si se demuestra | Costo energético del propio modelo (Green AI) | **Ninguna medición de energía real**; la energía se calcula solo con datos de potencia (E = ∫P dt) | Wh por workload frente a línea base (PMV3); overhead del modelo |
| Salud y seguridad | Alertas de disponibilidad | Exposición de servicios internos; credenciales | JWT, RBAC, puertos solo en loopback en desarrollo | Incidentes; pruebas 401/403 |
| Privacidad | Telemetría sin datos personales | Cuentas de usuario; **RLS permisiva y columna `password` en texto plano en el snapshot de Supabase** | `docs/HANDOFF.md` «Riesgos detectados» | Auditoría de políticas RLS; cero contraseñas en texto plano |
| Ética de IA | Explicabilidad: cada recomendación lleva los checks que la sustentan | Sesgo: el modelo entrenado con datos simulados puede subestimar picos reales | Error por régimen de carga en `model_comparison.csv` (picos: MAE 6,1 frente a 3,2 global) | Error en picos; tasa de recomendaciones con `insufficient_data` |

## 3. Marco legal (Perú) — matriz corregida
| Norma | Aplicación real | Requisito | Evidencia / acción |
|---|---|---|---|
| Ley 29733 y su reglamento (D.S. 016-2024-JUS) — protección de datos personales | Registro y autenticación de usuarios (correo, nombre, rol) | Finalidad, consentimiento, seguridad, mínimo privilegio | Supabase Auth; tabla `user_profiles` con RLS por usuario (`software/frontend/supabase-auth-setup.sql`). **Acción:** corregir la RLS «Permitir todo» y eliminar `password` en texto plano |
| D. Leg. 1412 (Gobierno Digital) | Interoperabilidad con servicios institucionales | Estándares abiertos | APIs REST y contratos OpenAPI |
| Ley 29973 (persona con discapacidad) / WCAG 2.1 | Interfaz web | Accesibilidad | **Pendiente:** auditoría WCAG del frontend |
| D. Leg. 822 (derecho de autor) | Uso de software libre | Licencias | Dependencias OSS (Apache-2.0, MIT, BSD) |
| Ley 30096 (delitos informáticos) / ISO/IEC 27001 (referencia) | Acceso a la API y a datos | Control de acceso, trazabilidad | JWT + RBAC, `X-Request-Id`, sin rutas comodín |
| ISO/IEC 21031:2024 (SCI) | Indicador de carbono del software | Unidad funcional, factor con fuente | `/v1/energy` exige la fuente del factor de emisión |
Verificar la vigencia de cada norma en el diario oficial antes de exportar.

## 4. Ética, inclusión y responsabilidad
- **Humano en el bucle:** ninguna recomendación se ejecuta sola; la política se abstiene si los datos son viejos
  o incompletos (`prediction_freshness`, `telemetry_identity_and_freshness`).
- **Transparencia:** cada respuesta declara su `origin` (simulated, estimated, unknown) y advertencias: «umbrales
  de demostración; no representan SLA aprobados».
- **Inclusión:** el beneficio es indirecto (estabilidad del servicio para estudiantes con conectividad limitada).
  No afirmarlo sin datos de uso.

## 5. KPIs de impacto (definidos, todavía no medidos)
% de violaciones de SLA frente a la línea base · Wh por workload · overhead energético del modelo · error en picos
· % de recomendaciones aprobadas o rechazadas · incidentes de seguridad · criterios WCAG cumplidos · SUS de
administradores.

## 6. Conclusión
La solución es socialmente responsable en su diseño: solo recomienda, es explicable y declara su incertidumbre.
Sus beneficios económicos y ambientales son **hipótesis** que el PMV3 debe medir. Hay riesgos de privacidad
concretos en la base de datos real que deben corregirse antes de afirmar cumplimiento de la Ley 29733.
