# Actualiza el índice y los campos de un DOCX con Microsoft Word (sin aviso al abrirlo después)
# y, opcionalmente, guarda un PDF de vista previa.
# Uso: powershell -File herramientas_IA/exportacion/actualizar_word.ps1 -Docx <archivo.docx> [-Pdf <salida.pdf>]
param(
    [Parameter(Mandatory = $true)][string]$Docx,
    [string]$Pdf
)
$ErrorActionPreference = 'Stop'
$path = (Resolve-Path $Docx).Path
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($path, $false, $false)
    foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
    $doc.Fields.Update() | Out-Null
    foreach ($toc in $doc.TablesOfContents) { $toc.Update() }   # tras numerar páginas
    $doc.Save()
    if ($Pdf) { $doc.SaveAs2([ref]$Pdf, [ref]17) }
    $pages = $doc.ComputeStatistics(2)
    $doc.Close($false)
    "OK: $path ($pages páginas)"
} finally {
    $word.Quit()
}
