# Architecture

The public implementation separates routing, retrieval, schema context, response generation, and delivery so each component can be evaluated independently.

```mermaid
flowchart LR
    A[Question] --> B[Router]
    B --> C[Local synthetic retriever]
    C --> D[Domain schema]
    D --> E[Specialist instruction]
    E --> F{API key configured?}
    F -->|No| G[Offline deterministic response]
    F -->|Yes| H[OpenAI Responses API]
    G --> I[FastAPI response]
    H --> I
```

## Production evolution

Replace the synthetic retriever with an authorized vector store, add document provenance and freshness checks, protect the API with authentication and rate limits, keep secrets in a managed vault, evaluate routing and groundedness, detect prompt injection, log safely, monitor cost and latency, and require qualified human review.
