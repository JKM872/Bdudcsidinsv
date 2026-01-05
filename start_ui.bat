@echo off
REM ============================================
REM BigOne UI Starter
REM Uruchamia API Server + Frontend jednocześnie
REM ============================================

echo.
echo ============================================
echo    BigOne UI Starter
echo ============================================
echo.

REM Sprawdź czy Python jest dostępny
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python nie jest zainstalowany lub nie jest w PATH
    pause
    exit /b 1
)

REM Sprawdź czy Node.js jest dostępny
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js nie jest zainstalowany lub nie jest w PATH
    pause
    exit /b 1
)

echo [INFO] Uruchamiam API Server na porcie 5000...
start "BigOne API Server" cmd /c "python api_server.py"

REM Poczekaj chwilę na uruchomienie API
timeout /t 3 /nobreak >nul

echo [INFO] Uruchamiam Frontend na porcie 5173...
cd frontend
start "BigOne Frontend" cmd /c "npm run dev"
cd ..

echo.
echo ============================================
echo    Serwery uruchomione!
echo ============================================
echo.
echo    API Server:  http://localhost:5000
echo    Frontend:    http://localhost:5173
echo.
echo    Aby zatrzymac, zamknij okna terminali.
echo ============================================
echo.

REM Otwórz przeglądarkę po 5 sekundach
timeout /t 5 /nobreak >nul
start http://localhost:5173

pause

