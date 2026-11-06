package policy

import "testing"

func TestUpstreamPathsMatchJavaGateway(t *testing.T) {
	want := map[string]string{
		"GET /api/monitoring/v1/metrics/current":       "/api/v1/metrics/current",
		"GET /api/processing/v1/historical-logs":       "/api/v1/historical-logs",
		"GET /api/processing/v1/prediction/dataset":    "/api/v1/prediction/dataset",
		"POST /api/prediction/v1/predictions":          "/v1/predictions",
		"POST /api/recommendations/v1/energy":          "/v1/energy",
		"POST /api/recommendations/v1/recommendations": "/v1/recommendations",
	}
	if n := len(Routes()); n != 9 {
		t.Fatalf("se esperaban 9 rutas publicadas, hay %d", n)
	}
	for key, path := range want {
		var method, p string
		for i := range key {
			if key[i] == ' ' {
				method, p = key[:i], key[i+1:]
				break
			}
		}
		r, ok := Match(method, p)
		if !ok || r.UpstreamPath() != path {
			t.Errorf("%s -> %q (ok=%v), se esperaba %q", key, r.UpstreamPath(), ok, path)
		}
	}
}

func TestNoWildcardsOrMethodMix(t *testing.T) {
	for _, c := range []struct{ m, p string }{
		{"POST", "/api/monitoring/v1/metrics/current"}, {"GET", "/api/prediction/v1/predictions"},
		{"GET", "/api/processing/v1/anything"}, {"GET", "/api/monitoring/v1/metrics/current/"},
		{"GET", "/api/monitoring/v1/metrics"},
	} {
		if _, ok := Match(c.m, c.p); ok {
			t.Errorf("%s %s no debe estar publicada", c.m, c.p)
		}
	}
}

func TestRoles(t *testing.T) {
	for role, ok := range map[string]bool{"ADMIN": true, "OPERATOR": true, "": false, "ROOT": false, "admin": false} {
		if RoleAllowed(role) != ok {
			t.Errorf("rol %q", role)
		}
	}
}

func TestViewerIsReadOnly(t *testing.T) {
	get, _ := Match("GET", "/api/monitoring/v1/metrics/current")
	post, _ := Match("POST", "/api/prediction/v1/predictions")
	if !get.Allows("VIEWER") || post.Allows("VIEWER") {
		t.Fatal("VIEWER debe poder leer (GET) y no invocar inferencia (POST)")
	}
	if !post.Allows("OPERATOR") || !post.Allows("ADMIN") || post.Allows("ROOT") || get.Allows("") {
		t.Fatal("roles ADMIN/OPERATOR completos; desconocidos sin acceso")
	}
}
