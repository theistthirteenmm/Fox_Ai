#!/bin/bash
# Fox AI Docker Management Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
}

# Build Fox AI Docker image
build() {
    log_info "Building Fox AI Docker image..."
    docker-compose build --no-cache
    log_success "Fox AI image built successfully!"
}

# Start Fox AI services
start() {
    log_info "Starting Fox AI services..."
    docker-compose up -d
    log_success "Fox AI is starting up!"
    log_info "Web interface will be available at: http://localhost:7070"
    log_info "Check status with: ./docker-fox.sh status"
}

# Start with production setup (including Nginx)
start_prod() {
    log_info "Starting Fox AI with production setup..."
    docker-compose --profile production up -d
    log_success "Fox AI production setup is starting!"
    log_info "Web interface available at: http://localhost (port 80)"
    log_info "Direct access: http://localhost:7070"
}

# Stop Fox AI services
stop() {
    log_info "Stopping Fox AI services..."
    docker-compose down
    log_success "Fox AI services stopped!"
}

# Restart Fox AI services
restart() {
    log_info "Restarting Fox AI services..."
    docker-compose restart
    log_success "Fox AI services restarted!"
}

# Show service status
status() {
    log_info "Fox AI service status:"
    docker-compose ps
    echo ""
    log_info "Container logs (last 20 lines):"
    docker-compose logs --tail=20
}

# Show logs
logs() {
    log_info "Fox AI logs (press Ctrl+C to exit):"
    docker-compose logs -f
}

# Update Fox AI
update() {
    log_info "Updating Fox AI..."
    git pull origin main
    docker-compose down
    docker-compose build --no-cache
    docker-compose up -d
    log_success "Fox AI updated successfully!"
}

# Backup data
backup() {
    log_info "Creating Fox AI backup..."
    timestamp=$(date +%Y%m%d_%H%M%S)
    docker run --rm -v fox-ai_fox_data:/data -v $(pwd):/backup alpine tar czf /backup/fox-ai-backup-$timestamp.tar.gz -C /data .
    log_success "Backup created: fox-ai-backup-$timestamp.tar.gz"
}

# Restore data
restore() {
    if [ -z "$1" ]; then
        log_error "Please specify backup file: ./docker-fox.sh restore <backup-file>"
        exit 1
    fi
    
    if [ ! -f "$1" ]; then
        log_error "Backup file not found: $1"
        exit 1
    fi
    
    log_warning "This will replace all current data. Continue? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        log_info "Restoring from backup: $1"
        docker-compose down
        docker run --rm -v fox-ai_fox_data:/data -v $(pwd):/backup alpine sh -c "cd /data && tar xzf /backup/$1"
        docker-compose up -d
        log_success "Data restored successfully!"
    else
        log_info "Restore cancelled."
    fi
}

# Clean up Docker resources
clean() {
    log_warning "This will remove all Fox AI containers, images, and volumes. Continue? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        log_info "Cleaning up Fox AI Docker resources..."
        docker-compose down -v --rmi all
        docker system prune -f
        log_success "Cleanup completed!"
    else
        log_info "Cleanup cancelled."
    fi
}

# Show help
help() {
    echo "🦊 Fox AI Docker Management"
    echo "=========================="
    echo ""
    echo "Usage: ./docker-fox.sh <command>"
    echo ""
    echo "Commands:"
    echo "  build      Build Fox AI Docker image"
    echo "  start      Start Fox AI services"
    echo "  start-prod Start with production setup (Nginx)"
    echo "  stop       Stop Fox AI services"
    echo "  restart    Restart Fox AI services"
    echo "  status     Show service status and logs"
    echo "  logs       Show live logs"
    echo "  update     Update Fox AI from Git"
    echo "  backup     Create data backup"
    echo "  restore    Restore from backup"
    echo "  clean      Clean up all Docker resources"
    echo "  help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./docker-fox.sh build"
    echo "  ./docker-fox.sh start"
    echo "  ./docker-fox.sh restore fox-ai-backup-20260101_120000.tar.gz"
}

# Main script
main() {
    check_docker
    
    case "${1:-help}" in
        build)
            build
            ;;
        start)
            start
            ;;
        start-prod)
            start_prod
            ;;
        stop)
            stop
            ;;
        restart)
            restart
            ;;
        status)
            status
            ;;
        logs)
            logs
            ;;
        update)
            update
            ;;
        backup)
            backup
            ;;
        restore)
            restore "$2"
            ;;
        clean)
            clean
            ;;
        help|--help|-h)
            help
            ;;
        *)
            log_error "Unknown command: $1"
            help
            exit 1
            ;;
    esac
}

main "$@"
