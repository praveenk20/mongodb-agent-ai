# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cisco Systems, Inc. and its affiliates

"""
MongoDB Agent - Basic Query Example
===================================
Simple example showing how to query MongoDB using natural language
"""

from mongodb_agent import MongoDBAgent, Config
import json

def main():
    """Run a basic MongoDB query"""
    
    print("🚀 MongoDB Agent - Basic Query Example")
    print("="*50)
    print()
    
    # Load configuration from .env file
    print("📋 Loading configuration from .env...")
    config = Config.from_env()
    print(f"✅ LLM Provider: {config.llm_provider}")
    print(f"✅ Vector DB: {config.vector_db}")
    print(f"✅ MongoDB Connection: {config.mongodb_connection_type.upper()}")
    if config.mongodb_connection_type == "direct":
        print(f"   Database: {config.mongodb_database}")
    print()
    
    # Create MongoDB Agent
    print("🤖 Initializing MongoDB Agent...")
    agent = MongoDBAgent(config)
    print("✅ Agent ready")
    print()
    
    # Example query
    question = "Show me all records from the last 7 days"
    yaml_file = "example_collection.yaml"
    
    print(f"❓ Question: {question}")
    print(f"📄 Semantic Model: {yaml_file}")
    print()
    
    # Execute query
    print("⚙️  Executing query...")
    try:
        result = agent.query(
            question=question,
            yaml_file_name=yaml_file
        )
        
        print("✅ Query executed successfully!")
        print()
        print("="*50)
        print("📊 RESULTS")
        print("="*50)
        print()
        
        # Print the natural language response
        if "query_result" in result:
            print("Natural Language Response:")
            print(result["query_result"])
            print()
        
        # Print the generated MongoDB query
        if "sql_query" in result:
            print("Generated MongoDB Query:")
            print(result["sql_query"])
            print()
        
        # Print collection name
        if "collection_name" in result:
            print(f"Collection: {result['collection_name']}")
            print()
        
        # Print any errors
        if "error" in result and result["error"]:
            print(f"⚠️  Error: {result['error']}")
            print()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
    
    print("="*50)
    print("✅ Example complete!")
    print()
    print("Try modifying the question to test different queries:")
    print("  - 'Count all records'")
    print("  - 'Show records where status is active'")
    print("  - 'Group by status and count'")
    print("  - 'Find records with amount greater than 1000'")
    print()

if __name__ == "__main__":
    main()
