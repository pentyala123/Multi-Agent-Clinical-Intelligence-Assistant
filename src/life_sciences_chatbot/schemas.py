from __future__ import annotations


AGENT_TOPICS = {
    "clinical_trials": "trial phases, eligibility, study status, sponsors, and endpoints",
    "drug_interactions": "drug interactions, contraindications, pharmacokinetics, and adverse effects",
    "regulatory": "FDA or EMA guidance, submissions, and ICH-aligned compliance",
    "pharmacovigilance": "adverse-event reporting, signal detection, and post-market surveillance",
    "general": "general life-sciences questions outside the specialist domains",
}

MCP_SCHEMAS = {
    "clinical_trials": {
        "schema_version": "1.0",
        "required_fields": ["trial_id", "phase", "indication", "sponsor", "status"],
        "output_format": "structured_trial_summary",
    },
    "drug_interactions": {
        "schema_version": "1.0",
        "required_fields": ["drug_a", "drug_b", "interaction_type", "severity", "mechanism"],
        "output_format": "interaction_report",
    },
    "regulatory": {
        "schema_version": "1.0",
        "required_fields": ["submission_type", "agency", "guideline_reference", "applicability"],
        "output_format": "regulatory_summary",
    },
    "pharmacovigilance": {
        "schema_version": "1.0",
        "required_fields": ["event", "seriousness", "expectedness", "source"],
        "output_format": "safety_signal_summary",
    },
}
