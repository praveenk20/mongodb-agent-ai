# MongoDB Agent AI - Architecture Diagram

## How Semantic Models + MongoDB Rules Process Queries

### Mermaid Diagram (Copy to mermaid.live or use in markdown renderers)

```mermaid
flowchart TD
    Start([User Query: Get DBS transactions REC-DGI last 30 days]) --> Router[Router Node]
    
    Router --> Semantic[Semantic Model Layer]
    
    Semantic --> SM1[Field Definitions<br/>partnerName: string<br/>transactionSubType: string<br/>creationDate: datetime]
    Semantic --> SM2[Sample Values<br/>partnerName: DHLUS DBSMX DBS<br/>transactionSubType: SSG REC-DGI DGI]
    Semantic --> SM3[Data Types & Descriptions<br/>Business context for each field]
    
    SM1 & SM2 & SM3 --> Mapping{Semantic Mapping}
    
    Mapping -->|DBS → partnerName| Map1[partnerName field]
    Mapping -->|REC-DGI → transactionSubType| Map2[transactionSubType field]
    Mapping -->|last 30 days → creationDate| Map3[creationDate field]
    
    Map1 & Map2 & Map3 --> Rules[MongoDB Rules Layer]
    
    Rules --> R1[Field Priorities<br/>✓ Use essential_fields<br/>✓ Limit to 25 fields max]
    Rules --> R2[Query Type Rules<br/>✓ Max 1 collection<br/>✓ Relevance threshold 0.8]
    Rules --> R3[Custom Instructions<br/>✓ ISODate format<br/>✓ Case-insensitive regex<br/>✓ $match early in pipeline]
    
    R1 & R2 & R3 --> Selector[Selector Node<br/>Field Selection]
    
    Selector --> Generator[Query Generator Node]
    
    Generator --> Query[Generated MongoDB Query<br/>db.b2btransaction.find]
    
    Query --> Executor[Query Executor Node]
    
    Executor --> MongoDB[(MongoDB Database<br/>eemdb_ts1.b2btransaction)]
    
    MongoDB --> Results[Query Results<br/>Matching Transactions]
    
    Results --> Parser[Output Parser Node]
    
    Parser --> NL[Natural Language Response<br/>Found 5 transactions for DBSMX<br/>with REC-DGI subtype...]
    
    NL --> End([User receives formatted answer])
    
    style Semantic fill:#e1f5ff
    style Rules fill:#fff4e1
    style Query fill:#e8f5e9
    style Start fill:#f3e5f5
    style End fill:#f3e5f5
    style MongoDB fill:#ffebee
```

### ASCII Diagram (For presentations/documents)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  USER QUERY: "Get DBS transactions, REC-DGI type, last 30 days"        │
└──────────────────────────────┬──────────────────────────────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │   ROUTER NODE        │
                    │  (Query Analysis)    │
                    └──────────┬───────────┘
                               ▼
        ┌──────────────────────────────────────────────────┐
        │                                                  │
        ▼                                                  ▼
┌────────────────────────────┐              ┌────────────────────────────┐
│  LAYER 1: SEMANTIC MODELS  │              │  LAYER 2: MONGODB RULES    │
│  ========================  │              │  ======================    │
│                            │              │                            │
│  Field Definitions:        │              │  Field Priorities:         │
│  • partnerName: string     │              │  • essential_fields        │
│  • transactionSubType: str │              │  • high_priority_fields    │
│  • creationDate: datetime  │              │                            │
│                            │              │  Query Type Rules:         │
│  Sample Values:            │              │  • max_collections: 1      │
│  • DBS, DHLUS, DBSMX       │              │  • max_fields: 25          │
│  • REC-DGI, SSG, DGI       │              │  • relevance: 0.8          │
│                            │              │                            │
│  ↓ MAPPING RESULT:         │              │  Custom Instructions:      │
│  • DBS → partnerName       │              │  • Use ISODate()           │
│  • REC-DGI → txnSubType    │              │  • Case-insensitive regex  │
│  • 30 days → creationDate  │              │  • $match first            │
└────────────┬───────────────┘              └────────────┬───────────────┘
             │                                           │
             └───────────────────┬───────────────────────┘
                                 ▼
                    ┌────────────────────────┐
                    │   SELECTOR NODE        │
                    │  (Field Selection)     │
                    │  Selected: 10 fields   │
                    └────────────┬───────────┘
                                 ▼
                    ┌────────────────────────┐
                    │  QUERY GENERATOR NODE  │
                    │  (MongoDB Query Build) │
                    └────────────┬───────────┘
                                 ▼
        ┌────────────────────────────────────────────────┐
        │  GENERATED QUERY (Optimized & Validated):     │
        │  ============================================  │
        │  db.b2btransaction.find({                     │
        │    "partnerName": {                           │
        │      $regex: "DBS",                           │
        │      $options: "i"                            │
        │    },                                         │
        │    "transactionSubType": "REC-DGI",           │
        │    "creationDate": {                          │
        │      $gte: ISODate("2025-12-14")              │
        │    }                                          │
        │  })                                           │
        └────────────────────┬───────────────────────────┘
                             ▼
                ┌────────────────────────┐
                │  QUERY EXECUTOR NODE   │
                │  (Execute on MongoDB)  │
                └────────────┬───────────┘
                             ▼
                ┌────────────────────────┐
                │   MONGODB DATABASE     │
                │  eemdb_ts1.appuser     │
                │   b2btransaction       │
                └────────────┬───────────┘
                             ▼
                ┌────────────────────────┐
                │    QUERY RESULTS       │
                │  [5 matching txns]     │
                └────────────┬───────────┘
                             ▼
                ┌────────────────────────┐
                │  OUTPUT PARSER NODE    │
                │ (Format to Natural     │
                │  Language)             │
                └────────────┬───────────┘
                             ▼
        ┌────────────────────────────────────────────────┐
        │  NATURAL LANGUAGE RESPONSE:                   │
        │  ============================================  │
        │  Found 5 transactions for DBSMX partner:      │
        │  • Requisition: 12329609                      │
        │  • Type: REC-DGI                              │
        │  • Date: 2025-12-31                           │
        │  • Status: COMPLETE                           │
        └────────────────────────────────────────────────┘
```

### Simplified Flow Diagram

```
┌──────────┐     ┌─────────────┐     ┌──────────────┐     ┌──────────┐     ┌────────┐
│          │     │  SEMANTIC   │     │   MONGODB    │     │          │     │        │
│   USER   │────▶│   MODELS    │────▶│    RULES     │────▶│  QUERY   │────▶│ MONGO  │
│  QUERY   │     │  (Business  │     │ (Governance) │     │ EXECUTOR │     │   DB   │
│          │     │   Context)  │     │              │     │          │     │        │
└──────────┘     └─────────────┘     └──────────────┘     └──────────┘     └───┬────┘
                                                                                │
                                                                                ▼
┌──────────┐     ┌─────────────┐                                         ┌──────────┐
│          │     │   OUTPUT    │                                         │          │
│   USER   │◀────│   PARSER    │◀────────────────────────────────────────│ RESULTS  │
│ RESPONSE │     │  (Format)   │                                         │          │
└──────────┘     └─────────────┘                                         └──────────┘
```

## Color-Coded Layers Legend

- 🔵 **Blue** = Semantic Models Layer (Business Context)
- 🟡 **Yellow** = MongoDB Rules Layer (Query Governance)
- 🟢 **Green** = Generated Query (Validated Output)
- 🔴 **Red** = Database Execution
- 🟣 **Purple** = User Interaction Points

## Key Takeaways from Architecture

1. **Dual-Layer Validation**: Every query passes through both semantic and rules layers
2. **Separation of Concerns**: Business context (WHAT) separate from query optimization (HOW)
3. **LangGraph Nodes**: Each step is a specialized node in the graph
4. **Guaranteed Optimization**: Rules layer ensures production-grade queries
5. **Transparency**: Debug mode shows exact flow through each node
