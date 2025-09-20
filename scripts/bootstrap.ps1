[CmdletBinding()]
param()

$Root = Split-Path -Parent $PSScriptRoot

Write-Host "==> Installing backend dependencies" -ForegroundColor Cyan
if (Get-Command uv -ErrorAction SilentlyContinue) {
  Push-Location (Join-Path $Root "backend")
  try {
    uv pip install -e ".[dev]"
  } finally {
    Pop-Location
  }
} else {
  Write-Warning "uv not found. Install it from https://github.com/astral-sh/uv or run the commands manually:" 
  Write-Host "  cd backend" 
  Write-Host "  python -m venv .venv" 
  Write-Host "  .\\.venv\\Scripts\\Activate.ps1" 
  Write-Host "  pip install -e .[dev]"
}

Write-Host "==> Installing frontend dependencies" -ForegroundColor Cyan
if (Get-Command pnpm -ErrorAction SilentlyContinue) {
  Push-Location (Join-Path $Root "frontend")
  try {
    pnpm install
  } finally {
    Pop-Location
  }
} elseif (Get-Command npm -ErrorAction SilentlyContinue) {
  Push-Location (Join-Path $Root "frontend")
  try {
    npm install
  } finally {
    Pop-Location
  }
} else {
  Write-Warning "Neither pnpm nor npm found. Install Node.js 20+ to continue."
}
