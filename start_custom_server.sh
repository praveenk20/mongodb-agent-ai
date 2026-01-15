#!/bin/bash
# ===========================================
# MongoDB Agent - Custom Server with HTML Support
# ===========================================
# Serves both API docs (/docs) and HTML documentation (README.html, etc.)

set -a  # Auto-export all variables
source .env 2>/dev/null || true
set +a

# Default values
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"

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
            echo "Usage: ./start_custom_server.sh [options]"
            echo ""
            echo "Options:"
            echo "  --host HOST       Server host (default: 127.0.0.1)"
            echo "  --port PORT       Server port (default: 8000)"
            echo "  --help            Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./start_custom_server.sh"
            echo "  ./start_custom_server.sh --port 8002"
            echo "  ./start_custom_server.sh --host 0.0.0.0 --port 8000"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Run './start_custom_server.sh --help' for usage"
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
    echo "   Run: pip install mongodb_agent_ai-*.whl"
    echo "   Or: pip install mongodb_agent_ai-1.0.0-py3-none-any.whl"
    exit 1
fi

echo "Starting server..."
echo ""
echo "📚 Available URLs:"
echo "   Root/README:        http://$HOST:$PORT/"
echo "   API Documentation:  http://$HOST:$PORT/docs"
echo "   ReDoc:              http://$HOST:$PORT/redoc"
echo "   Setup Guide:        http://$HOST:$PORT/SETUP_GUIDE.html"
echo "   All HTML files:     http://$HOST:$PORT/<filename>.html"
echo ""

# Run the custom server
python3 -m uvicorn custom_server:app --host "$HOST" --port "$PORT" --reload
