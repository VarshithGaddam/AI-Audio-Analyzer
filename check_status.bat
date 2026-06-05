@echo off
echo ========================================
echo   AI Voice Analyzer - Status Check
echo ========================================
echo.

python test_backend.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ All systems operational!
    echo.
    echo 📝 Next steps:
    echo    1. Keep both terminals running
    echo    2. Open http://localhost:3000
    echo    3. Upload an audio file
    echo    4. View comprehensive analysis!
) else (
    echo.
    echo ❌ Backend not running!
    echo.
    echo 💡 Run: start.bat
)

echo.
pause
