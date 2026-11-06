"""Adaptador mínimo para delegar un encargo a Antigravity CLI (`agy`) en modo headless.

Uso:
  python herramientas_IA/agentes/agy_task.py --cwd <dir> --prompt-file encargo.md \
      [--readonly] [--mode plan|accept-edits] [--timeout 600] [--conversation ID] [--out dir]

Diseño (ver docs/TOOLS_EVALUATION.md):
- Invoca el ejecutable con una lista de argumentos (sin shell, sin concatenar comandos).
- Ajustes solo para esta sesión vía `--settings` (nunca se guardan): desactiva el uso de
  créditos de pago (`useG1Credits: false`) y, con --readonly, deniega escritura, comandos,
  URLs y MCP.
- Nunca usa --dangerously-skip-permissions.
- Guarda stdout, stderr y un resumen en --out; informa de acciones denegadas (stderr) y de
  cambios reales en el árbol Git del directorio de trabajo (antes/después).
- Un solo intento; sin reintentos automáticos. Si la cuota se agota, el resultado lo indica.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
from pathlib import Path

MAX_PROMPT_CHARS = 20_000  # margen frente al límite de línea de comandos de Windows (32 767)

READONLY_DENY = ["write_file(*)", "command(*)", "read_url(*)", "execute_url(*)", "mcp(*)"]


def git_snapshot(cwd: Path) -> str | None:
    try:
        r = subprocess.run(["git", "-C", str(cwd), "status", "--porcelain", "--untracked-files=all"],
                           capture_output=True, text=True, timeout=60, encoding="utf-8", errors="replace")
        return r.stdout if r.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def build_argv(agy: str, prompt: str, args: argparse.Namespace) -> list[str]:
    settings: dict = {"useG1Credits": False}
    if args.readonly:
        settings["permissions"] = {"deny": READONLY_DENY}
    argv = [agy, "-p", prompt, "--output-format", "json", "--settings", json.dumps(settings)]
    if args.mode:
        argv += ["--mode", args.mode]
    if args.model:
        argv += ["--model", args.model]
    if args.conversation:
        argv += ["--conversation", args.conversation]
    if args.timeout:
        argv += ["--print-timeout", f"{args.timeout}s"]
    return argv


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--cwd", required=True, type=Path, help="Directorio de trabajo explícito del agente")
    p.add_argument("--prompt-file", required=True, type=Path)
    p.add_argument("--readonly", action="store_true", help="Deniega escritura, comandos, URLs y MCP")
    p.add_argument("--mode", choices=["plan", "accept-edits"], default=None)
    p.add_argument("--model", default=None)
    p.add_argument("--conversation", default=None, help="Reanudar una conversación concreta")
    p.add_argument("--timeout", type=int, default=600, help="Segundos (también se pasa a --print-timeout)")
    p.add_argument("--out", type=Path, default=Path("agy-runs"))
    args = p.parse_args()

    agy = shutil.which("agy")
    if not agy:
        print("ERROR: no se encontró 'agy' en PATH", file=sys.stderr)
        return 2
    cwd = args.cwd.resolve()
    if not cwd.is_dir():
        print(f"ERROR: --cwd no existe: {cwd}", file=sys.stderr)
        return 2
    prompt = args.prompt_file.read_text(encoding="utf-8")
    if len(prompt) > MAX_PROMPT_CHARS:
        print(f"ERROR: encargo de {len(prompt)} caracteres; reducir contexto (máx {MAX_PROMPT_CHARS})", file=sys.stderr)
        return 2

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out = (args.out / f"{stamp}-{args.prompt_file.stem}").resolve()
    out.mkdir(parents=True, exist_ok=True)

    before = git_snapshot(cwd)
    argv = build_argv(agy, prompt, args)
    started = dt.datetime.now()
    try:
        r = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=args.timeout + 60)
        code, stdout, stderr = r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired as e:
        code, stdout, stderr = -1, e.stdout or "", (e.stderr or "") + "\nTIMEOUT del adaptador"
    after = git_snapshot(cwd)

    (out / "stdout.json").write_text(stdout, encoding="utf-8")
    (out / "stderr.txt").write_text(stderr, encoding="utf-8")

    envelope: dict = {}
    try:
        envelope = json.loads(stdout) if stdout.strip() else {}
    except json.JSONDecodeError:
        envelope = {"parse_error": "stdout no es JSON"}

    denied = [ln for ln in stderr.splitlines() if "deni" in ln.lower() or "permission" in ln.lower()]
    quota = [ln for ln in stderr.splitlines() if "quota" in ln.lower() or "rate limit" in ln.lower()]
    summary = {
        "started": started.isoformat(timespec="seconds"),
        "elapsed_s": round((dt.datetime.now() - started).total_seconds(), 1),
        "cwd": str(cwd),
        "readonly": args.readonly,
        "mode": args.mode,
        "exit_code": code,
        "status": envelope.get("status"),
        "conversation_id": envelope.get("conversation_id"),
        "usage": envelope.get("usage"),
        "error": envelope.get("error"),
        "permission_notices": denied,
        "quota_notices": quota,
        "git_changed": None if before is None or after is None else before != after,
        "git_status_after": after,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "response.md").write_text(envelope.get("response") or "", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"\nResultados en: {out}")
    ok = code == 0 and envelope.get("status") == "SUCCESS"
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
