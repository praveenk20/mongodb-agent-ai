# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cisco Systems, Inc. and its affiliates

"""
FastAPI REST API wrapper for MongoDB Agent
Provides HTTP endpoints for testing and integration
"""
import os
import sys
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

# Load environment variables from .env file
from dotenv import load_dotenv
# Load .env from current working directory
env_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path=env_path, override=True)

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Configure logging - Write to file instead of console
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'mongodb_agent.log')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, mode='a'),
        logging.StreamHandler(sys.stdout)  # Keep minimal console output
    ]
)
logger = logging.getLogger(__name__)
logger.info(f"📝 Logging to file: {log_file}")

# Initialize FastAPI app
app = FastAPI(
    title="MongoDB Agent API",
    description="Natural Language to MongoDB Query Converter with YAML Semantic Models",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Pydantic Models
# ============================================================

class MongoDBQueryRequest(BaseModel):
    """Request model for MongoDB query"""
    question: str = Field(..., description="Natural language question about the data")
    yaml_file_name: str = Field(..., description="YAML semantic model file name")
    include_debug: bool = Field(default=False, description="Include debug information in response")
    environment: Optional[str] = Field(default="dev", description="Environment (dev/stage/prod)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "Show me all shipping documents from USA to India",
                "yaml_file_name": "SLShippingDocuments_semantic_model_convert_V4.yaml",
                "include_debug": True,
                "environment": "dev"
            }
        }


class MongoDBQueryResponse(BaseModel):
    """Response model for MongoDB query"""
    question: str
    yaml_file_name: str
    mongodb_query: str = Field(description="Generated MongoDB aggregation pipeline")
    query_result: List[Dict[str, Any]] = Field(description="Query execution results")
    natural_language_response: str = Field(description="Natural language explanation of results")
    execution_time_ms: float
    status: str = Field(description="success or error")
    timestamp: str
    
    # Debug information (optional)
    debug_info: Optional[Dict[str, Any]] = Field(default=None, description="Debug information if include_debug=True")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "Show me all shipping documents from USA to India",
                "yaml_file_name": "SLShippingDocuments_semantic_model_convert_V4.yaml",
                "mongodb_query": "db.collection.aggregate([{\"$match\": {...}}])",
                "query_result": [{"deliveryId": "123", "shipFromCountry": "US"}],
                "natural_language_response": "Found 10 shipping documents from USA to India",
                "execution_time_ms": 1234.56,
                "status": "success",
                "timestamp": "2025-12-05T12:00:00",
                "debug_info": {
                    "matched_rules": ["country_code_preprocessing"],
                    "verified_queries_used": ["template_1"],
                    "yaml_analysis": "Loaded 15 tables with 120 fields"
                }
            }
        }


class YAMLValidationRequest(BaseModel):
    """Request model for YAML validation"""
    yaml_file_name: str = Field(..., description="YAML semantic model file name to validate")
    test_questions: Optional[List[str]] = Field(default=None, description="Optional test questions to validate against")


class YAMLValidationResponse(BaseModel):
    """Response model for YAML validation"""
    yaml_file_name: str
    valid: bool
    validation_errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    schema_summary: Optional[Dict[str, Any]] = None
    test_results: Optional[List[Dict[str, Any]]] = None


# ============================================================
# MongoDB Agent Integration (Standalone)
# ============================================================

from mongodb_agent.config import Config
from mongodb_agent.agent import MongoDBAgent

# Initialize MongoDB Agent (standalone, no dependencies on mongodb_structure_agent)
mongodb_agent_instance = None
mongodb_agent_available = False

try:
    config = Config.from_env()
    mongodb_agent_instance = MongoDBAgent(config)
    mongodb_agent_available = True
    logger.info("✅ MongoDB Agent initialized successfully (standalone)")
except Exception as e:
    logger.warning(f"⚠️ Could not initialize MongoDB Agent: {e}")
    logger.warning("Check .env file for required configuration (AZURE_OPENAI_ENDPOINT, etc.)")


def execute_mongodb_query(question: str, yaml_file_name: str, include_debug: bool = False) -> Dict[str, Any]:
    """
    Execute MongoDB query using the standalone MongoDB Agent
    
    This uses the mongodb_agent package which is completely independent
    from mongodb_structure_agent. It has its own graph, nodes, and services.
    
    Args:
        question: Natural language question
        yaml_file_name: YAML semantic model file name
        include_debug: Whether to include debug information
        
    Returns:
        Dictionary with query results and metadata
    """
    start_time = datetime.now()
    
    try:
        if not mongodb_agent_available or mongodb_agent_instance is None:
            raise Exception("MongoDB Agent not available. Check .env configuration.")
        
        logger.info(f"Executing MongoDB Agent query: {question}")
        logger.info(f"Using YAML file: {yaml_file_name}")
        
        # Get database details from environment
        db_details = {
            "dbName": os.getenv("MONGODB_DATABASE", "CCDTOOl"),
            "userName": os.getenv("MONGODB_USERNAME", ""),
            "applicationName": "MongoDB-Agent-REST-API"
        }
        
        # Execute query using standalone MongoDB Agent
        result = mongodb_agent_instance.query(
            question=question,
            yaml_file_name=yaml_file_name,
            db_details=db_details
        )
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds() * 1000
        
        # Extract results
        mongodb_query = result.get("aggregation_pipeline", "") or result.get("sql_query", "")
        query_result_raw = result.get("raw_mongo_result")  # Actual MongoDB data
        natural_language_raw = result.get("query_result", "")  # Natural language summary
        
        # Handle different response formats
        if query_result_raw is not None:
            # We have actual MongoDB results
            query_result = query_result_raw if isinstance(query_result_raw, list) else [query_result_raw]
            natural_language = natural_language_raw or f"Query executed successfully. Found {len(query_result)} results."
        elif isinstance(natural_language_raw, str):
            # Only have natural language response, no raw data
            natural_language = natural_language_raw
            query_result = []
        else:
            # Fallback
            query_result = []
            natural_language = result.get("natural_language_response", "Query executed successfully")
        
        # Build response
        response_data = {
            "mongodb_query": mongodb_query,
            "query_result": query_result if isinstance(query_result, list) else [],
            "natural_language_response": natural_language,
            "execution_time_ms": round(execution_time, 2),
            "status": "success" if not result.get("error") else "error"
        }
        
        # Add debug info if requested
        if include_debug:
            response_data["debug_info"] = {
                "matched_rules": result.get("matched_rules", []),
                "verified_queries_used": result.get("verified_queries_used", []),
                "yaml_analysis": result.get("yaml_analysis", ""),
                "llm_reasoning": result.get("llm_reasoning", ""),
                "intermediate_steps": result.get("intermediate_steps", []),
                "collection_name": result.get("collection_name", ""),
                "error": result.get("error", ""),
                "raw_result": str(result)[:500]  # First 500 chars
            }
        
        # If there was an error, include it in response
        if result.get("error"):
            response_data["natural_language_response"] = f"Error: {result['error']}"
        
        return response_data
        
    except FileNotFoundError as e:
        logger.error(f"YAML file not found: {e}")
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds() * 1000
        
        return {
            "mongodb_query": "N/A",
            "query_result": [],
            "natural_language_response": f"❌ Semantic model file not found: {yaml_file_name}. Please ensure the YAML file exists in the semantic_models directory.",
            "execution_time_ms": round(execution_time, 2),
            "status": "error",
            "debug_info": {
                "error_type": "FileNotFoundError",
                "error_details": str(e),
                "yaml_file_requested": yaml_file_name,
                "note": "Check that the semantic model exists in the configured semantic_models directory"
            } if include_debug else None
        }
    
    except Exception as e:
        logger.error(f"Error executing MongoDB query: {e}", exc_info=True)
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds() * 1000
        
        error_message = str(e)
        # Make error messages more user-friendly
        if "CLIENT_ID" in error_message or "CLIENT_SECRET" in error_message:
            error_message = "OAuth credentials missing. Please configure CLIENT_ID and CLIENT_SECRET in .env file."
        elif "Connection refused" in error_message:
            error_message = "Cannot connect to MongoDB. Please check MONGODB_URI in .env file."
        
        return {
            "mongodb_query": "N/A",
            "query_result": [],
            "natural_language_response": f"❌ Error: {error_message}",
            "execution_time_ms": round(execution_time, 2),
            "status": "error",
            "debug_info": {
                "error_type": type(e).__name__,
                "error_details": str(e),
                "note": "Standalone MongoDB Agent - check .env configuration"
            } if include_debug else None
        }


# ============================================================
# API Endpoints
# ============================================================

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "MongoDB Agent API",
        "version": "1.0.0",
        "status": "running",
        "mongodb_agent_available": mongodb_agent_available,
        "endpoints": {
            "health": "GET /health",
            "docs": "GET /docs",
            "query": "POST /api/mongodb",
            "validate": "POST /api/validate-yaml"
        },
        "description": "Natural Language to MongoDB Query Converter with YAML Semantic Models"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "mongodb_agent",
        "timestamp": datetime.now().isoformat(),
        "mongodb_agent_available": mongodb_agent_available
    }


@app.post("/api/mongodb", response_model=MongoDBQueryResponse)
async def query_mongodb(request: MongoDBQueryRequest):
    """
    MongoDB query endpoint
    
    Processes natural language questions using YAML semantic models:
    1. Loads the specified YAML semantic model
    2. Analyzes the question and applies business rules
    3. Generates MongoDB aggregation pipeline
    4. Executes the query (if configured)
    5. Returns results with natural language explanation
    
    The response includes:
    - Generated MongoDB query
    - Query execution results
    - Natural language explanation
    - Debug information (if requested)
    """
    try:
        logger.info(f"Processing MongoDB query: {request.question}")
        
        # Execute the query
        result = execute_mongodb_query(
            question=request.question,
            yaml_file_name=request.yaml_file_name,
            include_debug=request.include_debug
        )
        
        # Build response
        response = MongoDBQueryResponse(
            question=request.question,
            yaml_file_name=request.yaml_file_name,
            mongodb_query=result["mongodb_query"],
            query_result=result["query_result"],
            natural_language_response=result["natural_language_response"],
            execution_time_ms=result["execution_time_ms"],
            status=result["status"],
            timestamp=datetime.now().isoformat(),
            debug_info=result.get("debug_info")
        )
        
        logger.info(f"Query processed successfully in {result['execution_time_ms']}ms")
        return response
        
    except Exception as e:
        logger.error(f"Error in /api/mongodb endpoint: {e}", exc_info=True)
        
        # Provide user-friendly error messages
        error_detail = str(e)
        if "FileNotFoundError" in str(type(e)):
            raise HTTPException(status_code=404, detail=f"Semantic model file not found: {request.yaml_file_name}")
        elif "validation error" in str(e).lower():
            raise HTTPException(status_code=400, detail=f"Invalid request: {error_detail}")
        else:
            raise HTTPException(status_code=500, detail=error_detail)


@app.post("/api/validate-yaml", response_model=YAMLValidationResponse)
async def validate_yaml(request: YAMLValidationRequest):
    """
    Validate YAML semantic model
    
    Checks:
    - YAML syntax and structure
    - Required fields presence
    - Collection/table definitions
    - Field mappings
    - Business rules syntax
    
    Optionally tests against provided questions.
    """
    try:
        logger.info(f"Validating YAML: {request.yaml_file_name}")
        
        # TODO: Implement YAML validation logic
        # For now, return a placeholder response
        
        return YAMLValidationResponse(
            yaml_file_name=request.yaml_file_name,
            valid=True,
            validation_errors=[],
            warnings=["YAML validation not yet implemented"],
            schema_summary={
                "note": "Full validation coming soon"
            },
            test_results=None
        )
        
    except Exception as e:
        logger.error(f"Error validating YAML: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/capabilities")
async def get_capabilities():
    """Get MongoDB Agent capabilities"""
    return {
        "mongodb_agent": {
            "description": "Natural Language to MongoDB Query Converter",
            "features": [
                "YAML-based semantic models",
                "Business rules and verified queries",
                "Country code preprocessing",
                "Date range handling",
                "Aggregation pipelines",
                "Debug mode for YAML tuning"
            ],
            "supported_databases": ["MongoDB"],
            "available": mongodb_agent_available
        },
        "endpoints": {
            "/api/mongodb": "Execute MongoDB queries from natural language",
            "/api/validate-yaml": "Validate YAML semantic models",
            "/health": "Health check",
            "/docs": "API documentation"
        }
    }


# ============================================================
# Application Startup
# ============================================================

@app.on_event("startup")
async def startup_event():
    """Application startup tasks"""
    logger.info("🚀 MongoDB Agent API starting up")
    logger.info(f"📡 MongoDB Agent available: {mongodb_agent_available}")
    if mongodb_agent_available:
        logger.info("✅ Ready to process MongoDB queries")
    else:
        logger.warning("⚠️ MongoDB Agent not available - check configuration")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks"""
    logger.info("👋 MongoDB Agent API shutting down")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
