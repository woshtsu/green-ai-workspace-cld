<#
Mide el arranque en frío (cold start) de los servicios de Render: primera petición tras inactividad
y segunda petición inmediata, con curl. Solo GET a rutas de salud públicas; sin tokens ni datos.
Uso: powershell -File herramientas_IA/operacion/medir_arranque_frio.ps1
#>
$servicios = [ordered]@{
  "gateway"         = "https://green-ai-gateway-dev.onrender.com/actuator/health"
  "monitoring"      = "https://green-ai-monitoring-dev.onrender.com/actuator/health"
  "prediction"      = "https://green-ai-prediction-dev-zxly.onrender.com/health/ready"
  "data-processing" = "https://green-ai-data-processing-dev.onrender.com/api/v1/health"
  "simulator"       = "https://green-ai-simulator-dev.onrender.com/health"
  "prometheus"      = "https://green-ai-prometheus-dev.onrender.com/-/healthy"
}
$fmt = "%{http_code} %{time_total}"
Write-Host ("{0,-16} {1,-22} {2,-22}" -f "servicio", "1.a peticion (HTTP s)", "2.a peticion (HTTP s)")
foreach ($k in $servicios.Keys) {
  $u = $servicios[$k]
  $a = curl.exe -s -o NUL -m 120 -w $fmt $u
  $b = curl.exe -s -o NUL -m 120 -w $fmt $u
  Write-Host ("{0,-16} {1,-22} {2,-22}" -f $k, $a, $b)
}
Write-Host ("Medido: " + (Get-Date -Format "dd/MM/yyyy HH:mm:ss") + " (hora de Lima)")
