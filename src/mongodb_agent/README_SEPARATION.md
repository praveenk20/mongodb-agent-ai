# Standalone MongoDB Agent Package

**⚠️ This is a separate implementation from the existing `mongodb_structure_agent/` deployment.**

## Purpose

This package (`mongodb_agent/`) provides a **reusable, standalone library** for MongoDB natural language query processing that:

- ✅ **Does NOT modify** existing `mongodb_structure_agent/`
- ✅ **Does NOT interfere** with current LangGraph server
- ✅ **Can be used** as a Python library in external projects
- ✅ **Can be deployed** as a separate MCP server
- ✅ **Can coexist** with existing production deployments

## Key Differences from mongodb_structure_agent/

| Aspect | `mongodb_structure_agent/` | `mongodb_agent/` |
|--------|---------------------------|------------------|
| **Purpose** | LangGraph server deployment | Reusable Python package |
| **Entry Point** | `mongo_agent.py:compiled_graph` | `MongoDBAgent` class |
| **Dependencies** | Cisco-specific (Conjur, CAE) | Generic (configurable) |
| **Deployment** | LangGraph `up` command | `pip install` |
| **Usage** | HTTP API only | Python import, MCP, CLI |
| **Configuration** | `config.ini` files | Environment variables |
| **State** | Production (unchanged) | New (beta) |

## Installation

```bash
# Install standalone package
pip install -e .

# Does not affect existing mongodb_structure_agent/
```

## Usage

### As Python Library
```python
from mongodb_agent import MongoDBAgent, Config

config = Config(
    llm_provider="azure",
    azure_endpoint="...",
    azure_api_key="...",
    vector_db="local",
    semantic_model_path="./semantic_models"
)

agent = MongoDBAgent(config)

result = agent.query(
    question="How many orders?",
    yaml_file_name="OrdersCollection.yaml",
    db_details={"database": "ESM"}
)

print(result["query_result"])
```

### As MCP Server (Separate from LangGraph)
```bash
# Run on different port
MONGODB_MCP_PORT=8001 python -m mcp_server.server
```

## Architecture

### Independent Deployment
```
┌────────────────────────────────────┐
│  Existing LangGraph Server         │
│  - mongodb_structure_agent/        │
│  - langgraph.json                  │
│  - Port 8000                       │
│  - Production APIs                 │
└────────────────────────────────────┘
              ↕ No Interaction
┌────────────────────────────────────┐
│  New Standalone Package            │
│  - mongodb_agent/                  │
│  - Python import or MCP server     │
│  - Port 8001 (if MCP)              │
│  - External integrations           │
└────────────────────────────────────┘
```

## Migration (Optional, Not Required)

If you want to eventually use this package in the LangGraph server:

### Step 1: Create Thin Wrapper
```python
# mongodb_agent_wrapper.py (new file at repo root)
from mongodb_agent import MongoDBAgent, Config

# Wrapper for LangGraph compatibility
config = Config.from_legacy_env(os.getenv("ENVIRONMENT", "dev"))
agent = MongoDBAgent(config)
compiled_graph = agent.compiled_graph
```

### Step 2: Update langgraph.json (When Ready)
```json
{
  "graphs": {
    "sql_agent": "./structured_agent/sql_agent.py:compiled_graph",
    "mongodb_agent": "./mongodb_structure_agent/mongo_agent.py:compiled_graph",
    "mongodb_agent_new": "./mongodb_agent_wrapper.py:compiled_graph"
  }
}
```

Both agents available simultaneously for A/B testing.

### Step 3: Gradual Cutover
After validation, update:
```json
{
  "graphs": {
    "sql_agent": "./structured_agent/sql_agent.py:compiled_graph",
    "mongodb_agent": "./mongodb_agent_wrapper.py:compiled_graph"
  }
}
```

## Use Cases

### Keep Using mongodb_structure_agent/ When:
- Production deployments
- Existing CAE integrations
- Supervisor agent orchestration
- Stable, tested workflows

### Use mongodb_agent/ When:
- External Python projects need MongoDB NL query
- Building custom integrations
- MCP server for Claude/Cursor
- Open source contributions
- Local development/testing

## No Breaking Changes

- ✅ `mongodb_structure_agent/` files unchanged
- ✅ `langgraph.json` unchanged
- ✅ Existing APIs unchanged
- ✅ Production deployments unaffected
- ✅ All new code in separate directories

## Development

### Test Existing Server (Unchanged)
```bash
cd /path/to/repo
langgraph up
# Works exactly as before
```

### Test New Package (Separate)
```bash
cd /path/to/repo
pip install -e ".[dev]"
python examples/basic_usage.py
```

Both work independently!

## Questions?

- **Existing deployment issues**: Use current support channels
- **New package questions**: GitHub Issues or sc-genai@cisco.com
- **Migration planning**: Contact team before making changes

---

**Remember**: This is **additive** - nothing breaks!
