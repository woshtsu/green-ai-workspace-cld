-- Perfil de DESARROLLO: equivalente SQLite de public.hardware y public.logs de Supabase
-- (fuente: software/simulator/docs/assets/esquema-verificado.json, snapshot 2026-09-22).
--
-- Divergencias deliberadas (NO se simulan):
--  * Sin tabla usuario ni FK hardware.usuario_id -> usuario: identidades y Auth pertenecen a Supabase.
--  * Sin RLS, roles, políticas, funciones ni procedimientos: SQLite no los tiene. La evidencia de
--    procedimientos almacenados y RLS solo puede obtenerse en Supabase/PostgreSQL.
--  * timestamptz -> TEXT UTC canónico 'YYYY-MM-DDTHH:MM:SS.ffffffZ' (CHECK), para que el orden
--    lexicográfico coincida con el cronológico y el cursor (timestamp, log_id) se comporte igual.
--  * numeric(p,2) -> REAL: sin precisión decimal exacta; los valores semilla tienen 2 decimales.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS hardware (
    hardware_id     TEXT PRIMARY KEY CHECK (length(hardware_id) BETWEEN 1 AND 20),
    usuario_id      TEXT NOT NULL CHECK (length(usuario_id) <= 20),
    hostname        TEXT NOT NULL CHECK (length(hostname) <= 100),
    ip_address      TEXT NOT NULL CHECK (length(ip_address) <= 45),
    cpu_cores       INTEGER NOT NULL,
    ram_gb          REAL NOT NULL,
    max_watts       REAL NOT NULL,
    ubicacion_rack  TEXT CHECK (ubicacion_rack IS NULL OR length(ubicacion_rack) <= 50),
    estado          TEXT DEFAULT 'activo' CHECK (estado IS NULL OR length(estado) <= 20),
    fecha_registro  TEXT
) STRICT;

CREATE TABLE IF NOT EXISTS logs (
    log_id               TEXT PRIMARY KEY CHECK (length(log_id) BETWEEN 1 AND 20),
    hardware_id          TEXT NOT NULL REFERENCES hardware(hardware_id) ON DELETE CASCADE,
    timestamp            TEXT NOT NULL CHECK (timestamp GLOB
        '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9][0-9][0-9][0-9]Z'),
    cpu_utilization_pct  REAL NOT NULL,
    ram_utilization_pct  REAL NOT NULL,
    temperatura_celsius  REAL NOT NULL,
    energia_watts        REAL NOT NULL,
    prediccion_watts     REAL NOT NULL,
    accion_recomendada   TEXT CHECK (accion_recomendada IS NULL OR length(accion_recomendada) <= 100),
    cumple_sla           INTEGER DEFAULT 1 CHECK (cumple_sla IS NULL OR cumple_sla IN (0, 1))
) STRICT;

CREATE INDEX IF NOT EXISTS idx_logs_hardware_timestamp ON logs (hardware_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs (timestamp DESC);
