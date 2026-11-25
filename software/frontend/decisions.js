/* HU-07: decisión humana sobre una recomendación. Lógica pura (sin DOM).
   Registrar una decisión es un registro de auditoría; nunca ejecuta cambios. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.GreenDecisions = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const MAX_COMMENT = 500;
  const FIXED_NOTICE = 'Registrar una decisión no ejecuta ningún cambio';
  const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  const LABELS = { APPROVED: 'Aprobada', REJECTED: 'Rechazada' };

  /** Los VIEWER (y roles desconocidos o pendientes) no ven los botones. */
  function canDecide(role) {
    const r = String(role || '').trim().toUpperCase();
    return r === 'ADMIN' || r === 'OPERATOR';
  }

  /** Normaliza el comentario; devuelve {ok, comment, error}. */
  function validateComment(text) {
    const comment = String(text == null ? '' : text).trim();
    if (comment.length > MAX_COMMENT) return { ok: false, comment, error: `El comentario no puede superar ${MAX_COMMENT} caracteres (tiene ${comment.length}).` };
    return { ok: true, comment, error: null };
  }

  function decisionsPath(recommendationId) {
    if (!UUID.test(String(recommendationId || ''))) throw new Error('Identificador de recomendación inválido.');
    return `/api/recommendations/v1/recommendations/${recommendationId}/decisions`;
  }

  /** Cuerpo del POST: la recomendación completa tal como la devolvió la evaluación. */
  function buildPayload(decision, commentText, recommendation) {
    if (decision !== 'APPROVED' && decision !== 'REJECTED') throw new Error('Decisión inválida.');
    if (!recommendation || recommendation.executionAllowed !== false) throw new Error('Recomendación inválida: no puede permitir ejecución.');
    const v = validateComment(commentText);
    if (!v.ok) throw new Error(v.error);
    const payload = { decision, recommendation };
    if (v.comment) payload.comment = v.comment;
    return payload;
  }

  /** Mensaje amigable por estado HTTP (401/403/404/409/422/503); null si no aplica.
   *  role: rol de la sesión. Un 403 con rol ADMIN/OPERATOR no es de permisos: el servidor
   *  aún no publica la ruta (backend sin desplegar), y se dice así en lugar de culpar al rol. */
  function friendlyError(status, detail, role) {
    const extra = typeof detail === 'string' && detail && detail.length < 160 ? ` ${detail}` : '';
    switch (status) {
      case 401: return 'Tu sesión venció. Inicia sesión de nuevo y repite la decisión.';
      case 403: return canDecide(role)
        ? 'El servidor todavía no admite registrar decisiones (función no desplegada). Avisa al administrador.'
        : 'Tu rol no permite registrar decisiones. Solo ADMIN y OPERATOR pueden hacerlo.';
      case 404: return 'El registro de decisiones no está disponible en el servidor. Avisa al administrador.';
      case 503: return 'El registro de decisiones está deshabilitado temporalmente en el servidor (falta su configuración). Avisa al administrador.';
      case 409: return 'Ya registraste una decisión para esta recomendación. Solo se permite una por usuario.';
      case 422: return `La decisión no se pudo validar.${extra || ' Evalúa de nuevo la recomendación y vuelve a intentarlo.'}`;
      default: return null;
    }
  }

  function normalizeList(body) {
    return Array.isArray(body && body.decisions) ? body.decisions : [];
  }

  /** Línea de texto de una decisión registrada. */
  function describe(d) {
    const x = d || {};
    return `${LABELS[x.decision] || x.decision || '—'} · ${x.decidedBy || '—'} (${x.decidedByRole || '—'}) · ${x.decidedAt || '—'}`
      + (x.comment ? ` · «${x.comment}»` : '');
  }

  /** Una recomendación solo puede decidirse si sigue siendo la vigente. */
  function isCurrent(current, recommendation) {
    return !!(current && recommendation && current.recommendationId === recommendation.recommendationId);
  }

  return { MAX_COMMENT, FIXED_NOTICE, canDecide, validateComment, decisionsPath, buildPayload, friendlyError, normalizeList, describe, isCurrent };
});
