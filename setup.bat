@echo off
REM Setup script for big-data project
REM Works on Windows

echo Setting up big-data project...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed. Please install Python first.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install required packages
echo Installing dependencies...
pip install pandas scikit-learn jupyter matplotlib seaborn numpy scipy plotly umap-learn

echo Setup complete!
echo.
echo To activate the virtual environment manually, run:
echo .venv\Scripts\activate.bat
echo.
echo To start Jupyter notebook, run:
echo jupyter notebook
pause