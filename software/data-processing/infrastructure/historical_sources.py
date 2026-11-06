"""Selección del adaptador de históricos según la configuración (el entorno elige, el código es el mismo)."""
from domain.errors import SourceNotConfigured
from domain.ports.historical_logs_source import HistoricalLogsSource
from infrastructure.adapters.input.sqlite_historical_logs_adapter import SqliteHistoricalLogsAdapter
from infrastructure.adapters.input.supabase_historical_logs_adapter import SupabaseHistoricalLogsAdapter


def historical_source(settings, request_id=None) -> HistoricalLogsSource:
    if settings.historical_source == "supabase":
        return SupabaseHistoricalLogsAdapter(settings.supabase_url, settings.supabase_key,
                                             settings.supabase_token, settings.timeout, request_id)
    if settings.historical_source == "sqlite":
        return SqliteHistoricalLogsAdapter(settings.sqlite_path)
    raise SourceNotConfigured("La fuente de históricos no está configurada.")
