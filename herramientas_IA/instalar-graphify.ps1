# Instala Graphify en un entorno local del monorepo (.tools\graphify), sin tocar PATH ni el Python global.
# Requiere Python 3.10+ disponible como 'python' o 'py'. Reversión: borrar la carpeta .tools\graphify.
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$venv = Join-Path $root '.tools\graphify'
$version = '0.9.96'

if (-not (Test-Path (Join-Path $venv 'Scripts\python.exe'))) {
    python -m venv $venv
}
& (Join-Path $venv 'Scripts\python.exe') -m pip install --disable-pip-version-check "graphifyy==$version"
& (Join-Path $venv 'Scripts\graphify.exe') --version
