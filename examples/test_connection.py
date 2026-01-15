#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cisco Systems, Inc. and its affiliates

"""
Test Direct MongoDB Connection
===============================
This script tests the direct MongoDB connection without MCP server
"""

import os
import sys
from mongodb_agent import Config
from mongodb_agent.services.mongodb_router import get_mongodb_client

def test_direct_connection():
    """Test direct MongoDB connection"""
    
    print("🧪 Testing Direct MongoDB Connection")
    print("="*60)
    print()
    
    # Create test configuration
    print("📋 Creating test configuration...")
    config = Config(
        llm_provider="openai",
        openai_api_key=os.getenv("OPENAI_API_KEY", "test-key"),
        mongodb_connection_type="direct",
        mongodb_uri=os.getenv("MONGODB_URI", "mongodb://localhost:27017"),
        mongodb_database=os.getenv("MONGODB_DATABASE", "test_db"),
        vector_db="local",
        semantic_model_path="./semantic_models"
    )
    
    print(f"✅ Connection Type: {config.mongodb_connection_type}")
    print(f"✅ MongoDB URI: {config.mongodb_uri}")
    print(f"✅ Database: {config.mongodb_database}")
    print()
    
    # Initialize MongoDB client
    print("🔌 Connecting to MongoDB...")
    try:
        client = get_mongodb_client(config)
        print("✅ MongoDB client initialized")
        print()
        
        # Test query
        print("📝 Testing aggregation query...")
        test_collection = os.getenv("TEST_COLLECTION", "test_collection")
        
        pipeline = [
            {"$limit": 5},
            {"$project": {"_id": 1}}
        ]
        
        result = client.execute_query(
            aggregation_pipeline=str(pipeline),
            db_details={"collection": test_collection}
        )
        
        print()
        print("="*60)
        print("📊 RESULTS")
        print("="*60)
        print()
        
        if result["success"]:
            print(f"✅ Query executed successfully!")
            print(f"📄 Documents returned: {len(result['data'])}")
            print()
            
            if result["data"]:
                print("Sample documents:")
                for i, doc in enumerate(result["data"][:3], 1):
                    print(f"  {i}. {doc}")
            else:
                print("  (No documents found)")
            
            print()
            print("="*60)
            print("✅ TEST PASSED")
            print("="*60)
            return True
        else:
            print(f"❌ Query failed: {result['error']}")
            print()
            print("="*60)
            print("❌ TEST FAILED")
            print("="*60)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("="*60)
        print("❌ TEST FAILED")
        print("="*60)
        return False
    finally:
        if 'client' in locals():
            client.close()
            print("🔌 Connection closed")

def test_mcp_connection():
    """Test MCP connection"""
    
    print()
    print("🧪 Testing MCP Connection")
    print("="*60)
    print()
    
    # Create test configuration
    print("📋 Creating test configuration...")
    config = Config(
        llm_provider="openai",
        openai_api_key=os.getenv("OPENAI_API_KEY", "test-key"),
        mongodb_connection_type="mcp",
        mongodb_mcp_endpoint=os.getenv("MONGODB_MCP_ENDPOINT", "http://localhost:3000/mongodb/query"),
        vector_db="local",
        semantic_model_path="./semantic_models"
    )
    
    print(f"✅ Connection Type: {config.mongodb_connection_type}")
    print(f"✅ MCP Endpoint: {config.mongodb_mcp_endpoint}")
    print()
    
    # Initialize MongoDB client
    print("🔌 Connecting to MCP server...")
    try:
        client = get_mongodb_client(config)
        print("✅ MCP client initialized")
        print()
        
        print("⚠️  Note: MCP tests require a running MCP server")
        print("   Skipping actual query execution")
        print()
        
        print("="*60)
        print("✅ TEST PASSED (Setup Only)")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("="*60)
        print("❌ TEST FAILED")
        print("="*60)
        return False

def main():
    """Run all tests"""
    
    print()
    print("="*60)
    print("   MongoDB Agent Connection Tests")
    print("="*60)
    print()
    
    # Check environment variables
    print("📋 Environment Check:")
    print(f"   MONGODB_CONNECTION_TYPE: {os.getenv('MONGODB_CONNECTION_TYPE', 'not set')}")
    print(f"   MONGODB_URI: {os.getenv('MONGODB_URI', 'not set')}")
    print(f"   MONGODB_DATABASE: {os.getenv('MONGODB_DATABASE', 'not set')}")
    print(f"   MONGODB_MCP_ENDPOINT: {os.getenv('MONGODB_MCP_ENDPOINT', 'not set')}")
    print()
    
    connection_type = os.getenv('MONGODB_CONNECTION_TYPE', 'direct').lower()
    
    if connection_type == 'direct':
        success = test_direct_connection()
    else:
        success = test_mcp_connection()
    
    print()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
