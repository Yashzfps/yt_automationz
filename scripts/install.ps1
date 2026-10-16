Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Host 'Installing backend dependencies...'
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  throw 'Python is not installed or not in PATH.'
}

Push-Location "$PSScriptRoot/.."
try {
  python -m venv .venv
  .\.venv\Scripts\python -m pip install --upgrade pip
  .\.venv\Scripts\pip install -e ./backend[dev]

  if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    throw 'Node.js/npm is not installed or not in PATH.'
  }

  Push-Location ./frontend
  try {
    npm install
  }
  finally {
    Pop-Location
  }

  Write-Host 'Installation complete.'
}
finally {
  Pop-Location
}
