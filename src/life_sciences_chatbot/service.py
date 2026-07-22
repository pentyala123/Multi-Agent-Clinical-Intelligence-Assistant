from __future__ import annotations

from .llm import LanguageModel, configured_model
from .models import ChatRequestData, ChatResult
from .retrieval import SyntheticKnowledgeBase
from .routing import route_query
from .schemas import AGENT_TOPICS, MCP_SCHEMAS


DISCLAIMER = (
    "Educational demonstration only. Not medical, clinical, legal, safety, or regulatory advice. "
    "Verify all information with qualified professionals and authoritative sources."
)


class ChatbotService:
    def __init__(self, knowledge_base: SyntheticKnowledgeBase, model: LanguageModel | None = None) -> None:
        self.knowledge_base = knowledge_base
        self.model = model or configured_model()

    def chat(self, request: ChatRequestData) -> ChatResult:
        query = request.query.strip()
        if not query:
            raise ValueError("query cannot be empty")
        if len(query) > 4000:
            raise ValueError("query must contain at most 4000 characters")
        domain = route_query(query)
        documents = self.knowledge_base.search(query, domain=domain)
        context = "\n\n".join(
            f"[{document.title}] {document.content} (Source: {document.source})"
            for document in documents
        )
        schema = MCP_SCHEMAS.get(domain, {})
        instructions = (
            f"You are the {domain.replace('_', ' ')} specialist in a life-sciences assistant. "
            f"Scope: {AGENT_TOPICS[domain]}. Use only the retrieved context. Never invent citations. "
            f"If evidence is insufficient, say so. Applicable output schema: {schema}. {DISCLAIMER}"
        )
        response = self.model.answer(instructions=instructions, query=query, context=context)
        return ChatResult(
            response=response,
            routed_to=domain,
            sources=[document.source for document in documents],
            session_id=request.session_id,
            disclaimer=DISCLAIMER,
        )
