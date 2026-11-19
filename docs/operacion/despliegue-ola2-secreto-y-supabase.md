# Despliegue de la ola 2: GATEWAY_SHARED_SECRET y contraseña de `usuario` (solo Ricardo)

## 1. `GATEWAY_SHARED_SECRET`

**Qué es:** una contraseña larga y aleatoria que solo conocen el Gateway y Prediction. El Gateway la envía en cada petición (`X-Green-Gateway-Secret`) y Prediction solo acepta decisiones HU-07 si coincide. Así nadie puede registrar decisiones llamando directo a Prediction (hallazgo H-01). **No existe todavía: la generas tú.** Nunca va al repositorio, a Trello ni al chat.

**Generarla** (PowerShell, en tu equipo; copia el resultado):
```powershell
$b = New-Object byte[] 48; [Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($b); [Convert]::ToBase64String($b)
```

**Dónde ponerla** (mismo valor exacto en los dos servicios):
1. https://dashboard.render.com → workspace «My Workspace» → proyecto **green-ai**.
2. Servicio **green-ai-gateway-dev** → menú **Environment** → **Add Environment Variable** → Key `GATEWAY_SHARED_SECRET`, Value: el valor generado → **Save changes**.
3. Servicio **green-ai-prediction-dev** → **Environment** → lo mismo → **Save changes**.
4. Render redespliega cada servicio al guardar (unos minutos).

**Orden recomendado:** poner la variable en los dos servicios → esperar la aprobación del PR #7 → fusionar → Render despliega `main` → avisar a Leonid para la validación en `/dev/`.

**Comprobar:** sin la variable, `POST .../decisions` responde 503 «decisiones deshabilitadas». Con ella y con sesión OPERATOR, «Aprobar» responde 201. Si ves 401 «Petición no originada en el Gateway», el valor no coincide entre los dos servicios.

**Si alguna vez se filtra:** genera otra y cámbiala en los dos servicios a la vez.

## 2. Supabase: dejar solo la contraseña hasheada en `public.usuario`

Contexto: `usuario` es la tabla histórica del dataset (10 usuarios sintéticos `@greenai.com`). La aplicación no la usa para iniciar sesión (eso lo hace Supabase Auth) y ningún código lee `password` ni `password_hash` (comprobado con `git grep` el 19/11/2026). Por eso se puede borrar la columna en texto plano sin romper nada.

Ejecuta en **Supabase → SQL Editor**, **un bloque cada vez**, y mira el resultado antes de seguir.

**Paso 1 — Diagnóstico (no cambia nada):**
```sql
select count(*)                                              as total,
       count(password)                                       as con_password,
       count(password_hash)                                  as con_hash,
       count(*) filter (where password_hash ~ '^\$2[aby]\$') as hash_bcrypt
from public.usuario;

select policyname, cmd, roles, qual
from pg_policies
where schemaname = 'public' and tablename = 'usuario';
```
Anota las cifras. Si `hash_bcrypt` = `total`, todos tienen ya hash bcrypt.

**Paso 2 — Hashear lo que falte y borrar la columna en texto plano (en una transacción):**
```sql
create extension if not exists pgcrypto with schema extensions;

begin;

update public.usuario
set password_hash = extensions.crypt(password, extensions.gen_salt('bf', 10))
where password is not null
  and (password_hash is null or password_hash !~ '^\$2[aby]\$');

-- Comprobación: debe devolver 0 antes de borrar la columna
select count(*) as sin_hash_bcrypt
from public.usuario
where password_hash is null or password_hash !~ '^\$2[aby]\$';

alter table public.usuario drop column password;

commit;
```
Si la comprobación no da 0, ejecuta `rollback;` en lugar de seguir y avísame.

**Paso 3 — Cerrar el acceso público a la tabla:** ninguna parte de la aplicación la necesita.
```sql
alter table public.usuario enable row level security;
revoke all on table public.usuario from anon, authenticated;
```
Si el Paso 1 mostró políticas tipo «Permitir todo» (`qual` = `true`) sobre `usuario`, bórralas con:
```sql
drop policy if exists "<nombre exacto de la política>" on public.usuario;
```

**Paso 4 — Verificar:**
```sql
select column_name from information_schema.columns
where table_schema = 'public' and table_name = 'usuario'
order by ordinal_position;
```
Ya no debe aparecer `password`. Haz una **captura** de este resultado y del Paso 1 (sin mostrar hashes ni correos) para el informe final (F-01 / H-02).

**Después:** prueba que el login de la aplicación sigue funcionando (usa Supabase Auth, no esta tabla).

## 3. Pendiente aparte: la contraseña también está en el repositorio

`software/data-processing/datasets/raw/synthetic_greenai/BD_GreenAi.xlsx` (hoja **Usuarios**) contiene las mismas contraseñas sintéticas en texto plano, y el repositorio es **público**. Ya está registrado como hallazgo OW-04 (captura S30 de semana 13). No son cuentas reales ni sirven para entrar a la aplicación. Opciones:
- **A (recomendada):** nueva versión del Excel sin la columna `password` (commit normal). Ningún documento cita el hash del archivo (comprobado el 19/11/2026); las hojas Hardware y Logs no cambian.
- **B:** además, reescribir el historial de Git para borrarla de commits antiguos. Implica `push --force` y que todos vuelvan a clonar; no se recomienda a estas alturas.
