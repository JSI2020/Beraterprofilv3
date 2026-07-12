$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

Write-Host ""
Write-Host "  =========================================" -ForegroundColor Cyan
Write-Host "  ORBIT Beraterprofil Generator  ** V3 **" -ForegroundColor Cyan
Write-Host "  =========================================" -ForegroundColor Cyan
Write-Host "  Folder: $ProjectRoot" -ForegroundColor DarkGray
Write-Host ""

if (-not (Test-Path "$ProjectRoot\streamlit_app.py")) {
    Write-Host "  ERROR: streamlit_app.py not found." -ForegroundColor Red
    Write-Host "  You are in the wrong folder. Use Beratorprofilv3, NOT Beratorprofilv2." -ForegroundColor Red
    exit 1
}

if (Test-Path "$ProjectRoot\src\web\pipeline.py") {
    Write-Host "  ERROR: This looks like Beratorprofilv2 (src\web\pipeline.py found)." -ForegroundColor Red
    Write-Host "  Please run from: C:\Personal\Agentic AI\Beratorprofilv3" -ForegroundColor Red
    exit 1
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "  ERROR: Python not found." -ForegroundColor Red
    exit 1
}

Write-Host "  [1/3] Stopping old server on port 8501..." -ForegroundColor DarkGray
$lines = netstat -ano | Select-String ":8501.*LISTENING"
foreach ($line in $lines) {
    $procId = ($line -split '\s+')[-1]
    if ($procId -match '^\d+$') { taskkill /F /PID $procId 2>$null | Out-Null }
}

Write-Host "  [2/3] Installing dependencies..." -ForegroundColor DarkGray
pip install -q streamlit pyyaml python-dotenv 2>$null

Write-Host "  [3/3] Starting Streamlit on http://localhost:8501" -ForegroundColor Green
Write-Host "        Entry: streamlit_app.py (ui.pipeline, not src.web.pipeline)" -ForegroundColor Yellow
Write-Host ""

$env:PYTHONDONTWRITEBYTECODE = "1"
python -m streamlit run streamlit_app.py --server.port 8501 --server.address 127.0.0.1 --server.headless true
