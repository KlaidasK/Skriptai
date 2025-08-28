param (
    [string]$Username  # (Pasirinktinai) Filtruoti tik vieno vartotojo procesus
)

# Dabartinė data ir laikas
$timestamp = Get-Date -Format "yyyy-MM-dd-HHmmss"

# Nustatoma, kur yra šis skriptas (naudojama, kad failai būtų kuriami šalia skripto)
$scriptDir = Split-Path -Parent $PSCommandPath

# Nustatomi "tikri" vartotojai, tie, kurie turi profilius kataloge C:\Users\

$realUsers = Get-CimInstance -ClassName Win32_UserProfile |
    Where-Object { $_.LocalPath -like "C:\Users\*" } |
    Select-Object -ExpandProperty LocalPath |
    ForEach-Object { ($_ -split '\\')[-1].ToLower() } |
    Where-Object { $_ -notin @("default", "public", "administrator", "defaultuser0") }


# Gaunami visi procesai su jų savininkais
$allProcesses = Get-WmiObject Win32_Process | ForEach-Object {
    try {
        $ownerInfo = $_.GetOwner()  # Bandoma gauti proceso savininką
        $rawUser = if ($ownerInfo.User) { $ownerInfo.User.ToLower() } else { "no_user" }

        # Jei savininkas yra tarp tikrų vartotojų – laikom jį realiu, kitaip priskiriam prie "no_user"
        $user = if ($realUsers -contains $rawUser) { $rawUser } else { "no_user" }

        # Sukuriamas objektas su reikalinga informacija apie procesą
        [PSCustomObject]@{
            Name   = $_.Name
            PID    = $_.ProcessId
            User   = $user
            Param1 = $_.CreationDate
            Param2 = $_.ExecutablePath
        }
    } catch {
        # Jei nepavyksta gauti savininko – priskiriam prie "no_user"
        [PSCustomObject]@{
            Name   = $_.Name
            PID    = $_.ProcessId
            User   = "no_user"
            Param1 = $_.CreationDate
            Param2 = $_.ExecutablePath
        }
    }
}


# Jei nurodytas konkretus vartotojo vardas, filtruojam tik jį, kitaip visus rastus
if ($null -ne $Username -and $Username.Trim() -ne "") {
    $users = @($Username.ToLower())
    Write-Host "Filtering processes for user: $($users -join ', ')"
} else {
    $users = $allProcesses.User | Sort-Object -Unique
    Write-Host "Found users: $($users -join ', ')"
}

$notepadProcesses = @()


# Sukuriami log failai kiekvienam vartotojui
foreach ($user in $users) {
    # Filtruojami procesai pagal vartotoją
    $userProcs = $allProcesses | Where-Object { $_.User -eq $user }

    # Jei procesų nerasta – praleidžiam
    if ($userProcs.Count -eq 0) {
        Write-Host "No processes found for user: $user"
        continue
    }

    $logPath = Join-Path $scriptDir "$user-process-log-$timestamp.txt"

    # Pridedam datą, laiką ir antraštę į failą
    Add-Content $logPath "Date: $(Get-Date -Format 'yyyy-MM-dd')"
    Add-Content $logPath "Time: $(Get-Date -Format 'HH:mm:ss')"
    Add-Content $logPath "`n--- Process List for $user ---`n"

    # Įrašomi visi proceso duomenys į failą
    foreach ($proc in $userProcs) {
        Add-Content $logPath "Name: $($proc.Name)"
        Add-Content $logPath "PID: $($proc.PID)"
        Add-Content $logPath "Param1 (CreationDate): $($proc.Param1)"
        Add-Content $logPath "Param2 (CommandLine): $($proc.Param2)"
        Add-Content $logPath "------------------------------"
    }

    # Atidaromas log failas su Notepad
    $np = Start-Process notepad.exe -ArgumentList $logPath -PassThru
    $notepadProcesses += $np
}

# Pranešimas apie sukurtus log failus
Write-Host "`nLog files created for users: $($users -join ', ')"

Read-Host "`nNotepad logs open. Press Enter to close them..."


# Uždaro visus atidarytus Notepad langus (kurie buvo paleisti šio skripto)
foreach ($np in $notepadProcesses) {
    try {
        $np.CloseMainWindow() | Out-Null
        Start-Sleep -Seconds 1
        if (-not $np.HasExited) {
            $np | Stop-Process
        }
    } catch {
        Write-Host "Could not close notepad PID $($np.Id)"
    }
}

# Pabaiga
Write-Host "`nScript completed."
