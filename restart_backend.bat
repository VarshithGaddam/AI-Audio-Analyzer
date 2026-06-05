@echo off
echo ========================================
echo   Restarting Backend...
echo ========================================
echo.

echo Finding backend process...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Stopping process %%a
    taskkill /F /PID %%a 2>nul
)

timeout /t 2 /nobreak > nul

echo Starting backend...
cd backend
start cmd /k "python api.py"

echo.
echo ✅ Backend restarted!
echo    API: http://localhost:8000
echo.
pause
