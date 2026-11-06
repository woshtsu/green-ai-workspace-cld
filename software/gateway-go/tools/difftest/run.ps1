# Prueba diferencial Gateway Java vs Go contra los servicios reales del stack green-ai-mono.
# Requisitos: stack levantado (docker-compose.yml) e imágenes green-ai-mono-gateway y green-ai-mono-gateway-go:local.
# Uso (desde la raíz del monorepo): .\software\gateway-go\tools\difftest\run.ps1 [-Requests 2000]
param([int]$Requests = 2000, [string]$Network = 'green-ai-mono_default')
$ErrorActionPreference = 'Stop'
$src = (Resolve-Path "$PSScriptRoot\..\..").Path
$issuer = 'https://difftest.local/auth/v1'
$common = @('--network', $Network,
    '-e', 'GATEWAY_MONITORING_BASE_URL=http://monitoring:8080',
    '-e', 'GATEWAY_DATA_PROCESSING_BASE_URL=http://data-processing:8000',
    '-e', 'GATEWAY_PREDICTION_BASE_URL=http://prediction:8000',
    '-e', "GATEWAY_AUTH_ISSUER_URI=$issuer",
    '-e', 'GATEWAY_AUTH_JWK_SET_URI=http://gwdiff-issuer:9999/jwks',
    '-e', 'GATEWAY_CORS_ALLOWED_ORIGIN=http://127.0.0.1:13001')

function Cleanup { docker rm -f gwdiff-issuer gwdiff-java gwdiff-go 2>$null | Out-Null }
Cleanup
try {
    docker run -d --name gwdiff-issuer --network $Network -v "${src}:/src:ro" -w /src -e GOFLAGS=-buildvcs=false `
        -e GOCACHE=/tmp/gocache golang:1.25.14-alpine sleep infinity | Out-Null
    $startup = @{}
    foreach ($g in @(@{n = 'gwdiff-java'; img = 'green-ai-mono-gateway:latest'; p = 18091 },
                     @{n = 'gwdiff-go'; img = 'green-ai-mono-gateway-go:local'; p = 18092 })) {
        $t0 = Get-Date
        docker run -d --name $g.n -p "127.0.0.1:$($g.p):8081" @common $g.img | Out-Null
        while ($true) {
            try { if ((Invoke-WebRequest -UseBasicParsing "http://127.0.0.1:$($g.p)/actuator/health/liveness" -TimeoutSec 2).StatusCode -eq 200) { break } } catch {}
            if (((Get-Date) - $t0).TotalSeconds -gt 120) { throw "$($g.n) no arrancó" }
            Start-Sleep -Milliseconds 100
        }
        $startup[$g.n] = [math]::Round(((Get-Date) - $t0).TotalSeconds, 2)
    }
    "ARRANQUE hasta health 200 (s): java=$($startup['gwdiff-java']) go=$($startup['gwdiff-go'])"
    "MEMORIA en reposo: " + ((docker stats --no-stream --format '{{.Name}}={{.MemUsage}}' gwdiff-java gwdiff-go) -join '  ')
    $ErrorActionPreference = 'Continue'   # difftest sale con 1 si hay diferencias; el informe debe mostrarse igual
    docker exec gwdiff-issuer go run ./tools/difftest -java http://gwdiff-java:8081 -go http://gwdiff-go:8081 -listen :9999 -issuer $issuer -n $Requests 2>&1 | ForEach-Object { "$_" }
    $code = $LASTEXITCODE
    "MEMORIA tras carga: " + ((docker stats --no-stream --format '{{.Name}}={{.MemUsage}} CPU={{.CPUPerc}}' gwdiff-java gwdiff-go) -join '  ')
    "IMAGEN: " + ((docker images --format '{{.Repository}}:{{.Tag}}={{.Size}}' | Select-String 'green-ai-mono-gateway') -join '  ')
    exit $code
} finally { Cleanup }
