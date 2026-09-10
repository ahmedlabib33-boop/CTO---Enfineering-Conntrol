@echo off
setlocal EnableExtensions EnableDelayedExpansion
title Engineering CAD Platform - One Click Launcher
cd /d "%~dp0"
set "ROOT=%CD%"
set "LOG_DIR=%ROOT%\logs"
set "LOG_FILE=%LOG_DIR%\startup.log"
set "VENV=%ROOT%\.venv"
set "REQ=%ROOT%\requirements.txt"
set "REQ_HASH=%VENV%\.requirements.sha256"

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
echo =============================================================== >> "%LOG_FILE%"
echo [%DATE% %TIME%] Startup >> "%LOG_FILE%"

echo.
echo ===============================================================
echo  ENGINEERING CAD PLATFORM
echo  One-click environment setup and startup
echo ===============================================================
echo.

set "PY_CMD="
where py >nul 2>&1 && set "PY_CMD=py"
if not defined PY_CMD where python >nul 2>&1 && set "PY_CMD=python"
if not defined PY_CMD where python3 >nul 2>&1 && set "PY_CMD=python3"

if not defined PY_CMD (
  echo [ERROR] Python 3.11+ was not found.
  echo [%DATE% %TIME%] Python not found >> "%LOG_FILE%"
  goto :FAIL
)

%PY_CMD% -c "import sys; raise SystemExit(0 if sys.version_info >= (3,11) else 1)" >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Python 3.11 or newer is required.
  goto :FAIL
)

if not exist "%VENV%\Scripts\python.exe" (
  echo Creating .venv...
  %PY_CMD% -m venv "%VENV%" >> "%LOG_FILE%" 2>&1
  if errorlevel 1 goto :FAIL
)

set "VPY=%VENV%\Scripts\python.exe"

if not exist "%REQ%" (
  echo [ERROR] requirements.txt is missing.
  goto :FAIL
)

for /f "delims=" %%H in ('"%VPY%" -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path(r'%REQ%').read_bytes()).hexdigest())"') do set "CURRENT_HASH=%%H"
set "SAVED_HASH="
if exist "%REQ_HASH%" set /p SAVED_HASH=<"%REQ_HASH%"

if /I not "%CURRENT_HASH%"=="%SAVED_HASH%" (
  echo Installing/updating Python requirements...
  "%VPY%" -m pip install --upgrade pip setuptools wheel >> "%LOG_FILE%" 2>&1
  if errorlevel 1 goto :FAIL
  "%VPY%" -m pip install -r "%REQ%" >> "%LOG_FILE%" 2>&1
  if errorlevel 1 (
    echo [ERROR] Dependency installation failed. See logs\startup.log
    goto :FAIL
  )
  >"%REQ_HASH%" echo %CURRENT_HASH%
) else (
  echo Python requirements already synchronized.
)



rem ----------------------------------------------------------------
rem ML + mathematical intelligence requirements
rem ----------------------------------------------------------------
set "ML_REQ=%ROOT%\requirements-ml.txt"
set "ML_HASH=%VENV%\.requirements-ml.sha256"
if exist "%ML_REQ%" (
  for /f "delims=" %%H in ('"%VPY%" -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path(r'%ML_REQ%').read_bytes()).hexdigest())"') do set "CURRENT_ML_HASH=%%H"
  set "SAVED_ML_HASH="
  if exist "%ML_HASH%" set /p SAVED_ML_HASH=<"%ML_HASH%"
  if /I not "!CURRENT_ML_HASH!"=="!SAVED_ML_HASH!" (
    echo Installing/updating ML and mathematical intelligence pack...
    "%VPY%" -m pip install -r "%ML_REQ%" >> "%LOG_FILE%" 2>&1
    if errorlevel 1 (
      echo [ERROR] Mandatory ML/math dependency installation failed.
      echo See logs\startup.log
      goto :FAIL
    )
    >"%ML_HASH%" echo !CURRENT_ML_HASH!
  ) else (
    echo ML/math requirements already synchronized.
  )
)

rem Advanced ML/math capability pack: attempt automatically, never fake availability.
set "ADV_ML_REQ=%ROOT%\requirements-ml-advanced.txt"
set "ADV_ML_MARKER=%VENV%\.advanced-ml-attempted"
if exist "%ADV_ML_REQ%" if not exist "%ADV_ML_MARKER%" (
  echo Attempting advanced ML / optimization capability pack...
  "%VPY%" -m pip install -r "%ADV_ML_REQ%" >> "%LOG_FILE%" 2>&1
  if errorlevel 1 (
    echo [WARNING] Some advanced optional ML/math libraries are unavailable on this Python/Windows configuration.
    echo [WARNING] The app will report exact capability status at /ml/capabilities.
  )
  >"%ADV_ML_MARKER%" echo attempted
)

rem Heavy ML is attempted but platform-specific failures do not block core engineering functions.
set "HEAVY_REQ=%ROOT%\requirements-ml-heavy.txt"
set "HEAVY_MARKER=%VENV%\.heavy-ml-attempted"
if exist "%HEAVY_REQ%" if not exist "%HEAVY_MARKER%" (
  echo Attempting heavy ML / GNN / Bayesian / 3D capability pack...
  "%VPY%" -m pip install -r "%HEAVY_REQ%" >> "%LOG_FILE%" 2>&1
  if errorlevel 1 (
    echo [WARNING] Some heavy optional ML libraries could not be installed on this machine.
    echo [WARNING] Core ML/math remains available; see /ml/capabilities and startup.log.
  )
  >"%HEAVY_MARKER%" echo attempted
)

for %%D in (data uploads outputs exports temp logs cache projects backups) do (
  if not exist "%ROOT%\%%D" mkdir "%ROOT%\%%D"
)

if not exist "%ROOT%\.env" if exist "%ROOT%\.env.example" copy /Y "%ROOT%\.env.example" "%ROOT%\.env" >nul

for /f %%P in ('"%VPY%" -c "import socket; s=socket.socket(); s.bind(('127.0.0.1',0)); print(s.getsockname()[1]); s.close()"') do set "API_PORT=%%P"
for /f %%P in ('"%VPY%" -c "import socket; s=socket.socket(); s.bind(('127.0.0.1',0)); print(s.getsockname()[1]); s.close()"') do set "WEB_PORT=%%P"

echo Starting API on port %API_PORT%...
start "Engineering CAD API" /D "%ROOT%\apps\api" cmd /k ""%VPY%" -m uvicorn app.main:app --host 127.0.0.1 --port %API_PORT%"

echo Waiting for API...
set "API_OK=0"
for /L %%I in (1,1,45) do (
  powershell -NoProfile -Command "try{$r=Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 'http://127.0.0.1:%API_PORT%/health'; if($r.StatusCode -eq 200){exit 0}else{exit 1}}catch{exit 1}" >nul 2>&1
  if not errorlevel 1 (
    set "API_OK=1"
    goto :API_READY
  )
  timeout /t 1 /nobreak >nul
)
:API_READY
if "%API_OK%"=="0" (
  echo [ERROR] API health check failed.
  goto :FAIL
)

if exist "%ROOT%\apps\web\package.json" (
  where node >nul 2>&1
  if errorlevel 1 (
    echo [ERROR] Node.js LTS is required for the web UI.
    echo API is available at http://127.0.0.1:%API_PORT%/docs
    goto :FAIL
  )
  where npm >nul 2>&1
  if errorlevel 1 goto :FAIL

  pushd "%ROOT%\apps\web"
  if not exist "node_modules" (
    echo Installing frontend requirements...
    if exist "package-lock.json" (
      call npm ci >> "%LOG_FILE%" 2>&1
    ) else (
      call npm install >> "%LOG_FILE%" 2>&1
    )
    if errorlevel 1 (
      popd
      goto :FAIL
    )
  )
  echo Starting web UI on port %WEB_PORT%...
  start "Engineering CAD Web" /D "%ROOT%\apps\web" cmd /k "set NEXT_PUBLIC_API_URL=http://127.0.0.1:%API_PORT%&& npm run dev -- --port %WEB_PORT%"
  popd

  set "WEB_OK=0"
  for /L %%I in (1,1,60) do (
    powershell -NoProfile -Command "try{$r=Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 'http://127.0.0.1:%WEB_PORT%'; if($r.StatusCode -ge 200 -and $r.StatusCode -lt 500){exit 0}else{exit 1}}catch{exit 1}" >nul 2>&1
    if not errorlevel 1 (
      set "WEB_OK=1"
      goto :WEB_READY
    )
    timeout /t 1 /nobreak >nul
  )
  :WEB_READY
  if "%WEB_OK%"=="0" goto :FAIL
  start "" "http://127.0.0.1:%WEB_PORT%"
) else (
  start "" "http://127.0.0.1:%API_PORT%/docs"
)

echo.
echo Startup complete.
echo API: http://127.0.0.1:%API_PORT%
if exist "%ROOT%\apps\web\package.json" echo Web: http://127.0.0.1:%WEB_PORT%
exit /b 0

:FAIL
echo.
echo ===============================================================
echo STARTUP FAILED
echo Review: %LOG_FILE%
echo ===============================================================
pause
exit /b 1
