# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cisco Systems, Inc. and its affiliates

"""
Server module for MongoDB Agent
Provides both MCP protocol and REST API endpoints
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import full structured_agent_server first (for complete application)
# Fall back to standalone API if not available (for distribution package)
try:
    from scripts.servers.structured_agent_server import app
    print("✅ Using full structured_agent_server with all agents")
except ImportError:
    # Use standalone MongoDB Agent API
    try:
        from mongodb_agent.api import app
        print("✅ Using standalone MongoDB Agent API")
    except ImportError:
        # Final fallback: minimal server
        from fastapi import FastAPI
        
        app = FastAPI(
            title="MongoDB Agent API",
            description="Natural Language to MongoDB Query Converter",
            version="1.0.0"
        )
        
        @app.get("/health")
        def health_check():
            return {"status": "healthy", "service": "mongodb_agent"}
        
        print("⚠️ Using minimal fallback server")

__all__ = ["app"]
