/* Traduce errores técnicos de la API a mensajes humanos. Lógica pura (sin DOM). */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.GreenErrors = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const WAIT_CODES = new Set(['INSUFFICIENT_DATA', 'INVALID_DATASET']);
  const CONTEXTS = new Set(['prediccion', 'recomendacion', 'energia', 'reporte', 'metricas']);

  function problemOf(body) {
    const b = body && typeof body === 'object' ? body : {};
    const nested = b.detail && typeof b.detail === 'object' && !Array.isArray(b.detail) ? b.detail : {};
    const code = String(b.code || nested.code || '');
    let detail = '';
    if (typeof b.detail === 'string') detail = b.detail;
    else if (Array.isArray(b.detail)) detail = b.detail.map(d => d && (d.msg || d.message) || '').filter(Boolean).join('; ');
    else detail = String(nested.message || nested.detail || b.message || '');
    return { code, detail };
  }

  /** @param {{status?:number|null, body?:object, reference?:string|null, context?:string, networkError?:boolean}} input */
  function classify(input = {}) {
    const context = CONTEXTS.has(input.context) ? input.context : 'metricas';
    const status = Number.isFinite(input.status) ? input.status : null;
    const { code, detail } = problemOf(input.body);
    const technical = [status ? `HTTP ${status}` : null, code || null, detail || null,
      input.reference ? `Referencia ${input.reference}` : null].filter(Boolean).join(' · ');
    const base = { detalleTecnico: technical, status, code };

    if (status === null || input.networkError) {
      return { ...base, tipo: 'servicio', titulo: 'El servicio está despertando',
        mensaje: 'Los servicios de la nube se duermen cuando no se usan. Espera un minuto y vuelve a intentarlo.',
        accion: 'Reintentar' };
    }
    if (status === 401) {
      return { ...base, tipo: 'sesion', titulo: 'Tu sesión venció',
        mensaje: 'Inicia sesión de nuevo y repite la operación.', accion: 'Ir a iniciar sesión' };
    }
    if (status === 403) {
      return { ...base, tipo: 'permisos', titulo: 'Tu rol no permite esta acción',
        mensaje: 'Con tu rol actual solo puedes consultar. Pide a un administrador que te asigne el rol necesario.', accion: null };
    }
    const waits = WAIT_CODES.has(code)
      || (status === 422 && (context === 'prediccion' || (context === 'recomendacion' && !detail)));
    if (waits) {
      return { ...base, tipo: 'espera', titulo: 'Aún estamos reuniendo datos',
        mensaje: 'El simulador necesita unos 20 minutos de historial para predecir. Vuelve a intentarlo en unos minutos.',
        accion: 'Reintentar' };
    }
    if (status === 422 || status === 400) {
      const campo = context === 'energia'
        ? 'Revisa que el archivo sea un JSON con "origin" y al menos 2 muestras con "timestamp" y "watts".'
        : context === 'reporte'
          ? 'Revisa las fechas y el código de hardware (por ejemplo HW045).'
          : 'Revisa los valores que escribiste (memoria y errores entre 0 y 100, latencia mayor o igual a 0).';
      return { ...base, tipo: 'datos', titulo: 'Hay datos por corregir',
        mensaje: detail && detail.length < 160 ? `${detail} ${campo}`.trim() : campo, accion: null };
    }
    if (status === 413) {
      return { ...base, tipo: 'datos', titulo: 'El archivo es demasiado grande',
        mensaje: 'Reduce el número de muestras (máximo 1,5 MB).', accion: null };
    }
    return { ...base, tipo: 'servicio', titulo: 'No pudimos completar la operación',
      mensaje: 'El servicio no respondió como se esperaba. Espera un minuto y vuelve a intentarlo.', accion: 'Reintentar' };
  }

  /** Error de JavaScript con la información amigable adjunta (message = texto sin códigos). */
  function toError(input) {
    const friendly = classify(input);
    const error = new Error(`${friendly.titulo}. ${friendly.mensaje}`);
    error.friendly = friendly;
    return error;
  }

  /** Para errores capturados (AbortError/TimeoutError/TypeError de red). */
  function fromException(error, context) {
    if (error && error.friendly) return error.friendly;
    const name = error && error.name;
    const network = name === 'TimeoutError' || name === 'AbortError' || name === 'TypeError';
    if (network || !error) return classify({ status: null, networkError: true, context });
    return { ...classify({ status: 500, context }), status: null, detalleTecnico: String(error.message || error) };
  }

  return { classify, toError, fromException, problemOf };
});
