# Episodio 3 del video: lo abre grabar_episodios.py en Windows Terminal. Muestra el comando, espera Enter,
# ejecuta la carga real (pide correo y contraseña con getpass) y enseña las primeras líneas del CSV.
$ErrorActionPreference = 'Continue'
$root = Resolve-Path (Join-Path $PSScriptRoot '..\..')
Set-Location $root
$csv = 'docs/evidencias/carga-video.csv'
# Letra grande para que la tabla se lea en el video (Ctrl + «+» del teclado numérico en Windows Terminal)
Start-Sleep -Milliseconds 1500
Add-Type -AssemblyName System.Windows.Forms
1..6 | ForEach-Object { [System.Windows.Forms.SendKeys]::SendWait('^{ADD}'); Start-Sleep -Milliseconds 150 }
Clear-Host
Write-Host 'Green AI - Episodio 3: pruebas con data masiva' -ForegroundColor Green
Write-Host ''
Write-Host 'python herramientas_IA/video/carga_transacciones.py --login --gateway https://green-ai-gateway-dev.onrender.com --iteraciones 200 --concurrencia 3 --out docs/evidencias/carga-video.csv' -ForegroundColor Yellow
Write-Host ''
Read-Host 'Pulsa Enter para ejecutar'
python herramientas_IA/video/carga_transacciones.py --login --gateway https://green-ai-gateway-dev.onrender.com --iteraciones 200 --concurrencia 3 --out $csv
$codigo = $LASTEXITCODE
Write-Host ''
Write-Host "Primeras lineas de $csv" -ForegroundColor Green
if (Test-Path $csv) { Get-Content $csv -TotalCount 6 }
Set-Content -Path (Join-Path $root '.tools/video/ep3-terminado.txt') -Value "codigo $codigo" -Encoding utf8
# Tiempo para leer la tabla; luego la ventana se cierra y queda Edge con Prometheus
Start-Sleep -Seconds 15
