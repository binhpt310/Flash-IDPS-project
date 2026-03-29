#!/bin/bash
# Flash-IDPS Docker Setup Script
# Automates the setup and running of the Flash-IDPS Jupyter notebook environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Functions
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    print_success "Docker is installed"
}

check_docker_compose() {
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    print_success "Docker Compose is installed"
}

create_directories() {
    print_header "Creating Required Directories"
    
    mkdir -p data models output notebooks
    
    print_success "Directories created: data/, models/, output/, notebooks/"
}

build_image() {
    print_header "Building Docker Image"
    
    if [ "$1" == "gpu" ]; then
        print_warning "Building GPU-enabled image..."
        docker build -f Dockerfile.gpu -t flash-idps:gpu --target final .
    else
        print_success "Building CPU-only image..."
        docker build -t flash-idps:latest --target final .
    fi
    
    print_success "Docker image built successfully"
}

start_container() {
    print_header "Starting Container"
    
    if [ "$1" == "gpu" ]; then
        print_warning "Starting GPU-enabled container on port 8889..."
        docker compose --profile gpu up -d flash-idps-gpu 2>/dev/null || \
        docker run -d --gpus all \
            --name flash-idps-gpu-notebook \
            -p 8889:8888 \
            -v "$(pwd)":/app:cached \
            -v "$(pwd)/data":/app/data \
            -v "$(pwd)/models":/app/models \
            -v "$(pwd)/output":/app/output \
            -e JUPYTER_ENABLE_LAB=yes \
            flash-idps:gpu
    else
        print_success "Starting CPU-only container on port 8888..."
        docker compose up -d flash-idps 2>/dev/null || \
        docker run -d \
            --name flash-idps-notebook \
            -p 8888:8888 \
            -v "$(pwd)":/app:cached \
            -v "$(pwd)/data":/app/data \
            -v "$(pwd)/models":/app/models \
            -v "$(pwd)/output":/app/output \
            flash-idps:latest
    fi
    
    print_success "Container started"
}

stop_container() {
    print_header "Stopping Container"
    
    docker compose down 2>/dev/null || true
    docker stop flash-idps-notebook flash-idps-gpu-notebook 2>/dev/null || true
    docker rm flash-idps-notebook flash-idps-gpu-notebook 2>/dev/null || true
    
    print_success "Container stopped"
}

show_status() {
    print_header "Container Status"
    
    echo ""
    echo "Running containers:"
    docker ps --filter "name=flash-idps" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    echo ""
    echo "Docker images:"
    docker images flash-idps --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
}

show_access_info() {
    print_header "Access Information"
    
    echo ""
    echo -e "${GREEN}Jupyter Notebook is running!${NC}"
    echo ""
    echo "Access the notebook at:"
    echo -e "  ${BLUE}http://localhost:8888${NC}"
    echo ""
    echo "To stop the container:"
    echo "  ./setup.sh stop"
    echo ""
    echo "To view logs:"
    echo "  docker logs -f flash-idps-notebook"
    echo ""
}

# Main script
main() {
    print_header "Flash-IDPS Docker Setup"
    
    case "${1:-setup}" in
        setup)
            check_docker
            check_docker_compose
            create_directories
            build_image
            start_container
            sleep 5
            show_access_info
            ;;
        build)
            check_docker
            build_image "${2:-}"
            ;;
        start)
            start_container "${2:-}"
            show_access_info
            ;;
        stop)
            stop_container
            ;;
        restart)
            stop_container
            sleep 2
            start_container "${2:-}"
            show_access_info
            ;;
        status)
            show_status
            ;;
        clean)
            print_header "Cleaning Up"
            docker rmi flash-idps:latest flash-idps:gpu 2>/dev/null || true
            print_success "Images removed"
            ;;
        help|*)
            echo "Flash-IDPS Docker Setup Script"
            echo ""
            echo "Usage: ./setup.sh [command] [options]"
            echo ""
            echo "Commands:"
            echo "  setup       - Full setup (default): check, build, and start"
            echo "  build       - Build Docker image only"
            echo "  build gpu   - Build GPU-enabled image"
            echo "  start       - Start container"
            echo "  start gpu   - Start GPU-enabled container"
            echo "  stop        - Stop and remove container"
            echo "  restart     - Restart container"
            echo "  status      - Show container status"
            echo "  clean       - Remove Docker images"
            echo "  help        - Show this help message"
            echo ""
            ;;
    esac
}

main "$@"
