@echo off
echo ========================================
echo   AI Voice Analyzer - Setup
echo ========================================
echo.

echo [1/3] Installing Python dependencies...
pip install -r requirements.txt

echo.
echo [2/3] Installing Node.js dependencies...
cd frontend
call npm install

cd ..

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo To start the application:
echo   1. Run: start.bat
echo   2. Open browser: http://localhost:3000
echo.
pause
