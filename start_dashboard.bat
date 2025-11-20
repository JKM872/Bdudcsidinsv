@echo off
echo ========================================
echo Starting Sports Prediction Dashboard
echo ========================================
echo.

echo [1/2] Starting Backend API (Port 5000)...
start "Dashboard API" cmd /k "cd /d c:\Users\jakub\Desktop\BigOne && python api/app.py"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend (Port 3000)...
start "Dashboard Frontend" cmd /k "cd /d c:\Users\jakub\Desktop\BigOne\dashboard && npm run dev"

echo.
echo ========================================
echo Dashboard is starting...
echo ========================================
echo Backend API:  http://localhost:5000
echo Frontend:     http://localhost:3000
echo ========================================
echo.
echo Waiting for servers to initialize...
timeout /t 8 /nobreak >nul

echo Opening dashboard in browser...
start http://localhost:3000

echo.
echo Dashboard launched successfully!
echo Press any key to close this window (servers will continue running)
pause >nul
