Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Push-Location "$PSScriptRoot/.."
try {
  if (-not (Test-Path ./.venv/Scripts/python.exe)) {
    throw 'Virtual environment missing. Run scripts/install.ps1 first.'
  }

  $backend = Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "-m","uvicorn","app.main:app","--app-dir","backend","--host","127.0.0.1","--port","8787" -PassThru
  Write-Host "Backend started with PID $($backend.Id)"

  Push-Location ./frontend
  try {
    npm run dev -- --host 127.0.0.1 --port 5173
  }
  finally {
    Pop-Location
  }
}
finally {
  Pop-Location
}
