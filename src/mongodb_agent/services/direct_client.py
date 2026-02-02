# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cisco Systems, Inc. and its affiliates

"""
Direct MongoDB client using PyMongo

Handles:
- Direct MongoDB connection
- Aggregation pipeline execution
- Connection pooling
- Error handling
"""

import logging
from typing import Dict, Any, Optional
import json

from mongodb_agent.config import Config

logger = logging.getLogger(__name__)

# PyMongo is optional - only imported if direct connection is used
try:
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False
    logger.warning("PyMongo not installed. Direct MongoDB connection unavailable.")


class DirectMongoClient:
    """Direct MongoDB client using PyMongo"""
    
    def __init__(self, config: Config):
        if not PYMONGO_AVAILABLE:
            raise ImportError(
                "PyMongo is required for direct MongoDB connection. "
                "Install it with: pip install pymongo"
            )
        
        self.uri = config.mongodb_uri
        self.database_name = config.mongodb_database
        self.client = None
        self.db = None
        
        if not self.uri:
            raise ValueError("MONGODB_URI is required for direct connection")
        if not self.database_name:
            raise ValueError("MONGODB_DATABASE is required for direct connection")
        
        logger.info(f"Initializing direct MongoDB connection to: {self.database_name}")
        self._connect()
    
    def _connect(self):
        """Establish MongoDB connection"""
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.database_name]
            # Test connection
            self.client.admin.command('ping')
            logger.info(f"✅ Connected to MongoDB: {self.database_name}")
        except Exception as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            raise
    
    def execute_query(
        self,
        aggregation_pipeline: str,
        db_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute MongoDB aggregation pipeline directly
        
        Args:
            aggregation_pipeline: MongoDB aggregation pipeline (JSON string or list)
            db_details: Database details (must include 'collection' name)
        
        Returns:
            Dict with keys: success, data, error
        """
        try:
            # Parse collection name from various possible keys
            collection_name = (
                db_details.get("collection") or 
                db_details.get("collectionName") or
                db_details.get("collection_name")
            )
            
            if not collection_name:
                error_msg = "Collection name is required in db_details (use 'collection' key)"
                logger.error(error_msg)
                return {
                    "success": False,
                    "data": None,
                    "error": error_msg
                }
            
            collection = self.db[collection_name]
            
            # Parse pipeline
            if isinstance(aggregation_pipeline, str):
                import re
                from datetime import datetime
                
                pipeline_str = aggregation_pipeline.strip()
                
                # Extract pipeline from db.collection.aggregate([...]) format
                if "aggregate(" in pipeline_str:
                    start = pipeline_str.find("[")
                    end = pipeline_str.rfind("]") + 1
                    if start != -1 and end > start:
                        pipeline_str = pipeline_str[start:end]
                
                # Convert ISODate("...") to temporary placeholders
                isodate_values = {}
                def store_isodate(match):
                    date_str = match.group(1)
                    key = f"__ISODATE_{len(isodate_values)}__"
                    isodate_values[key] = date_str
                    return f'"{key}"'
                
                pipeline_str = re.sub(r'ISODate\("([^"]+)"\)', store_isodate, pipeline_str)
                
                try:
                    pipeline = json.loads(pipeline_str)
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON in aggregation pipeline: {e}")
                    logger.error(f"Pipeline string: {pipeline_str[:500]}")
                    raise ValueError(f"Invalid JSON in aggregation pipeline: {e}")
                
                # Replace placeholders with datetime objects
                def replace_dates(obj):
                    if isinstance(obj, dict):
                        return {k: replace_dates(v) for k, v in obj.items()}
                    elif isinstance(obj, list):
                        return [replace_dates(item) for item in obj]
                    elif isinstance(obj, str) and obj in isodate_values:
                        date_str = isodate_values[obj]
                        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    return obj
                
                pipeline = replace_dates(pipeline)
            else:
                pipeline = aggregation_pipeline
            
            if not isinstance(pipeline, list):
                error_msg = f"Pipeline must be a list of stages, got: {type(pipeline)}"
                logger.error(error_msg)
                return {
                    "success": False,
                    "data": None,
                    "error": error_msg
                }
            
            logger.info("="*80)
            logger.info("📤 DIRECT MONGODB QUERY")
            logger.info(f"Database: {self.database_name}")
            logger.info(f"Collection: {collection_name}")
            logger.info(f"Pipeline: {str(pipeline)[:1000]}")  # Use str() instead of json.dumps()
            logger.info("="*80)
            
            # Execute aggregation
            result = list(collection.aggregate(pipeline))
            
            logger.info("="*80)
            logger.info("📥 MONGODB RESPONSE")
            logger.info(f"Success: True")
            logger.info(f"Documents Returned: {len(result)}")
            if len(result) > 0:
                logger.info(f"Sample Document Keys: {list(result[0].keys()) if result else []}")
            logger.info("="*80)
            
            return {
                "success": True,
                "data": result,
                "error": None
            }
        
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in aggregation pipeline: {e}"
            logger.error(error_msg)
            logger.error(f"Pipeline string: {aggregation_pipeline[:500]}")
            return {
                "success": False,
                "data": None,
                "error": error_msg
            }
        
        except Exception as e:
            error_msg = f"MongoDB query failed: {str(e)}"
            logger.exception(error_msg)
            return {
                "success": False,
                "data": None,
                "error": error_msg
            }
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")


def get_direct_client(config: Config) -> DirectMongoClient:
    """Get direct MongoDB client instance"""
    return DirectMongoClient(config)
