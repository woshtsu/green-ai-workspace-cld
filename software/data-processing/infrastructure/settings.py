from dataclasses import dataclass, field
import math
import os
from urllib.parse import urlsplit


def validate_url(value, *, secure=False):
    parts = urlsplit(value)
    if (parts.scheme not in (("https",) if secure else ("http", "https"))
            or not parts.hostname or parts.username or parts.password
            or parts.query or parts.fragment):
        raise ValueError("URL de servicio inválida; use HTTP(S) sin credenciales ni query.")
    return value.rstrip("/")


def validate_timeout(value):
    if not math.isfinite(value) or not 0 < value <= 120:
        raise ValueError("REQUEST_TIMEOUT_SECONDS debe estar entre 0 y 120.")
    return value


def configured_credential(value):
    """Reject copied template markers without echoing credential contents."""
    normalized = value.strip()
    return bool(normalized) and not any(char.isspace() for char in normalized) and not (
        "<" in normalized or ">" in normalized
        or normalized.upper() in {"TU_ACCESS_TOKEN", "YOUR_ACCESS_TOKEN", "CHANGEME"}
    )


@dataclass(frozen=True)
class Settings:
    monitoring_url: str
    timeout: float
    supabase_enabled: bool = False
    supabase_url: str = ""
    supabase_key: str = field(default="", repr=False)
    supabase_token: str = field(default="", repr=False)
    historical_page_size: int = 500
    historical_source: str = ""
    sqlite_path: str = ""
    app_env: str = "production"

    def __post_init__(self):
        # Compatibilidad: sin HISTORICAL_SOURCE explícito, SUPABASE_ENABLED decide.
        if not self.historical_source:
            object.__setattr__(self, "historical_source", "supabase" if self.supabase_enabled else "none")

    @classmethod
    def from_env(cls):
        enabled = os.getenv("SUPABASE_ENABLED", "false").lower()
        if enabled not in ("true", "false"):
            raise ValueError("SUPABASE_ENABLED debe ser true o false.")
        app_env = os.getenv("APP_ENV", "production").lower()
        if app_env not in ("development", "test", "production"):
            raise ValueError("APP_ENV debe ser development, test o production.")
        source = os.getenv("HISTORICAL_SOURCE", "").lower() or ("supabase" if enabled == "true" else "none")
        if source not in ("none", "supabase", "sqlite"):
            raise ValueError("HISTORICAL_SOURCE debe ser none, supabase o sqlite.")
        if (source == "supabase") != (enabled == "true"):
            raise ValueError("HISTORICAL_SOURCE y SUPABASE_ENABLED son incoherentes.")
        sqlite_path = os.getenv("SQLITE_PATH", "")
        if source == "sqlite":
            # SQLite no replica Auth, RLS ni procedimientos: nunca en producción.
            if app_env == "production":
                raise ValueError("HISTORICAL_SOURCE=sqlite solo se permite con APP_ENV=development o test.")
            if not sqlite_path or not os.path.isfile(sqlite_path):
                raise ValueError("HISTORICAL_SOURCE=sqlite requiere SQLITE_PATH a una base existente.")
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_API_KEY", "")
        token = os.getenv("SUPABASE_READ_TOKEN", "")
        if enabled == "true":
            validate_url(url, secure=True)
            if not configured_credential(key) or not configured_credential(token):
                raise ValueError("Supabase habilitado requiere API key y token de lectura dedicado.")
            if token.startswith(("sb_publishable_", "sb_secret_")):
                raise ValueError("SUPABASE_READ_TOKEN requiere un JWT de lectura, no una API key.")
        size = int(os.getenv("HISTORICAL_MAX_PAGE_SIZE", "500"))
        if not 1 <= size <= 500:
            raise ValueError("HISTORICAL_MAX_PAGE_SIZE debe estar entre 1 y 500.")
        return cls(
            validate_url(os.getenv("MONITORING_BASE_URL", "http://localhost:8080")),
            validate_timeout(float(os.getenv("REQUEST_TIMEOUT_SECONDS", "10"))),
            enabled == "true", url.rstrip("/"), key, token, size, source, sqlite_path, app_env,
        )
