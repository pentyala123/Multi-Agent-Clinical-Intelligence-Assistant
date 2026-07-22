import unittest

from life_sciences_chatbot.llm import LocalDemonstrationModel
from life_sciences_chatbot.models import ChatRequestData
from life_sciences_chatbot.retrieval import SyntheticKnowledgeBase
from life_sciences_chatbot.service import ChatbotService


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.service = ChatbotService(
            SyntheticKnowledgeBase("data/synthetic/knowledge.json"),
            LocalDemonstrationModel(),
        )

    def test_returns_route_sources_and_disclaimer(self):
        result = self.service.chat(ChatRequestData("What is tracked for a clinical trial?", "S1"))
        self.assertEqual(result.routed_to, "clinical_trials")
        self.assertTrue(result.sources)
        self.assertIn("not medical", result.disclaimer.casefold())
        self.assertEqual(result.session_id, "S1")

    def test_rejects_empty_query(self):
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            self.service.chat(ChatRequestData("  "))


if __name__ == "__main__":
    unittest.main()
