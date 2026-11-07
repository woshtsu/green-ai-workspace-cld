# Retira el workspace antiguo: COPIA el monorepo fuera, verifica Git, instala Graphify y (con confirmacion) borra el workspace.
# Cerrar antes Claude, terminales y editores. Ejecutar:
#   powershell -ExecutionPolicy Bypass -File C:\Practicas\202620\TallerProyectos\green-ai-workspace\green-ai-monorepo\herramientas_IA\retirar-workspace.ps1
$ErrorActionPreference = 'Stop'
$workspace = 'C:\Practicas\202620\TallerProyectos\green-ai-workspace'
$destino   = 'C:\Practicas\202620\TallerProyectos\green-ai'
$origen    = Join-Path $workspace 'green-ai-monorepo'
Set-Location 'C:\Practicas\202620\TallerProyectos'

# 1. Quitar una copia anterior incompleta
if (Test-Path $destino) {
    Write-Host "Borrando copia anterior $destino ..."
    Remove-Item $destino -Recurse -Force -Confirm:$false
}

# 2. Copiar todo, incluidos ocultos (.git) y archivos ignorados (.env, config.local.js)
robocopy $origen $destino /E /COPY:DAT /A-:SH /R:1 /W:1 /NFL /NDL /NJH /NP
if ($LASTEXITCODE -ge 8) { throw "robocopy fallo (codigo $LASTEXITCODE). El original sigue intacto." }

# 3. Verificar que la copia es el mismo repositorio
$a = git -C $origen rev-parse HEAD
$b = git -C $destino rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or $a -ne $b) { throw "La copia no es un repositorio Git valido. El original sigue intacto." }
git -C $destino worktree prune
git -C $destino status -sb | Select-Object -First 1
Write-Host "Copia verificada: HEAD $b"

# 4. Graphify local en el monorepo copiado
Set-Location $destino
& .\herramientas_IA\instalar-graphify.ps1

# 5. Borrado irreversible del workspace antiguo (incluye el original y las carpetas -wt-*)
Set-Location 'C:\Practicas\202620\TallerProyectos'
$r = Read-Host "Escribe BORRAR para eliminar $workspace (la copia ya esta verificada)"
if ($r -ceq 'BORRAR') {
    Remove-Item $workspace -Recurse -Force -Confirm:$false
    git -C $destino worktree prune
    Write-Host 'Workspace antiguo eliminado.'
} else { Write-Host 'Workspace conservado.' }
Write-Host "Monorepo en $destino. Abre esa carpeta en Claude."
