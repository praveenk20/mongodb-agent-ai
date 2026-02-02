#!/bin/bash
# ===========================================
# MongoDB Agent - Quick Server Launcher
# ===========================================
# Starts the unified API and documentation server
#
# Author: Cisco Systems, Inc.
# License: MIT
# Version: 1.0.0
# ===========================================

echo "🚀 Starting MongoDB Agent Server..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if package is installed
if ! python3 -c "import mongodb_agent" 2>/dev/null; then
    echo "⚠️  MongoDB Agent not installed in editable mode"
    echo "📦 Installing package..."
    pip3 install -e .
fi

# Start the server
python3 server.py

# ===========================================
# End of Quick Server Launcher
# ===========================================
