@echo off
echo ========================================
echo   AI Voice Analyzer - Starting...
echo ========================================
echo.

echo Starting FastAPI Backend...
start cmd /k "cd backend && python api.py"

timeout /t 3 /nobreak > nul

echo.
echo Starting React Frontend...
start cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo   Application Starting!
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit this window...
pause > nul
