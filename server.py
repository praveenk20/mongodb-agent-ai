#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cisco Systems, Inc. and its affiliates

"""
MongoDB Agent Server - Unified server for API and Documentation
Serves both the REST API and HTML documentation in a single service
"""
import os
import sys
from pathlib import Path

# Import the FastAPI app from mongodb_agent
try:
    from mongodb_agent.api import app
except ImportError:
    print("❌ MongoDB Agent not installed")
    print("   Run: pip install -e .")
    sys.exit(1)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Directory setup
BASE_DIR = Path(__file__).parent.absolute()
DOCS_DIR = BASE_DIR / "docs"


# Mount documentation as static files (serves all .html, .css, .js automatically)
if DOCS_DIR.exists():
    app.mount("/docs-static", StaticFiles(directory=str(DOCS_DIR), html=True), name="docs")
    
    # Mount images separately for better caching
    images_dir = DOCS_DIR / "images"
    if images_dir.exists():
        app.mount("/images", StaticFiles(directory=str(images_dir)), name="images")


# Root route - serve documentation homepage
@app.get("/")
async def serve_home():
    """Serve the documentation homepage"""
    index_path = DOCS_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {
        "service": "MongoDB Agent",
        "version": "1.0.0",
        "api_docs": "/docs",
        "documentation": "/docs-static/index.html"
    }


# Serve any HTML file from docs directory dynamically
@app.get("/{filename:path}.html")
async def serve_html(filename: str):
    """Serve any HTML documentation file"""
    file_path = DOCS_DIR / f"{filename}.html"
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    return {"error": f"Documentation file '{filename}.html' not found"}


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*70)
    print("🚀 MongoDB Agent - Unified API & Documentation Server")
    print("="*70)
    print("📖 Documentation: http://127.0.0.1:8001/")
    print("📡 API Endpoint:  http://127.0.0.1:8001/api/mongodb")
    print("📚 API Docs:      http://127.0.0.1:8001/docs")
    print("❤️  Health Check: http://127.0.0.1:8001/health")
    print("="*70 + "\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")
