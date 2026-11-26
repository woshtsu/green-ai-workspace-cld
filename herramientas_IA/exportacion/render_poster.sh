#!/usr/bin/env bash
# Exporta el póster (HTML) a PDF A1 y PNG con Edge headless. Ejecutar desde Git Bash.
set -e
R=$(cd "$(dirname "$0")/../.." && pwd -W)
S=$(cygpath -m -l "$(mktemp -d)")
E="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
[ -f "$E" ] || E="/c/Program Files/Microsoft/Edge/Application/msedge.exe"
U="file:///$R/entregables/semana15/poster/poster-green-ai.html"
"$E" --headless=new --disable-gpu --user-data-dir="$S" --hide-scrollbars --force-device-scale-factor=1 --window-size=2384,3370 --screenshot="$R/exportados/semana15/poster-green-ai.png" "$U"
"$E" --headless=new --disable-gpu --user-data-dir="$S" --no-pdf-header-footer --print-to-pdf="$R/exportados/semana15/poster-green-ai.pdf" "$U"
echo "Revisar: exportados/semana15/poster-green-ai.pdf (debe ser 1 página) y el .png"
