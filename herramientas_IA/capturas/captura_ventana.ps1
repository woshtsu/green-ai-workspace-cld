<#
Captura REAL de una ventana de consola de Windows (conhost) ejecutando un comando en esta máquina.
Abre la consola, ejecuta el comando, espera a que termine, captura la ventana con PrintWindow y la cierra.
La ventana aparece unos segundos en pantalla. El resultado es una captura de pantalla, no un render.

Uso:
  powershell -File herramientas_IA/capturas/captura_ventana.ps1 -Comando "cd software/frontend; node --test tests/*.test.cjs" -Salida ruta.png [-Titulo "..."] [-Columnas 120] [-Filas 34] [-TimeoutSeg 600]
#>
param(
  [Parameter(Mandatory=$true)][string]$Comando,
  [Parameter(Mandatory=$true)][string]$Salida,
  [string]$Titulo = "Green AI - evidencia",
  [int]$Columnas = 120,
  [int]$Filas = 34,
  [int]$TimeoutSeg = 600
)
$ErrorActionPreference = "Stop"
$repo = (Resolve-Path "$PSScriptRoot\..\..").Path
$marca = Join-Path $env:TEMP ("captura_fin_" + [guid]::NewGuid().ToString("N") + ".txt")
$salidaAbs = [IO.Path]::GetFullPath((Join-Path $repo $Salida))

Add-Type -AssemblyName System.Drawing
Add-Type @"
using System; using System.Runtime.InteropServices;
public static class Win {
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L, T, R, B; }
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint f);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
}
"@

$fecha = Get-Date -Format "dd/MM/yyyy HH:mm"
$script = @"
`$host.UI.RawUI.WindowTitle = '$Titulo - $fecha';
try { `$host.UI.RawUI.BufferSize = New-Object Management.Automation.Host.Size($Columnas, 3000); `$host.UI.RawUI.WindowSize = New-Object Management.Automation.Host.Size($Columnas, $Filas) } catch {}
chcp 65001 > `$null; [Console]::OutputEncoding = [Text.Encoding]::UTF8; `$OutputEncoding = [Text.Encoding]::UTF8;
Set-Location '$repo';
Write-Host ('PS ' + (Get-Location).Path + '> $($Comando.Replace("'","''"))') -ForegroundColor Yellow;
$Comando
Write-Host '';
Set-Content -Path '$marca' -Value 'fin'
"@
$enc = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($script))
$p = Start-Process conhost.exe -ArgumentList "powershell.exe -NoExit -NoProfile -EncodedCommand $enc" -PassThru

$t0 = Get-Date
while (-not (Test-Path $marca)) {
  if (((Get-Date) - $t0).TotalSeconds -gt $TimeoutSeg) { Stop-Process -Id $p.Id -Force; throw "Tiempo agotado" }
  Start-Sleep -Milliseconds 500
}
Start-Sleep -Milliseconds 800
# En Windows 11 la consola puede pertenecer a otro proceso (p. ej. Windows Terminal): se busca por título.
$h = [IntPtr]::Zero; $dueno = $null
for ($i = 0; $i -lt 20 -and $h -eq [IntPtr]::Zero; $i++) {
  $dueno = Get-Process | Where-Object { $_.MainWindowTitle -like "$Titulo - $fecha*" } | Select-Object -First 1
  if ($dueno) { $h = $dueno.MainWindowHandle } else { Start-Sleep -Milliseconds 300 }
}
if ($h -eq [IntPtr]::Zero) { Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue; throw "Sin ventana" }
[Win]::SetForegroundWindow($h) | Out-Null; Start-Sleep -Milliseconds 400
$r = New-Object Win+RECT; [Win]::GetWindowRect($h, [ref]$r) | Out-Null
$bmp = New-Object Drawing.Bitmap ($r.R - $r.L), ($r.B - $r.T)
$g = [Drawing.Graphics]::FromImage($bmp); $hdc = $g.GetHdc()
[Win]::PrintWindow($h, $hdc, 2) | Out-Null
$g.ReleaseHdc($hdc); $g.Dispose()
New-Item -ItemType Directory -Force -Path (Split-Path $salidaAbs) | Out-Null
$bmp.Save($salidaAbs, [Drawing.Imaging.ImageFormat]::Png); $bmp.Dispose()
Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
if ($dueno -and $dueno.ProcessName -ne "WindowsTerminal") { Stop-Process -Id $dueno.Id -Force -ErrorAction SilentlyContinue }
Remove-Item $marca -ErrorAction SilentlyContinue
"OK $salidaAbs"
