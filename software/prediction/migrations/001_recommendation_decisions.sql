-- HU-07: decisiones humanas sobre recomendaciones (PostgreSQL / Supabase).
-- NO APLICADA: no se ejecuta contra ningún entorno sin autorización explícita del usuario.
-- Equivalente a la tabla SQLite creada por SqliteDecisionRepository.

CREATE TABLE IF NOT EXISTS public.recommendation_decisions (
    decision_id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    recommendation_id     uuid        NOT NULL,
    decision              text        NOT NULL CHECK (decision IN ('APPROVED', 'REJECTED')),
    comment               text        CHECK (comment IS NULL OR char_length(comment) <= 500),
    decided_by            text        NOT NULL,
    decided_by_role       text        NOT NULL CHECK (decided_by_role IN ('ADMIN', 'OPERATOR', 'VIEWER')),
    decided_at            timestamptz NOT NULL DEFAULT now(),
    recommendation_sha256 char(64)    NOT NULL,
    execution_allowed     boolean     NOT NULL DEFAULT false CHECK (execution_allowed = false)
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_decisions_recommendation_user
    ON public.recommendation_decisions (recommendation_id, decided_by);

-- RLS habilitada sin políticas: ningún rol anon/authenticated accede por la API de Supabase.
-- El servicio accederá con credenciales de servidor, nunca desde el frontend.
ALTER TABLE public.recommendation_decisions ENABLE ROW LEVEL SECURITY;
