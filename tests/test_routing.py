import unittest

from life_sciences_chatbot.routing import route_query


class RoutingTests(unittest.TestCase):
    def test_routes_clinical_trial_query(self):
        self.assertEqual(route_query("What are Phase 3 trial endpoints?"), "clinical_trials")

    def test_routes_regulatory_query(self):
        self.assertEqual(route_query("Which FDA submission is relevant?"), "regulatory")

    def test_uses_general_fallback(self):
        self.assertEqual(route_query("Explain protein folding"), "general")


if __name__ == "__main__":
    unittest.main()
