package policy

import (
	"testing"
	"time"
)

func TestUpstreamPathsMatchJavaGateway(t *testing.T) {
	want := map[string]string{
		"GET /api/monitoring/v1/metrics/current":       "/api/v1/metrics/current",
		"GET /api/processing/v1/historical-logs":       "/api/v1/historical-logs",
		"GET /api/processing/v1/prediction/dataset":    "/api/v1/prediction/dataset",
		"POST /api/prediction/v1/predictions":          "/v1/predictions",
		"POST /api/recommendations/v1/energy":          "/v1/energy",
		"POST /api/recommendations/v1/recommendations": "/v1/recommendations",
	}
	if n := len(Routes()); n != 12 {
		t.Fatalf("se esperaban 12 rutas publicadas, hay %d", n)
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

const rid = "3f2b8c1e-0a5d-4e6f-9b7a-1c2d3e4f5a6b"

func TestDecisionsRouteMatchesOnlyUUID(t *testing.T) {
	p := "/api/recommendations/v1/recommendations/" + rid + "/decisions"
	for _, m := range []string{"GET", "POST"} {
		r, ok := Match(m, p)
		if !ok || r.UpstreamPath() != "/v1/recommendations/"+rid+"/decisions" || r.MaxBody != maxBody || r.Timeout != 30*time.Second {
			t.Errorf("%s: %+v ok=%v", m, r, ok)
		}
	}
	base := "/api/recommendations/v1/recommendations/"
	for _, bad := range []string{base + "abc/decisions", base + rid + "0/decisions", base + "zf2b8c1e-0a5d-4e6f-9b7a-1c2d3e4f5a6b/decisions",
		base + "/decisions", base + rid + "/decisions/", base + rid, base + "{uuid}/decisions", base + rid + "/x/decisions"} {
		for _, m := range []string{"GET", "POST"} {
			if _, ok := Match(m, bad); ok {
				t.Errorf("%s %s no debe estar publicada", m, bad)
			}
		}
	}
	if _, ok := Match("PUT", p); ok {
		t.Error("PUT no debe estar publicada")
	}
	if !NotPublished("GET", base+"abc/decisions") || NotPublished("GET", p) || NotPublished("DELETE", base+"abc/decisions") ||
		NotPublished("GET", base+"/decisions") || NotPublished("GET", "/api/monitoring/v1/metrics/current") {
		t.Error("NotPublished: solo {id} no UUID de GET/POST")
	}
}

func TestDecisionsRoles(t *testing.T) {
	p := "/api/recommendations/v1/recommendations/" + rid + "/decisions"
	get, _ := Match("GET", p)
	post, _ := Match("POST", p)
	if !get.Allows("VIEWER") || !get.Allows("ADMIN") || !get.Allows("OPERATOR") || get.Allows("ROOT") {
		t.Error("GET: ADMIN, OPERATOR y VIEWER")
	}
	if post.Allows("VIEWER") || !post.Allows("ADMIN") || !post.Allows("OPERATOR") {
		t.Error("POST: solo ADMIN y OPERATOR")
	}
}
