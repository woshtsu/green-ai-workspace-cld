-- Base PostgreSQL de PRUEBAS DE CONTRATO (no es Supabase ni su esquema completo).
-- Reproduce public.hardware y public.logs según esquema-verificado.json (snapshot 2026-09-22),
-- sin la tabla usuario ni su FK. Roles mínimos para PostgREST:
--   web_reader      -> solo SELECT sobre logs (equivalente al token de lectura dedicado)
--   contract_writer -> inserta/borra filas de prueba (solo lo usa la prueba)
CREATE TABLE public.hardware (
    hardware_id     varchar(20) PRIMARY KEY,
    usuario_id      varchar(20) NOT NULL,
    hostname        varchar(100) NOT NULL,
    ip_address      varchar(45) NOT NULL,
    cpu_cores       integer NOT NULL,
    ram_gb          numeric(6,2) NOT NULL,
    max_watts       numeric(6,2) NOT NULL,
    ubicacion_rack  varchar(50),
    estado          varchar(20) DEFAULT 'activo',
    fecha_registro  timestamptz DEFAULT now()
);

CREATE TABLE public.logs (
    log_id               varchar(20) PRIMARY KEY,
    hardware_id          varchar(20) NOT NULL REFERENCES public.hardware(hardware_id) ON DELETE CASCADE,
    "timestamp"          timestamptz NOT NULL,
    cpu_utilization_pct  numeric(5,2) NOT NULL,
    ram_utilization_pct  numeric(5,2) NOT NULL,
    temperatura_celsius  numeric(5,2) NOT NULL,
    energia_watts        numeric(6,2) NOT NULL,
    prediccion_watts     numeric(6,2) NOT NULL,
    accion_recomendada   varchar(100),
    cumple_sla           boolean DEFAULT true
);
CREATE INDEX idx_logs_hardware_timestamp ON public.logs (hardware_id, "timestamp" DESC);
CREATE INDEX idx_logs_timestamp ON public.logs ("timestamp" DESC);

CREATE ROLE web_anon NOLOGIN;
CREATE ROLE web_reader NOLOGIN;
CREATE ROLE contract_writer NOLOGIN;
-- La contraseña de authenticator llega por variable de entorno en el arranque (ver 01-authenticator.sh).
CREATE ROLE authenticator NOINHERIT LOGIN;
GRANT web_anon, web_reader, contract_writer TO authenticator;

GRANT USAGE ON SCHEMA public TO web_reader, contract_writer;
GRANT SELECT ON public.logs TO web_reader;
GRANT SELECT, INSERT, DELETE ON public.hardware, public.logs TO contract_writer;
