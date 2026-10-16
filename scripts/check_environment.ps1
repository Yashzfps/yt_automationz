Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Assert-Command($name) {
  if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
    throw "$name was not found in PATH."
  }
}

Assert-Command python
Assert-Command npm
Assert-Command ffmpeg
Assert-Command ffprobe

Push-Location "$PSScriptRoot/.."
try {
  if (-not (Test-Path ./.venv/Scripts/python.exe)) {
    throw 'Virtual environment missing. Run scripts/install.ps1 first.'
  }

  .\.venv\Scripts\python --version
  npm --version
  ffmpeg -version | Select-Object -First 1
  ffprobe -version | Select-Object -First 1

  Write-Host 'Environment checks passed.'
}
finally {
  Pop-Location
}
