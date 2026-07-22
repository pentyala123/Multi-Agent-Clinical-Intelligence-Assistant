from __future__ import annotations

import os
from typing import Protocol


class LanguageModel(Protocol):
    def answer(self, *, instructions: str, query: str, context: str) -> str: ...


class LocalDemonstrationModel:
    """Offline fallback that makes the repository runnable without an API key."""

    def answer(self, *, instructions: str, query: str, context: str) -> str:
        if not context:
            return (
                "No relevant synthetic reference content was found. Consult an authoritative "
                "regulatory, clinical, or scientific source before making a decision."
            )
        return (
            "Based on the synthetic reference material, the relevant points are:\n\n"
            f"{context}\n\n"
            "This demonstration response requires verification against authoritative sources."
        )


class OpenAIResponsesModel:
    """Optional OpenAI Responses API adapter; reads credentials only from the environment."""

    def __init__(self) -> None:
        from openai import OpenAI

        self.client = OpenAI()
        self.model = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")

    def answer(self, *, instructions: str, query: str, context: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            instructions=instructions,
            input=f"User question:\n{query}\n\nRetrieved context:\n{context}",
        )
        return response.output_text


def configured_model() -> LanguageModel:
    return OpenAIResponsesModel() if os.getenv("OPENAI_API_KEY") else LocalDemonstrationModel()
