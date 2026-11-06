$ErrorActionPreference = 'Stop'
$workspace = Split-Path $PSScriptRoot -Parent
Push-Location $workspace
try {
    python deployment/crear_paquete.py
    if ($LASTEXITCODE -ne 0) { throw 'Error generando configuracion' }
    docker compose build
    if ($LASTEXITCODE -ne 0) { throw 'Error construyendo imagenes' }
    docker pull grafana/grafana:12.4.11
    if ($LASTEXITCODE -ne 0) { throw 'Error descargando Grafana' }
    docker pull prom/prometheus:v3.13.3
    if ($LASTEXITCODE -ne 0) { throw 'Error descargando Prometheus' }
    $packageImages = @()
    foreach ($serviceName in @('simulator','monitoring','data-processing','prediction','gateway','frontend')) {
        $imageTag = "green-ai-portable/${serviceName}:2026-10-21"
        docker tag "green-ai-workspace-${serviceName}:latest" $imageTag
        if ($LASTEXITCODE -ne 0) { throw "Error etiquetando $serviceName" }
        $packageImages += $imageTag
    }
    $packageImages += @('prom/prometheus:v3.13.3','grafana/grafana:12.4.11')
    docker image inspect --format '{{.Id}} {{.Os}}/{{.Architecture}} {{join .RepoTags ","}}' @packageImages | Set-Content output/green-ai-portable/imagenes-manifest.txt
    docker save -o output/green-ai-portable/imagenes.tar @packageImages
    if ($LASTEXITCODE -ne 0) { throw 'Error exportando TAR' }
    (Get-FileHash output/green-ai-portable/imagenes.tar -Algorithm SHA256).Hash | Set-Content output/green-ai-portable/imagenes.tar.sha256
} finally { Pop-Location }
