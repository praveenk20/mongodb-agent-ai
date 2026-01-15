#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cisco Systems, Inc. and its affiliates

"""
Custom MongoDB Agent Server with Static File Support
Serves both API docs and HTML documentation files
"""
import os
import sys
from pathlib import Path

# Add mongodb_agent to path
try:
    from mongodb_agent.api import app
except ImportError:
    print("❌ MongoDB Agent not installed")
    print("   Run: pip install mongodb_agent-*.whl")
    sys.exit(1)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Get the directory where this script is located
DISTRIBUTION_DIR = Path(__file__).parent.absolute()

# Mount static files for HTML documentation
app.mount("/static", StaticFiles(directory=str(DISTRIBUTION_DIR)), name="static")

# Mount images directory for architecture diagrams
images_dir = DISTRIBUTION_DIR / "images"
if images_dir.exists():
    app.mount("/images", StaticFiles(directory=str(images_dir)), name="images")

# Serve README.html as the root page
@app.get("/")
async def read_root():
    """Redirect root to README.html"""
    readme_path = DISTRIBUTION_DIR / "README.html"
    if readme_path.exists():
        return FileResponse(readme_path)
    return {
        "service": "MongoDB Agent API",
        "version": "1.0.0",
        "documentation": "/README.html or /docs",
        "endpoints": {
            "health": "GET /health",
            "docs": "GET /docs",
            "readme": "GET /README.html",
            "query": "POST /api/mongodb",
            "validate": "POST /api/validate-yaml"
        }
    }

# Serve individual HTML files
@app.get("/index.html")
async def read_index():
    """Serve index.html"""
    return FileResponse(DISTRIBUTION_DIR / "index.html")

@app.get("/README.html")
async def read_readme():
    """Serve README.html"""
    return FileResponse(DISTRIBUTION_DIR / "README.html")

@app.get("/SETUP_GUIDE.html")
async def read_setup_guide():
    """Serve SETUP_GUIDE.html"""
    return FileResponse(DISTRIBUTION_DIR / "SETUP_GUIDE.html")

@app.get("/api-reference.html")
async def read_api_reference():
    """Serve api-reference.html"""
    return FileResponse(DISTRIBUTION_DIR / "api-reference.html")

@app.get("/architecture.html")
async def read_architecture():
    """Serve architecture.html"""
    return FileResponse(DISTRIBUTION_DIR / "architecture.html")

@app.get("/comparison.html")
async def read_comparison():
    """Serve comparison.html"""
    return FileResponse(DISTRIBUTION_DIR / "comparison.html")

@app.get("/configuration.html")
async def read_configuration():
    """Serve configuration.html"""
    return FileResponse(DISTRIBUTION_DIR / "configuration.html")

@app.get("/getting-started.html")
async def read_getting_started():
    """Serve getting-started.html"""
    return FileResponse(DISTRIBUTION_DIR / "getting-started.html")

@app.get("/installation.html")
async def read_installation():
    """Serve installation.html"""
    return FileResponse(DISTRIBUTION_DIR / "installation.html")

@app.get("/semantic-models.html")
async def read_semantic_models():
    """Serve semantic-models.html"""
    return FileResponse(DISTRIBUTION_DIR / "semantic-models.html")

@app.get("/troubleshooting.html")
async def read_troubleshooting():
    """Serve troubleshooting.html"""
    return FileResponse(DISTRIBUTION_DIR / "troubleshooting.html")

@app.get("/usage.html")
async def read_usage():
    """Serve usage.html"""
    return FileResponse(DISTRIBUTION_DIR / "usage.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
