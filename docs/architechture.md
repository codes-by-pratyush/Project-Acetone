                 ┌──────────────────────┐
                 │   React Dashboard    │
                 │ React + TypeScript   │
                 └──────────┬───────────┘
                            │
                       REST/WebSocket
                            │
                 ┌──────────▼───────────┐
                 │    FastAPI Gateway   │
                 │ Auth + RBAC + APIs   │
                 └──────────┬───────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
     Case Service     Tracing Engine     Reporting
          │                 │                 │
          ▼                 ▼                 ▼
      PostgreSQL          Neo4j           Redis
                            ▲
                            │
                     Blockchain APIs
                  Alchemy / Etherscan