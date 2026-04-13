$taskName = "Django_Balanca"
$scriptPath = "C:\Users\edson\Downloads\balanca\iniciar_balanca.bat"
$description = "Inicia o Django controle_etanol automaticamente"

$action = New-ScheduledTaskAction -Execute $scriptPath
$trigger = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "Tarefa antiga removida."
}

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Description $description -Force

Write-Host "Tarefa '$taskName' criada com sucesso!"
Write-Host "O Django iniciara automaticamente ao reiniciar o Windows."