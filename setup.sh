#!/bin/bash

# Sessions Marketplace - Quick Setup Script
# This script automates the initial setup process

echo "🚀 Sessions Marketplace Backend Setup"
echo "======================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env file created. Please update it with your credentials."
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Ask for setup type
echo "Choose setup type:"
echo "1) Docker (Recommended)"
echo "2) Local Development"
read -p "Enter your choice (1 or 2): " setup_type

if [ "$setup_type" == "1" ]; then
    echo ""
    echo "🐳 Docker Setup"
    echo "==============="
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    echo "✅ Docker and Docker Compose are installed"
    echo ""
    
    # Build and start containers
    echo "🔨 Building and starting containers..."
    docker-compose up --build -d
    
    echo ""
    echo "⏳ Waiting for services to be ready..."
    sleep 10
    
    echo ""
    echo "✅ Setup complete!"
    echo ""
    echo "🌐 Services are running:"
    echo "   - API: http://localhost/api/"
    echo "   - Admin: http://localhost/admin/"
    echo "   - Swagger: http://localhost/swagger/"
    echo ""
    echo "🔑 Default admin credentials:"
    echo "   Username: admin"
    echo "   Password: admin123"
    echo ""
    echo "📊 View logs: docker-compose logs -f backend"
    echo "🛑 Stop services: docker-compose down"
    
elif [ "$setup_type" == "2" ]; then
    echo ""
    echo "💻 Local Development Setup"
    echo "=========================="
    
    # Check if Python is installed
    if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
        echo "❌ Python is not installed. Please install Python 3.11+ first."
        exit 1
    fi
    
    PYTHON_CMD=$(command -v python3 || command -v python)
    echo "✅ Python found: $PYTHON_CMD"
    echo ""
    
    # Create virtual environment
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    
    # Activate virtual environment
    echo "🔧 Activating virtual environment..."
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    # Install dependencies
    echo "📥 Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo ""
    echo "⚠️  Make sure PostgreSQL is running and configured in .env"
    read -p "Press Enter when PostgreSQL is ready..."
    
    # Run migrations
    echo "🗃️  Running migrations..."
    python manage.py makemigrations
    python manage.py migrate
    
    # Create superuser
    echo ""
    echo "👤 Create superuser account:"
    python manage.py createsuperuser
    
    # Collect static files
    echo ""
    echo "📁 Collecting static files..."
    python manage.py collectstatic --noinput
    
    echo ""
    echo "✅ Setup complete!"
    echo ""
    echo "🚀 Start the server:"
    echo "   python manage.py runserver"
    echo ""
    echo "🌐 The API will be available at:"
    echo "   - API: http://localhost:8000/api/"
    echo "   - Admin: http://localhost:8000/admin/"
    echo "   - Swagger: http://localhost:8000/swagger/"
    
else
    echo "❌ Invalid choice. Please run the script again."
    exit 1
fi

echo ""
echo "📖 For more information, see README.md"
echo "🎉 Happy coding!"
