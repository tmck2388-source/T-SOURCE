#!/bin/bash
# Quick OttA setup for PowerShell (Windows)

Write-Host "🚀 OttA Windows Setup" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan

# Check Python
Write-Host "[1/3] Checking Python..." -ForegroundColor Yellow
python --version

# Create virtual environment (optional)
if (-Not (Test-Path "venv")) {
    Write-Host "[2/3] Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    .\venv\Scripts\Activate.ps1
} else {
    Write-Host "[2/3] Activating virtual environment..." -ForegroundColor Yellow
    .\venv\Scripts\Activate.ps1
}

# Install dependencies
Write-Host "[3/3] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "Run: python main.py" -ForegroundColor Cyan
