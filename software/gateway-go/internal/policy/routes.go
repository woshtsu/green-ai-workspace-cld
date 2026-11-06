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
	for _, p := range []string{"metrics/history", "historical-logs", "prediction/dataset"} {
		routes = append(routes, Route{"GET", "/api/processing/v1/" + p, DataProcessing, 3, "/api/v1", 0, 15 * time.Second})
	}
	routes = append(routes, Route{"POST", "/api/prediction/v1/predictions", Prediction, 2, "", maxBody, 30 * time.Second})
	for _, p := range []string{"recommendations", "energy"} {
		routes = append(routes, Route{"POST", "/api/recommendations/v1/" + p, Prediction, 2, "", maxBody, 30 * time.Second})
	}
	return routes
}

// Routes devuelve una copia de la tabla publicada.
func Routes() []Route { return append([]Route(nil), table...) }

// Match busca coincidencia exacta de método y ruta (sin comodines ni barra final).
func Match(method, path string) (Route, bool) {
	for _, r := range table {
		if r.Method == method && r.Path == path {
			return r, true
		}
	}
	return Route{}, false
}

// RoleAllowed indica si el rol del token puede usar rutas publicadas.
func RoleAllowed(role string) bool { return allowedRoles[role] }

// UpstreamPath aplica StripPrefix y PrefixPath.
func (r Route) UpstreamPath() string {
	parts := strings.Split(strings.TrimPrefix(r.Path, "/"), "/")
	if r.StripPrefix >= len(parts) {
		return r.PrefixPath + "/"
	}
	return r.PrefixPath + "/" + strings.Join(parts[r.StripPrefix:], "/")
}
