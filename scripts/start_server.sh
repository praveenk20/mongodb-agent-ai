#!/bin/bash
# ===========================================
# MongoDB Agent - Unified Server Launcher
# ===========================================
# Serves both API and HTML documentation
#
# Author: Cisco Systems, Inc.
# License: MIT
# Version: 1.0.0
# ===========================================

set -a  # Auto-export all variables
source .env 2>/dev/null || true
set +a

# Default values
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8001}"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --host)
            HOST="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --help)
            echo "Usage: ./scripts/start_server.sh [options]"
            echo ""
            echo "Options:"
            echo "  --host HOST       Server host (default: 127.0.0.1)"
            echo "  --port PORT       Server port (default: 8001)"
            echo "  --help            Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./scripts/start_server.sh"
            echo "  ./scripts/start_server.sh --port 8002"
            echo "  ./scripts/start_server.sh --host 0.0.0.0 --port 8001"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Run './scripts/start_server.sh --help' for usage"
            exit 1
            ;;
    esac
done

echo "🚀 Starting MongoDB Agent with HTML Documentation"
echo "=================================================="
echo "Host:   $HOST"
echo "Port:   $PORT"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "   Run ./setup.sh first or create .env from .env.template"
    echo ""
fi

# Check if package is installed
python3 -c "from mongodb_agent import MongoDBAgent" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ MongoDB Agent not installed"
    echo "   Installing in editable mode..."
    pip3 install -e .
fi

echo "Starting MongoDB Agent Server..."
echo ""
echo "📚 Available URLs:"
echo "   Documentation:      http://$HOST:$PORT/"
echo "   API Docs:           http://$HOST:$PORT/docs"
echo "   API Endpoint:       http://$HOST:$PORT/api/mongodb"
echo "   Health Check:       http://$HOST:$PORT/health"
echo ""

# Run the unified server
python3 server.py

# ===========================================
# End of Unified Server Launcher
# ===========================================
