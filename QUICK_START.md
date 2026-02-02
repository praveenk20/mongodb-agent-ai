# 🚀 MongoDB Agent - Quick Start Guide

Get started with MongoDB Agent in **5 minutes**!

---

## Prerequisites

✅ Python 3.9 or higher  
✅ MongoDB instance (local or remote)  
✅ LLM API key (OpenAI, Azure, or Anthropic)

---

## Step 1: Run Setup Script

The setup script will guide you through the installation:

```bash
# Run interactive setup
./setup.sh
```

**You'll be asked to choose:**
1. **MCP Protocol** - For Claude Desktop / AI assistant integrations
2. **Direct Connection** - For standalone use (simpler setup)

### Option 1: MCP Protocol (Recommended for Claude Desktop)
- Requires MCP server running separately
- Best for AI assistant integrations
- See: https://github.com/modelcontextprotocol/servers

### Option 2: Direct Connection (Simpler)
- No MCP server needed
- Connects directly via PyMongo
- Best for local development and testing

---

## Step 2: Configure Environment

After setup, edit `.env` with your credentials:

```bash
nano .env  # or use your favorite editor
```

### Configuration Examples

**Option A: Direct MongoDB Connection (Simplest)**
```bash
# MongoDB Connection
MONGODB_CONNECTION_TYPE=direct
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=your_database_name

# LLM Provider
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
```

**Option B: MCP Protocol Connection**
```bash
# MongoDB Connection
MONGODB_CONNECTION_TYPE=mcp
MONGODB_MCP_ENDPOINT=http://localhost:3000/mongodb/query

# LLM Provider
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
```

**Option C: Azure OpenAI + Direct MongoDB**
```bash
# MongoDB Connection
MONGODB_CONNECTION_TYPE=direct
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=your_database_name

# LLM Provider
LLM_PROVIDER=azure
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
```

---

## Step 3: Start the Server

Start the server to access the web interface and API:

```bash
# Option 1: Quick start (from project root)
./start_server.sh

# Option 2: Direct Python
python3 server.py

# Option 3: Using scripts folder
./scripts/start_server.sh
```

Then access:
- **📖 HTML Docs:** http://127.0.0.1:8001/
- **📚 API Docs:** http://127.0.0.1:8001/docs
- **❤️ Health Check:** http://127.0.0.1:8001/health

---

## Step 4: Create a Semantic Model

Create `semantic_models/my_collection.yaml`:

```yaml
collection_info:
  database: "myapp"
  schema_name: "orders"
  
collections:
  orders:
    name: orders
    description: "Customer orders collection"
    fields:
      _id:
        data_type: "ObjectId"
        description: "Unique order ID"
      orderDate:
        data_type: "date"
        description: "Order creation date"
      customerName:
        data_type: "string"
        description: "Customer name"
      totalAmount:
        data_type: "number"
        description: "Total order amount"
      status:
        data_type: "string"
        description: "Order status"
        sample_values: ["pending", "shipped", "delivered"]

verified_queries:
  - name: "RecentOrders"
    question: "Show me orders from last 30 days"
    mongodb_query: 'db.orders.find({"orderDate": {"$gte": new Date(Date.now() - 30*24*60*60*1000)}})'
```

---

## Step 4: Start the Server

### Option A: MCP Server (for Claude Desktop)

```bash
python3 -m mongodb_agent.cli server --port 8000
```

### Option B: REST API Server (for HTTP access)

```bash
python3 -m mongodb_agent.cli server --port 8000 --mode rest
```

---

## Step 5: Test Your Setup

### Test via Python

```python
from mongodb_agent import MongoDBAgent, Config

# Load config from .env
config = Config.from_env()

# Create agent
agent = MongoDBAgent(config)

# Run a query
result = agent.query(
    question="Show me all orders from last month",
    yaml_file_name="my_collection.yaml"
)

print(result["query_result"])
```

### Test via REST API

```bash
curl -X POST http://localhost:8000/api/mongodb \\
  -H "Content-Type: application/json" \\
  -d '{
    "question": "Show me all orders from last month",
    "yaml_file_name": "my_collection.yaml"
  }'
```

### Test via MCP (Claude Desktop)

Add to your Claude Desktop config (`~/.config/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "mongodb-agent": {
      "command": "python3",
      "args": ["-m", "mongodb_agent.cli", "server", "--port", "8000"]
    }
  }
}
```

Then in Claude: "Using mongodb-agent, show me all orders from last month"

---

## ✅ Verify It's Working

If everything is set up correctly, you should see:

```
✅ Server started on http://127.0.0.1:8000
✅ MongoDB Agent initialized
✅ LLM provider: openai
✅ Vector DB: local
✅ Ready to accept queries
```

---

## 🎯 Example Queries

Try these natural language questions:

- "How many orders were placed last week?"
- "Show me the top 10 customers by total order value"
- "What is the average order amount for each month?"
- "Find all pending orders older than 7 days"
- "Group orders by status and count them"

---

## 🐛 Troubleshooting

### Server won't start

```bash
# Check if port is in use
lsof -i :8000

# Use a different port
python3 -m mongodb_agent.cli server --port 8001
```

### Can't connect to MongoDB

```bash
# Check MCP endpoint is running
curl http://localhost:3000/health

# Verify MongoDB connection
mongo --eval "db.adminCommand('ping')"
```

### LLM authentication failed

```bash
# Test your API key
curl https://api.openai.com/v1/models \\
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Import errors

```bash
# Reinstall package
pip uninstall mongodb-agent
pip install mongodb_agent-1.0.0-py3-none-any.whl --force-reinstall
```

---

## 📚 Next Steps

- **Read the full [USER_GUIDE.md](./docs/USER_GUIDE.md)** for advanced features
- **Check [API_REFERENCE.md](./docs/API_REFERENCE.md)** for API details
- **See [examples/](./examples/)** for more code examples
- **Review [CONFIGURATION.md](./docs/CONFIGURATION.md)** for all config options

---

## 💡 Pro Tips

1. **Use semantic models** - They dramatically improve query accuracy
2. **Add verified queries** - Pre-define common queries for best results
3. **Enable token caching** - Speeds up repeated queries
4. **Start with simple queries** - Test basic functionality first
5. **Check the logs** - Located in `logs/mongodb_agent.log`

---

## 🆘 Need Help?

- **Documentation**: See `docs/` folder
- **Examples**: See `examples/` folder
- **Issues**: [GitHub Issues](https://github.com/your-org/mongodb-agent/issues)
- **Troubleshooting**: [TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)

---

**Happy querying! 🎉**
