"""Copia reproducible de las fuentes del workspace antiguo al monorepo (sin .git anidados).

Uso (desde la raíz del monorepo):
  python herramientas_IA/migracion/copiar_fuentes.py --workspace .. [--only monitoring,gateway] [--dry-run]

- Toma solo archivos versionados o no ignorados de cada repositorio (`git ls-files -co --exclude-standard`),
  lo que incluye cambios locales sin commit y excluye caches/builds ignorados.
- Aplica exclusiones adicionales (secretos, binarios, dependencias, documentos docentes duplicados).
- No borra ni mueve nada en el origen. Escribe docs/migracion/manifiesto-copia.json con SHA de origen,
  rama, estado sucio y archivos excluidos.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import shutil
import subprocess
from pathlib import Path, PurePosixPath

# destino -> (repo git de origen, subcarpeta dentro del repo o "", carpeta destino)
UNITS: dict[str, tuple[str, str, str]] = {
    "monitoring": ("green-ai-monitoring", "", "software/monitoring"),
    "simulator": ("green-ai-simulator", "", "software/simulator"),
    "gateway": ("green-ai-gateway", "", "software/gateway"),
    "data-processing": ("green-ai-data-processing/Green-IA", "data-processing-service", "software/data-processing"),
    "data-processing-datasets": ("green-ai-data-processing/Green-IA", "datasets", "software/data-processing/datasets"),
    "prediction": ("green-ai-prediction/green-ai-project-docs", "", "software/prediction"),
    "frontend": ("green-ai-front-end/Frontend-GreenAi", "", "software/frontend"),
}

# Archivos sueltos del workspace raíz (no pertenecen a ningún repo hijo).
ROOT_FILES: dict[str, str] = {
    "docker-compose.yml": "software/infraestructura/docker-compose.yml",
    "compose.swagger.yaml": "software/infraestructura/compose.swagger.yaml",
    "compose.observability.yml": "software/infraestructura/compose.observability.yml",
    "prometheus-demo.yml": "software/infraestructura/prometheus/prometheus.yml",
    "observability/alerts.yml": "software/infraestructura/prometheus/alerts.yml",
    "observability/grafana/dashboards/pmv2.json": "software/infraestructura/grafana/dashboards/pmv2.json",
    "observability/grafana/provisioning/dashboards/pmv2.yml": "software/infraestructura/grafana/provisioning/dashboards/pmv2.yml",
    "observability/grafana/provisioning/datasources/prometheus.yml": "software/infraestructura/grafana/provisioning/datasources/prometheus.yml",
    "deployment/crear_paquete.py": "herramientas_IA/exportacion/crear_paquete.py",
    "deployment/exportar.ps1": "herramientas_IA/exportacion/exportar.ps1",
}

EXCLUDE_GLOBS = [
    ".env", "*/.env", ".env.local", "*/.env.local",  # .env.example sí se copia
    "*.pem", "*.key", "*.p12", "*.pfx", "kubeconfig", "*.kubeconfig",
    "*.exe", "*.jar", "*.class", "*.db", "*.sqlite", "*.sqlite3",
    "node_modules/*", "*/node_modules/*", ".m2/*", "target/*",
    "runs/*", "mlruns/*", "*/__pycache__/*", "*.pyc",
    "processed/dataset_green_ai_v2_hexagonal.csv",  # salida regenerable del ETL (11 MB)
    "2. Conocimiento de Ingenieria.md", "4. Gesti*n de Proyecto.md",  # originales docentes duplicados
    "*.docx", "*.pdf",
]


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          check=True, encoding="utf-8").stdout


def excluded(rel: str) -> bool:
    name = PurePosixPath(rel).name
    return any(fnmatch.fnmatch(rel, g) or fnmatch.fnmatch(name, g) for g in EXCLUDE_GLOBS)


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", type=Path, required=True)
    ap.add_argument("--dest", type=Path, default=Path("."))
    ap.add_argument("--only", default="")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    ws, dest = a.workspace.resolve(), a.dest.resolve()
    only = {x for x in a.only.split(",") if x}

    manifest: dict = {"units": {}, "root_files": {}}
    for unit, (repo_rel, sub, target) in UNITS.items():
        if only and unit not in only and unit.split("-datasets")[0] not in only:
            continue
        repo = ws / repo_rel
        files = git(repo, "-c", "core.quotepath=off", "ls-files", "-co", "--exclude-standard", "-z").split("\0")
        prefix = f"{sub}/" if sub else ""
        copied, skipped = [], []
        for rel in filter(None, files):
            if not rel.startswith(prefix):
                continue
            inner = rel[len(prefix):]
            if excluded(inner) or (repo / rel).is_dir():
                skipped.append(inner)
                continue
            out = dest / target / inner
            if not a.dry_run:
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(repo / rel, out)
            copied.append(inner)
        manifest["units"][unit] = {
            "source": repo_rel + (f"/{sub}" if sub else ""),
            "target": target,
            "branch": git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip(),
            "sha": git(repo, "rev-parse", "HEAD").strip(),
            "dirty_files": [ln for ln in git(repo, "status", "--porcelain").splitlines()],
            "copied": len(copied),
            "excluded": sorted(skipped),
        }
        print(f"{unit}: {len(copied)} copiados, {len(skipped)} excluidos -> {target}")

    if not only or "root" in only:
        root_sha = git(ws, "rev-parse", "HEAD").strip()
        for src, target in ROOT_FILES.items():
            sp = ws / src
            if not a.dry_run:
                (dest / target).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(sp, dest / target)
            manifest["root_files"][src] = {"target": target, "sha256": sha256(sp)}
        manifest["root_workspace_sha"] = root_sha
        print(f"root: {len(ROOT_FILES)} archivos de configuración")

    if not a.dry_run:
        mp = dest / "docs/migracion/manifiesto-copia.json"
        mp.parent.mkdir(parents=True, exist_ok=True)
        old = json.loads(mp.read_text(encoding="utf-8")) if mp.exists() else {"units": {}, "root_files": {}}
        old["units"].update(manifest["units"])
        old["root_files"].update(manifest["root_files"])
        if "root_workspace_sha" in manifest:
            old["root_workspace_sha"] = manifest["root_workspace_sha"]
        mp.write_text(json.dumps(old, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
