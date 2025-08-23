#!/bin/bash

# Odoo Catering Management System - Startup Script
# This script helps you get started with the development environment

echo "🍽️  Odoo Catering Management System Setup"
echo "=========================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists docker; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command_exists docker-compose; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Check if containers are already running
if docker-compose ps | grep -q "Up"; then
    echo "🟡 Containers are already running."
    echo "📊 Current status:"
    docker-compose ps
    echo ""
    read -p "Do you want to restart the services? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🔄 Restarting services..."
        docker-compose down
        docker-compose up -d
    fi
else
    echo "🚀 Starting Odoo Catering Management System..."
    docker-compose up -d
fi

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Services started successfully!"
    echo ""
    echo "🌐 Access URLs:"
    echo "   📱 Odoo Application: http://localhost:8069"
    echo "   🗄️  pgAdmin (Database): http://localhost:8080"
    echo ""
    echo "🔑 Login Credentials:"
    echo "   Odoo Database Setup:"
    echo "   - Master Password: admin"
    echo "   - Database Name: catering_db (suggested)"
    echo ""
    echo "   pgAdmin:"
    echo "   - Email: admin@catering.local"
    echo "   - Password: admin123"
    echo ""
    echo "📝 Next Steps:"
    echo "   1. Open http://localhost:8069 in your browser"
    echo "   2. Create a new database called 'catering_db'"
    echo "   3. Install the 'Catering Management' module"
    echo "   4. Start developing your catering system!"
    echo ""
    echo "🛠️  Development Commands:"
    echo "   View logs: docker-compose logs -f web"
    echo "   Restart Odoo: docker-compose restart web"
    echo "   Stop all: docker-compose down"
    echo ""
else
    echo "❌ Failed to start services. Check the logs:"
    docker-compose logs
fi
