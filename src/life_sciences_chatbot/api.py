from __future__ import annotations

import os
from pathlib import Path

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel, Field
except ImportError as exc:  # pragma: no cover
    raise RuntimeError("Install API dependencies with: pip install -e '.[api]'") from exc

from .models import ChatRequestData
from .retrieval import SyntheticKnowledgeBase
from .service import ChatbotService
from .schemas import AGENT_TOPICS


knowledge_file = Path(os.getenv("KNOWLEDGE_DATA", "data/synthetic/knowledge.json"))
service = ChatbotService(SyntheticKnowledgeBase(knowledge_file))
app = FastAPI(
    title="Life Sciences Multi-Agent Chatbot",
    version="1.0.0",
    description="Public portfolio implementation using synthetic reference content.",
)


class ChatRequest(BaseModel):
    query: str = Field(min_length=1, max_length=4000)
    session_id: str | None = Field(default=None, max_length=100)


@app.get("/health")
def health() -> dict[str, object]:
    return {"status": "ok", "agents": list(AGENT_TOPICS), "mode": "portfolio-demo"}


@app.post("/chat")
def chat(request: ChatRequest) -> dict[str, object]:
    try:
        return service.chat(ChatRequestData(**request.model_dump())).to_dict()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
