@echo off
echo Setting up Luxury E-Commerce for Windows...
echo.

:: Create virtual environment
echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Failed to create virtual environment. Make sure Python is installed.
    pause
    exit /b
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install requirements
echo Installing requirements...
pip install -r requirements.txt

:: Fix Flask-Login issue
echo Patching Flask-Login for compatibility...
python fix_flask_login.py

echo.
echo Setup complete!
echo To run the application:
echo 1. venv\Scripts\activate
echo 2. python run.py
echo.
pause
