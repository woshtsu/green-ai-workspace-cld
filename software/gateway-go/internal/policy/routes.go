// Package policy es el dominio del Gateway: qué rutas existen, a qué servicio van, con qué límites
// y qué roles pueden usarlas. No depende de HTTP, JWT ni red.
package policy

import (
	"strings"
	"time"
)

// Upstream identifica un servicio interno; la URL concreta la aporta la configuración.
type Upstream string

const (
	Monitoring     Upstream = "monitoring"
	DataProcessing Upstream = "data-processing"
	Prediction     Upstream = "prediction"
)

// Roles admitidos en el claim user_role (igual que el Gateway Java).
var allowedRoles = map[string]bool{"ADMIN": true, "OPERATOR": true}

// Route es una ruta publicada explícitamente. Nada fuera de la tabla se reenvía.
type Route struct {
	Method      string
	Path        string
	Upstream    Upstream
	StripPrefix int // segmentos eliminados, como StripPrefix de Spring Cloud Gateway
	PrefixPath  string
	MaxBody     int64 // 0 = sin límite propio
	Timeout     time.Duration
}

const (
	defaultTimeout = 6 * time.Second
	maxBody        = 2 << 20 // 2 MB
)

var table = buildTable()

func buildTable() []Route {
	var routes []Route
	for _, p := range []string{"catalog", "current", "history"} {
		routes = append(routes, Route{"GET", "/api/monitoring/v1/metrics/" + p, Monitoring, 3, "/api/v1", 0, defaultTimeout})
	}
	for _, p := range []string{"metrics/history", "historical-logs", "prediction/dataset", "reports/historical-summary"} {
		routes = append(routes, Route{"GET", "/api/processing/v1/" + p, DataProcessing, 3, "/api/v1", 0, 15 * time.Second})
	}
	routes = append(routes, Route{"POST", "/api/prediction/v1/predictions", Prediction, 2, "", maxBody, 30 * time.Second})
	for _, p := range []string{"recommendations", "energy"} {
		routes = append(routes, Route{"POST", "/api/recommendations/v1/" + p, Prediction, 2, "", maxBody, 30 * time.Second})
	}
	// {uuid}: único segmento paramétrico admitido (sin comodines generales); solo UUID.
	decisions := "/api/recommendations/v1/recommendations/{uuid}/decisions"
	routes = append(routes,
		Route{"POST", decisions, Prediction, 2, "", maxBody, 30 * time.Second},
		Route{"GET", decisions, Prediction, 2, "", maxBody, 30 * time.Second})
	return routes
}

const uuidSegment = "{uuid}"

// isUUID comprueba el formato 8-4-4-4-12 hexadecimal.
func isUUID(s string) bool {
	if len(s) != 36 {
		return false
	}
	for i := 0; i < len(s); i++ {
		switch c := s[i]; {
		case i == 8 || i == 13 || i == 18 || i == 23:
			if c != '-' {
				return false
			}
		case (c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F'):
		default:
			return false
		}
	}
	return true
}

// matchPattern compara segmento a segmento; {uuid} exige un UUID válido (strict) o cualquier segmento no vacío.
func matchPattern(pattern, path string, strict bool) bool {
	ps, xs := strings.Split(pattern, "/"), strings.Split(path, "/")
	if len(ps) != len(xs) {
		return false
	}
	for i := range ps {
		switch {
		case ps[i] == uuidSegment && strict:
			if !isUUID(xs[i]) {
				return false
			}
		case ps[i] == uuidSegment:
			if xs[i] == "" {
				return false
			}
		case ps[i] != xs[i]:
			return false
		}
	}
	return true
}

// NotPublished indica que la ruta tiene la forma de una ruta con {uuid} para ese método pero el
// segmento no es un UUID: se responde 404 (el Gateway Java: sin ruta). No aplica a rutas sin {uuid}.
func NotPublished(method, path string) bool {
	for _, r := range table {
		if r.Method == method && strings.Contains(r.Path, uuidSegment) &&
			matchPattern(r.Path, path, false) && !matchPattern(r.Path, path, true) {
			return true
		}
	}
	return false
}

// Routes devuelve una copia de la tabla publicada.
func Routes() []Route { return append([]Route(nil), table...) }

// Match busca coincidencia exacta de método y ruta (sin comodines ni barra final); el segmento {uuid}
// solo acepta UUID. La Route devuelta lleva la ruta concreta (UpstreamPath la reenvía tal cual).
func Match(method, path string) (Route, bool) {
	for _, r := range table {
		if r.Method != method {
			continue
		}
		if !strings.Contains(r.Path, uuidSegment) && r.Path == path {
			return r, true
		}
		if strings.Contains(r.Path, uuidSegment) && matchPattern(r.Path, path, true) {
			r.Path = path
			return r, true
		}
	}
	return Route{}, false
}

// RoleAllowed indica si el rol del token puede usar rutas publicadas.
func RoleAllowed(role string) bool { return allowedRoles[role] || role == "VIEWER" }

// Allows decide el acceso por ruta: ADMIN y OPERATOR usan todas las rutas publicadas;
// VIEWER (observador, HU-14) solo las de lectura (GET), no la inferencia ni las recomendaciones.
func (r Route) Allows(role string) bool {
	if allowedRoles[role] {
		return true
	}
	return role == "VIEWER" && r.Method == "GET"
}

// UpstreamPath aplica StripPrefix y PrefixPath.
func (r Route) UpstreamPath() string {
	parts := strings.Split(strings.TrimPrefix(r.Path, "/"), "/")
	if r.StripPrefix >= len(parts) {
		return r.PrefixPath + "/"
	}
	return r.PrefixPath + "/" + strings.Join(parts[r.StripPrefix:], "/")
}
