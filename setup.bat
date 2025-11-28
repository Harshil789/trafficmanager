@echo off
REM Setup script for Windows

echo 🚀 Smart Traffic Monitoring System - Setup
echo ==================================================

REM Create virtual environment
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment exists
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Create .env if missing
if not exist ".env" (
    echo 📝 Creating .env file...
    (
        echo # Auto-generated .env file
        echo DATABASE_URL=sqlite:///traffic_monitoring.db
        echo SESSION_SECRET=dev_secret_key_change_in_production
    ) > .env
    echo ✓ .env file created (SQLite for local development)
) else (
    echo ✓ .env file exists
)

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt
echo ✓ Dependencies installed

echo ==================================================
echo ✅ Setup complete!
echo.
echo Virtual environment is activated. To run the app:
echo    python main.py
echo.
echo Then open http://localhost:5000 in your browser
