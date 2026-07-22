from __future__ import annotations


KEYWORDS = {
    "clinical_trials": {"trial", "phase", "eligibility", "study", "endpoint", "sponsor"},
    "drug_interactions": {"interaction", "contraindication", "drug", "dose", "pharmacokinetic"},
    "regulatory": {"fda", "ema", "regulatory", "nda", "bla", "510k", "ich", "submission"},
    "pharmacovigilance": {"faers", "adverse", "safety", "signal", "post-market", "seriousness"},
}


def route_query(query: str) -> str:
    """Return the highest-scoring specialist route using explainable keyword matching."""

    normalized = query.casefold()
    scores = {
        topic: sum(keyword in normalized for keyword in keywords)
        for topic, keywords in KEYWORDS.items()
    }
    best = max(scores, key=scores.get)
    return best if scores[best] else "general"
