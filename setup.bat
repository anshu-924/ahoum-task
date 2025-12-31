@echo off
REM Sessions Marketplace - Quick Setup Script for Windows
REM This script automates the initial setup process

echo ========================================
echo Sessions Marketplace Backend Setup
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo .env file created. Please update it with your credentials.
    echo.
) else (
    echo .env file already exists
    echo.
)

REM Ask for setup type
echo Choose setup type:
echo 1^) Docker ^(Recommended^)
echo 2^) Local Development
set /p setup_type="Enter your choice (1 or 2): "

if "%setup_type%"=="1" (
    echo.
    echo ========================================
    echo Docker Setup
    echo ========================================
    
    REM Check if Docker is installed
    docker --version >nul 2>&1
    if errorlevel 1 (
        echo Docker is not installed. Please install Docker first.
        pause
        exit /b 1
    )
    
    docker-compose --version >nul 2>&1
    if errorlevel 1 (
        echo Docker Compose is not installed. Please install Docker Compose first.
        pause
        exit /b 1
    )
    
    echo Docker and Docker Compose are installed
    echo.
    
    REM Build and start containers
    echo Building and starting containers...
    docker-compose up --build -d
    
    echo.
    echo Waiting for services to be ready...
    timeout /t 10 /nobreak >nul
    
    echo.
    echo ========================================
    echo Setup complete!
    echo ========================================
    echo.
    echo Services are running:
    echo    - API: http://localhost/api/
    echo    - Admin: http://localhost/admin/
    echo    - Swagger: http://localhost/swagger/
    echo.
    echo Default admin credentials:
    echo    Username: admin
    echo    Password: admin123
    echo.
    echo View logs: docker-compose logs -f backend
    echo Stop services: docker-compose down
    
) else if "%setup_type%"=="2" (
    echo.
    echo ========================================
    echo Local Development Setup
    echo ========================================
    
    REM Check if Python is installed
    python --version >nul 2>&1
    if errorlevel 1 (
        echo Python is not installed. Please install Python 3.11+ first.
        pause
        exit /b 1
    )
    
    echo Python is installed
    echo.
    
    REM Create virtual environment
    echo Creating virtual environment...
    python -m venv venv
    
    REM Activate virtual environment
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    
    REM Install dependencies
    echo Installing dependencies...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    
    echo.
    echo Make sure PostgreSQL is running and configured in .env
    pause
    
    REM Run migrations
    echo Running migrations...
    python manage.py makemigrations
    python manage.py migrate
    
    REM Create superuser
    echo.
    echo Create superuser account:
    python manage.py createsuperuser
    
    REM Collect static files
    echo.
    echo Collecting static files...
    python manage.py collectstatic --noinput
    
    echo.
    echo ========================================
    echo Setup complete!
    echo ========================================
    echo.
    echo Start the server:
    echo    python manage.py runserver
    echo.
    echo The API will be available at:
    echo    - API: http://localhost:8000/api/
    echo    - Admin: http://localhost:8000/admin/
    echo    - Swagger: http://localhost:8000/swagger/
    
) else (
    echo Invalid choice. Please run the script again.
    pause
    exit /b 1
)

echo.
echo For more information, see README.md
echo Happy coding!
echo.
pause
