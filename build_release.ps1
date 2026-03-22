$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$packagingScript = Join-Path $projectRoot 'packaging\build.ps1'

if (-not (Test-Path $packagingScript)) {
    throw "Build script not found: $packagingScript"
}

& powershell -ExecutionPolicy Bypass -File $packagingScript