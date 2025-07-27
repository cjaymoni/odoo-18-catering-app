#!/bin/bash

# Development helper script for Odoo Catering Management
echo "🛠️  Odoo Development Helper"
echo "=========================="

show_help() {
    echo "Available commands:"
    echo "  start     - Start the Odoo environment"
    echo "  stop      - Stop all services"
    echo "  restart   - Restart Odoo service"
    echo "  logs      - Show Odoo logs"
    echo "  shell     - Access Odoo shell (requires database name)"
    echo "  update    - Update module (requires module name)"
    echo "  backup    - Backup database (requires database name)"
    echo "  status    - Show service status"
    echo "  clean     - Remove all containers and volumes"
    echo ""
    echo "Usage: ./dev.sh [command] [arguments]"
    echo "Example: ./dev.sh shell catering_db"
    echo "Example: ./dev.sh update catering_management"
}

case "$1" in
    "start")
        echo "🚀 Starting Odoo services..."
        docker-compose up -d
        ;;
    "stop")
        echo "🛑 Stopping services..."
        docker-compose down
        ;;
    "restart")
        echo "🔄 Restarting Odoo..."
        docker-compose restart web
        ;;
    "logs")
        echo "📋 Showing Odoo logs (Ctrl+C to exit)..."
        docker-compose logs -f web
        ;;
    "shell")
        if [ -z "$2" ]; then
            echo "❌ Please provide database name: ./dev.sh shell database_name"
            exit 1
        fi
        echo "🐚 Accessing Odoo shell for database: $2"
        docker-compose exec web odoo shell -d "$2"
        ;;
    "update")
        if [ -z "$2" ]; then
            echo "❌ Please provide module name: ./dev.sh update module_name"
            exit 1
        fi
        if [ -z "$3" ]; then
            echo "❌ Please provide database name: ./dev.sh update module_name database_name"
            exit 1
        fi
        echo "📦 Updating module: $2 in database: $3"
        docker-compose exec web odoo -u "$2" -d "$3" --stop-after-init
        ;;
    "backup")
        if [ -z "$2" ]; then
            echo "❌ Please provide database name: ./dev.sh backup database_name"
            exit 1
        fi
        timestamp=$(date +"%Y%m%d_%H%M%S")
        filename="backup_${2}_${timestamp}.sql"
        echo "💾 Creating backup: $filename"
        docker-compose exec db pg_dump -U odoo "$2" > "$filename"
        echo "✅ Backup created: $filename"
        ;;
    "status")
        echo "📊 Service Status:"
        docker-compose ps
        ;;
    "clean")
        echo "🧹 This will remove all containers and volumes. Are you sure? (y/N)"
        read -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "🗑️  Cleaning up..."
            docker-compose down -v --remove-orphans
            docker-compose rm -f
            echo "✅ Cleanup complete"
        else
            echo "❌ Cleanup cancelled"
        fi
        ;;
    *)
        show_help
        ;;
esac
