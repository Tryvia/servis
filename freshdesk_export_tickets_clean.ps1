
$API_KEY = "YbOYtaCLmhZuvC9hqWUo"
$DOMAIN = "suportetryvia"  # sem o ".freshdesk.com"
$HEADERS = @{
    Authorization = ("Basic " + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$($API_KEY):x")))
}

$allTickets = @()
$page = 1
$maxPerPage = 100

do {
    $uri = "https://$DOMAIN.freshdesk.com/api/v2/tickets?page=$page&per_page=$maxPerPage"

    try {
        $response = Invoke-RestMethod -Uri $uri -Headers $HEADERS -Method Get

        if ($response.Count -eq 0) {
            break
        }
        if ($response.Count -lt $maxPerPage) {
            Write-Warning "Menos de $maxPerPage tickets retornados na página $page. Provavelmente chegou ao fim dos tickets."
            $allTickets += $response
            foreach ($ticket in $response) {
                Write-Output "Ticket puxado: $($ticket.id)"
            }
            Write-Output "Página ${page}: $($response.Count) tickets"
            break
        }

        $allTickets += $response
        foreach ($ticket in $response) {
            Write-Output "Ticket puxado: $($ticket.id)"
        }
        Write-Output "Página ${page}: $($response.Count) tickets"
        $page++

        Start-Sleep -Milliseconds 500  # evitar throttle
    }
    catch {
        Write-Error "Erro na página ${page}: $_"
        break
    }

} while ($true)

# Exportar para CSV
$allTickets | Select-Object id, subject, status, priority, created_at | Export-Csv -Path "tickets_exportados.csv" -NoTypeInformation
Write-Output "Exportação concluída. Total de tickets exportados: $($allTickets.Count)"