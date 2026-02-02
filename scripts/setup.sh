#!/bin/bash
# ===========================================
# MongoDB Agent - Setup Script
# ===========================================
# This script sets up the MongoDB Agent for first-time use
#
# Author: Cisco Systems, Inc.
# License: MIT
# Version: 1.0.0
# ===========================================

set -e  # Exit on error

echo "🚀 MongoDB Agent Setup"
echo "====================="
echo ""

# Check Python version
echo "📌 Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]); then
    echo "❌ Python 3.9 or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi
echo "✅ Python $PYTHON_VERSION detected"
echo ""

# Ask user about MongoDB connection type
echo "🔧 MongoDB Connection Setup"
echo "============================"
echo ""
echo "How would you like to connect to MongoDB?"
echo ""
echo "1) MCP Protocol (Recommended for Claude Desktop / MCP clients)"
echo "   - Requires MCP server running separately"
echo "   - Best for AI assistant integrations"
echo ""
echo "2) Direct MongoDB Connection"
echo "   - Connects directly to MongoDB using PyMongo"
echo "   - No MCP server needed"
echo "   - Simpler for standalone use"
echo ""
read -p "Enter your choice (1 or 2): " CONNECTION_CHOICE
echo ""

if [ "$CONNECTION_CHOICE" = "2" ]; then
    echo "📦 Installing PyMongo for direct MongoDB connection..."
    pip3 install pymongo --quiet
    if [ $? -eq 0 ]; then
        echo "✅ PyMongo installed"
        USE_DIRECT_CONNECTION=true
    else
        echo "❌ Failed to install PyMongo"
        exit 1
    fi
    echo ""
else
    echo "✅ Will use MCP protocol (default)"
    USE_DIRECT_CONNECTION=false
    echo ""
fi

# Check if wheel file exists
echo "📦 Looking for package wheel..."
WHEEL_FILE=$(ls mongodb_agent_ai-*.whl 2>/dev/null | head -n 1)
if [ -z "$WHEEL_FILE" ]; then
    echo "❌ No wheel file found. Please ensure mongodb_agent-*.whl is in this directory."
    exit 1
fi
echo "✅ Found: $WHEEL_FILE"
echo ""

# Create .env if it doesn't exist
echo "⚙️  Checking configuration..."
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.template .env
    
    # Configure based on connection choice
    if [ "$USE_DIRECT_CONNECTION" = true ]; then
        echo "MONGODB_CONNECTION_TYPE=direct" >> .env
        echo "MONGODB_URI=mongodb://localhost:27017" >> .env
        echo "MONGODB_DATABASE=your_database_name" >> .env
        echo ""
        echo "✅ .env configured for DIRECT MongoDB connection"
        echo ""
        echo "⚠️  IMPORTANT: Please edit .env with your credentials:"
        echo "   - Set your LLM provider (OpenAI, Azure, or Anthropic)"
        echo "   - Add your API keys"
        echo "   - Update MONGODB_URI with your connection string"
        echo "   - Set MONGODB_DATABASE to your database name"
    else
        echo "MONGODB_CONNECTION_TYPE=mcp" >> .env
        echo ""
        echo "✅ .env configured for MCP connection"
        echo ""
        echo "⚠️  IMPORTANT: Please edit .env with your credentials:"
        echo "   - Set your LLM provider (OpenAI, Azure, or Anthropic)"
        echo "   - Add your API keys"
        echo "   - Configure MONGODB_MCP_ENDPOINT (default: http://localhost:3000/mongodb/query)"
        echo "   - Make sure your MCP server is running before testing"
    fi
    echo ""
    echo "   Run: nano .env"
    echo ""
else
    echo "✅ .env file exists"
    echo ""
fi

# Create directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p semantic_models
echo "✅ Directories created"
echo ""

# Install package
echo "📥 Installing MongoDB Agent package..."
pip3 install "$WHEEL_FILE" --upgrade --quiet
if [ $? -eq 0 ]; then
    echo "✅ Package installed successfully"
else
    echo "❌ Package installation failed"
    exit 1
fi
echo ""

# Verify installation
echo "🔍 Verifying installation..."
python3 -c "from mongodb_agent import MongoDBAgent; print('✅ Import successful')" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ MongoDB Agent is ready to use"
else
    echo "❌ Installation verification failed"
    exit 1
fi
echo ""

# Check semantic models
echo "📚 Checking semantic models..."
YAML_COUNT=$(find semantic_models -name "*.yaml" 2>/dev/null | wc -l | tr -d ' ')
if [ "$YAML_COUNT" -eq 0 ]; then
    echo "⚠️  No YAML semantic models found in semantic_models/"
    echo "   Add your MongoDB collection YAML files to semantic_models/"
    echo "   See example_collection.yaml for reference"
else
    echo "✅ Found $YAML_COUNT YAML semantic model(s)"
fi
echo ""

# Summary
echo "="*50
echo "✅ Setup Complete!"
echo "="*50
echo ""
echo "Next steps:"
echo "1. Edit .env with your credentials:  nano .env"
echo "2. Add semantic models to semantic_models/"
echo "3. Start the server:  ./start_server.sh"
echo ""
echo "For help, see:"
echo "  - QUICK_START.md"
echo "  - docs/USER_GUIDE.md"
echo "  - docs/TROUBLESHOOTING.md"
echo ""

# ===========================================
# End of Setup Script
# ===========================================
