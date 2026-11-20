"""Emisor JWT LOCAL de pruebas (solo para la auditoría; no forma parte del repo).
Genera una clave ES256, publica el JWKS y emite tokens con los claims que exige el Gateway."""
import json, sys, time, uuid, pathlib
import jwt
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from jwt.algorithms import ECAlgorithm
base = pathlib.Path("/home/claude/idp")
keyf = base / "key.pem"
if not keyf.exists():
    k = ec.generate_private_key(ec.SECP256R1())
    keyf.write_bytes(k.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
k = serialization.load_pem_private_key(keyf.read_bytes(), None)
jwk = json.loads(ECAlgorithm.to_jwk(k.public_key())); jwk.update({"kid": "audit-key-1", "use": "sig", "alg": "ES256"})
(base / "auth/v1/.well-known/jwks.json").write_text(json.dumps({"keys": [jwk]}))
ISS = "http://127.0.0.1:18999/auth/v1"
def token(user_role, **extra):
    now = int(time.time())
    claims = {"iss": ISS, "aud": "authenticated", "sub": str(uuid.uuid4()), "role": "authenticated",
              "iat": now, "exp": now + 3600, "is_anonymous": False}
    if user_role: claims["user_role"] = user_role
    claims.update(extra)
    return jwt.encode(claims, k, algorithm="ES256", headers={"kid": "audit-key-1"})
if __name__ == "__main__":
    out = {r or "NONE": token(r) for r in ["ADMIN", "OPERATOR", "VIEWER", None]}
    out["EXPIRED"] = token("OPERATOR", exp=int(time.time()) - 5)
    out["ANON"] = token("OPERATOR", is_anonymous=True)
    (base / "tokens.json").write_text(json.dumps(out))
    print("tokens:", ", ".join(out))
