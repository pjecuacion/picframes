$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$distDir = Join-Path $projectRoot 'dist'
$specFile = Join-Path $PSScriptRoot 'MyApp.spec'  # TODO: rename when you rename the spec file
$issScript = Join-Path $PSScriptRoot 'installer.iss'

function Find-InnoSetupCompiler {
    $candidates = @(
        (Get-Command 'ISCC.exe' -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue),
        'C:\Program Files (x86)\Inno Setup 6\ISCC.exe',
        'C:\Program Files\Inno Setup 6\ISCC.exe'
    ) | Where-Object { $_ }

    foreach ($candidate in $candidates) {
        if (Test-Path $candidate) {
            return $candidate
        }
    }

    return $null
}

Push-Location $projectRoot
try {
    $python = Join-Path $projectRoot '.venv\Scripts\python.exe'
    if (-not (Test-Path $python)) {
        throw 'Expected virtual environment Python at .venv\Scripts\python.exe'
    }

    & $python -m PyInstaller --noconfirm --clean $specFile

    $iscc = Find-InnoSetupCompiler
    if ($null -eq $iscc) {
        Write-Warning 'PyInstaller build completed, but ISCC.exe was not found. Install Inno Setup 6 to generate the installer.'
        return
    }

    & $iscc "/DProjectRoot=$projectRoot" "/DDistDir=$distDir" $issScript
}
finally {
    Pop-Location
}