param(
    [Parameter(Mandatory=$true)]
    [string]$CfEmpresa
)

$API_KEY = "YbOYtaCLmhZuvC9hqWUo"
$DOMAIN = "suportetryvia"  # sem o ".freshdesk.com"
$HEADERS = @{
    Authorization = ("Basic " + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$($API_KEY):x")))
}

$allTickets = @()
$page = 1
$maxPerPage = 100

Write-Output "Buscando tickets para a empresa (cf_empresa): $CfEmpresa"

do {
    $uri = "https://$DOMAIN.freshdesk.com/api/v2/tickets?page=$page&per_page=$maxPerPage"

    try {
        $response = Invoke-RestMethod -Uri $uri -Headers $HEADERS -Method Get

        if ($response.Count -eq 0) {
            break
        }

        # Filtrar tickets pelo campo customizado cf_empresa
        $empresaTickets = $response | Where-Object { 
            $_.custom_fields -and $_.custom_fields.cf_empresa -eq $CfEmpresa
        }

        if ($empresaTickets.Count -gt 0) {
            $allTickets += $empresaTickets
            Write-Output "Página ${page}: Encontrados $($empresaTickets.Count) tickets para a empresa $CfEmpresa"
        } else {
            Write-Output "Página ${page}: Nenhum ticket encontrado para a empresa $CfEmpresa"
        }

        if ($response.Count -lt $maxPerPage) {
            Write-Output "Menos de $maxPerPage tickets retornados na página $page. Chegou ao fim dos tickets."
            break
        }

        $page++
        Start-Sleep -Milliseconds 500  # evitar throttle
    }
    catch {
        Write-Error "Erro na página ${page}: $_"
        break
    }

} while ($true)

# Criar nome de arquivo seguro
$safeFileName = $CfEmpresa -replace " ", "_" -replace "/", "_" -replace "\\", "_"
$outputFile = "tickets_empresa_$safeFileName.json"

# Exportar para JSON
$allTickets | ConvertTo-Json -Depth 100 | Set-Content -Path $outputFile -Encoding UTF8
Write-Output "Exportação concluída. Total de tickets exportados para empresa $CfEmpresa : $($allTickets.Count)"
Write-Output "Arquivo salvo como: $outputFile"

