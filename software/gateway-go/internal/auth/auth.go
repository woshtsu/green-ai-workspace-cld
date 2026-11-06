// Package auth define el puerto de verificación de identidad del Gateway.
package auth

import (
	"context"
	"errors"
)

// Principal es la identidad ya verificada que usa la política de acceso.
type Principal struct {
	Subject string
	Role    string // valor del claim user_role ("" si falta)
}

var (
	// ErrInvalidToken: token ausente, malformado, con firma, emisor, audiencia o vigencia inválidos → 401.
	ErrInvalidToken = errors.New("token inválido")
	// ErrUnavailable: no se pudo obtener el JWKS del emisor → 503 (no se acepta el token).
	ErrUnavailable = errors.New("proveedor de identidad no disponible")
)

// Verifier es el puerto: el adaptador concreto valida un JWT de Supabase Auth.
type Verifier interface {
	Verify(ctx context.Context, token string) (Principal, error)
}
