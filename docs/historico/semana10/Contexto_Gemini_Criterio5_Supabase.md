# Contexto para Gemini — criterio 5 de Supabase

Preparado por Codex el 29 de octubre de 2026, a solicitud del usuario.
Objetivo: que Gemini continúe la verificación sin repetir toda la auditoría.
Este archivo es una guía de evaluación, no un certificado de cumplimiento ni una
autorización para modificar la base de datos.

## 1. Qué pide el docente

Fuentes proporcionadas por el usuario, en `C:/Users/Riss/Downloads/`:

- `S10.Evaluacion-formativa-Tablero-Github-Python.docx`: en la lista de código,
  «Que el código en base de datos cumpla requisitos de procedimientos almacenados».
  La consigna pide determinar hallazgos, acciones correctivas, recomendaciones y
  nivel de cumplimiento. El número 5 procede de la numeración usada en nuestra evaluación.
- `TallerProy1-ListaCotejo-Unidad-3-202610.docx`, indicador 11: demostración de
  arquitectura hexagonal, uso de procedimientos almacenados mediante código GitHub
  y tablero Kanban completo. Trello queda fuera del encargo de Codex.
- Esa rúbrica también pide demostración en video y evidencia de pruebas por HU.
  Su nombre indica Unidad 3, pero su encabezado dice Unidad I y Semana 12; no corregir
  ni reinterpretar esa discrepancia sin confirmar cuál versión aplica.
- `Consigna-Taller1-Actualizado-Icacit.docx (1).pdf`: la página 47 del original
  muestra el esquema Supabase. Ese esquema acredita diseño, no ejecución de rutinas.

No se identificó en esos enunciados una cantidad mínima de procedimientos ni una
operación concreta del negocio energético. No inventar esas condiciones. Tampoco
asumir que una función de autenticación cumple automáticamente lo que el docente
entiende por procedimiento almacenado.

## 2. Evidencia de código existente

Archivo revisado nuevamente para este handoff:
`green-ai-front-end/Frontend-GreenAi/supabase-auth-setup.sql`.
Rutas relativas a `C:/Practicas/202620/TallerProyectos/green-ai-workspace`.

| Objeto | Tipo declarado | Responsabilidad observada en el SQL |
| --- | --- | --- |
| `public.handle_new_auth_user()` | Función PL/pgSQL, `RETURNS trigger` | Inserta perfil en `user_profiles` y rol `OPERATOR` en `user_roles` para el nuevo usuario Auth. |
| `on_auth_user_created_green_ai` | Trigger `AFTER INSERT ON auth.users` | Invoca la función anterior al crear el usuario. No es una función ni un procedimiento por sí mismo. |
| `public.custom_access_token_hook(event jsonb)` | Función PL/pgSQL, `RETURNS jsonb` | Consulta `user_roles` e incorpora `user_role` a los claims devueltos. |

El script habilita RLS, define políticas y asigna permisos al rol
`supabase_auth_admin` para el hook. También contiene inserciones de regularización
para usuarios anteriores. Por eso, encontrar una fila ya existente en los perfiles
NO demuestra que el trigger la haya creado: pudo provenir de esa regularización.

La existencia del script local no prueba que esté instalado en Supabase, ni que el
hook esté activado en la configuración Auth, ni que GitHub contenga la misma versión.

### Precisión terminológica

Son funciones almacenadas y un trigger. La cláusula histórica
`EXECUTE PROCEDURE public.handle_new_auth_user()` de `CREATE TRIGGER` invoca una
función de trigger; no acredita un objeto `CREATE PROCEDURE`.
[Documentación oficial de PostgreSQL — CREATE TRIGGER](https://www.postgresql.org/docs/current/sql-createtrigger.html).

Si el docente acepta rutinas almacenadas implementadas como funciones/triggers,
documentar esa interpretación y demostrar su uso. Si exige literalmente un
procedimiento SQL, registrar la brecha; no crear uno vacío o sin uso solo para marcar
la casilla. Cualquier implementación adicional debe resolver una operación real y
preservar permisos y límites de responsabilidad.

## 3. Con quién se involucra Supabase

Flujo de alta y autorización que debe verificarse:

`Frontend → Supabase Auth → auth.users → trigger → user_profiles/user_roles`.

Al emitir un token, el Custom Access Token Hook configurado consulta el rol y
devuelve el claim `user_role`. El Frontend usa el token para llamar al Gateway,
que verifica JWT y roles. Esa validación no ejecuta SQL ni el trigger.

El acceso a históricos por Data Processing es otro flujo: lectura de tablas por
su adaptador Supabase. No afirmar que ese adaptador llama las funciones de Auth
solo porque ambos utilizan Supabase. Prediction no consulta Supabase ni requiere
un servicio separado de recomendaciones.

## 4. Verificación paso a paso

1. Revisar `HANDOFF.md` y `Revision_Arquitectura_Hexagonal.md`. Sus conclusiones son
   antecedentes: verificar archivos, capturas y versión antes de ratificar estados.
2. Registrar rama y commit del SQL que se entrega, proyecto/entorno de prueba y fecha.
   Comparar las definiciones desplegadas con ese SQL; no volver a ejecutar todo el
   script automáticamente, porque contiene cambios de políticas, trigger y datos.
3. Capturar las dos funciones instaladas y la definición/estado del trigger.
4. Con el usuario, registrar una cuenta de prueba desde la aplicación, después de
   instalar el trigger. No insertar directamente en `auth.users`. Conservar evento,
   fecha y un identificador consistente para vincular las evidencias.
5. Mostrar que ese mismo usuario tiene perfil y rol `OPERATOR` sin inserción manual.
   Una captura de un usuario antiguo no permite atribuir la creación al trigger.
6. Comprobar que el Custom Access Token Hook configurado corresponde a la función
   revisada. Obtener una sesión nueva tras su activación y comprobar el claim
   `user_role` de forma local; no subir tokens a decodificadores externos ni capturarlos completos.
7. Vincular esa sesión a una operación permitida por Gateway. Un login HTTP 200 de
   Supabase acredita autenticación, pero no por sí solo la ejecución del hook o del trigger.
8. Contrastar los permisos/RLS relevantes: mostrar que la aplicación no puede
   asignarse roles arbitrarios. Una consulta en SQL Editor con privilegios de
   administrador no demuestra el comportamiento de una sesión de usuario.
9. Documentar resultado esperado, obtenido, evidencia y límites. Si no se puede
   ejecutar un paso, marcarlo pendiente o no verificado, sin inventar resultados.

No borrar usuarios reales, modificar roles del equipo ni desactivar RLS para que
la demostración pase. Si el entorno requiere una nueva cuenta, coordinarla con el
usuario. Ocultar contraseñas, tokens, claves y datos personales ajenos a la prueba.

## 5. Consultas auxiliares de solo lectura

Propuestas para que el usuario/Gemini inspeccione el entorno autorizado.
NO fueron ejecutadas por Codex en esta sesión.

Definición y tipo de las rutinas:

```sql
select n.nspname as esquema,
       p.proname as rutina,
       p.prokind as tipo_catalogo,
       pg_get_function_identity_arguments(p.oid) as argumentos,
       pg_get_functiondef(p.oid) as definicion
from pg_proc p
join pg_namespace n on n.oid = p.pronamespace
where n.nspname = 'public'
  and p.proname in ('handle_new_auth_user', 'custom_access_token_hook')
  and p.prokind in ('f', 'p');
```

`f` identifica función y `p` procedimiento. Capturar la firma y definición real,
no solo el nombre mostrado por la interfaz.

Definición del trigger:

```sql
select t.tgname, t.tgenabled,
       pg_get_triggerdef(t.oid, true) as definicion
from pg_trigger t
join pg_class c on c.oid = t.tgrelid
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'auth' and c.relname = 'users'
  and t.tgname = 'on_auth_user_created_green_ai'
  and not t.tgisinternal;
```

Resultado del alta: sustituir el UUID nulo por el de la cuenta de prueba autorizada.
La consulta limita la evidencia a ese usuario y no lista toda la base:

```sql
select left(u.id::text, 8) as referencia_usuario,
       u.created_at as alta_auth,
       p.id is not null as perfil_creado,
       p.created_at as alta_perfil,
       r.role
from auth.users u
left join public.user_profiles p on p.id = u.id
left join public.user_roles r on r.user_id = u.id
where u.id = '00000000-0000-0000-0000-000000000000'::uuid;
```

No invocar directamente `handle_new_auth_user()` con SELECT: su contexto es el
trigger. Una llamada manual al hook permite comprobar su lógica, pero no demuestra
que Supabase Auth lo ejecute en un inicio de sesión real.

## 6. Evidencias y documento de salida

Nombres sugeridos, no archivos que se den por existentes:

- `evidencias/supabase_01_funciones.jpg`: definiciones desplegadas.
- `evidencias/supabase_02_trigger.jpg`: evento, tabla, función y estado del trigger.
- `evidencias/supabase_03_registro_prueba.jpg`: registro de cuenta de prueba, sin contraseña.
- `evidencias/supabase_04_resultado.jpg`: perfil y rol del mismo registro.
- `evidencias/supabase_05_hook.jpg`: configuración del hook.
- `evidencias/supabase_06_rol_y_gateway.jpg`: claim de rol anonimizado y resultado autorizado.

Entregar `output/semana10/Verificacion_Criterio5_Supabase.md` con:

| Campo | Contenido requerido |
| --- | --- |
| Requisito | Enunciado de S10 y relación con indicador 11. |
| Interpretación | Funciones/triggers aceptados o exigencia de procedimiento pendiente de aclarar. |
| Versión | Repo, rama, commit y fecha de prueba. |
| Prueba | Pasos realmente ejecutados y datos de prueba identificados. |
| Resultado | Esperado y obtenido, sin deducir ejecución de una mera definición. |
| Evidencia | Archivo, figura o video y qué demuestra específicamente. |
| Nivel | Suficiente, parcial o no verificado, con justificación. |
| Pendientes | Acción correctiva concreta para cada falta de evidencia. |

Se puede proponer suficiente cuando la interpretación del requisito esté resuelta,
las rutinas relevantes estén instaladas y se demuestre su uso y efecto desde el
flujo de la aplicación. La decisión académica final corresponde al docente.

## 7. Observaciones para la revisión global de Gemini

Codex leyó `Revision_Arquitectura_Hexagonal.md`, pero no inspeccionó en esta sesión
las capturas que allí se citan, el informe modificado, los artículos ni los remotos.
Por tanto, no ratifica todavía los estados «100 %» o «completo» del documento.
Antes de cerrar la evaluación, resolver estos puntos de trazabilidad:

- La revisión describe acoplamiento directo en Simulator y a la vez declara
  arquitectura completamente conforme. Delimitar alcance y justificar la conclusión
  o registrar la brecha; separación de una política no prueba todos los servicios.
- `executionAllowed=false` demuestra que no se ejecutan acciones automáticas;
  no demuestra por sí solo el flujo de aprobación/rechazo humano de HU-07. Evaluar
  HU-06, HU-07 y HU-08 por sus criterios individuales, sin aprobarlas en bloque por HTTP 200.
- Citar el archivo y versión del informe efectivamente corregido. «Datos reales
  del manifiesto» debe entenderse como valores leídos del archivo; el dataset sigue
  siendo simulado, no observaciones reales.
- Aportar título, autores, año y DOI/URL verificable de los tres estudios usados;
  comprobar que realmente apoyan la comparación. No basta una mención autor–año.
- Registrar commits remotos y enlaces verificados con fecha. El handoff de Codex
  anterior decía «sin push»; Gemini informa publicación posterior, que requiere
  actualizar el estado con evidencia en lugar de mezclar ambas fechas.

Este contexto permite continuar la verificación con Gemini; no requiere delegar
nuevas tareas a Codex ni repetir las pruebas ya documentadas sin una razón concreta.
