import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from level_manager import LevelManager


class TestLevelManager(unittest.TestCase):
    def setUp(self):
        self.lm = LevelManager()

    def test_get_level_params(self):
        params1 = self.lm.get_level_params(1)
        self.assertIn("alien_health", params1)
        self.assertIn("rows", params1)
        params2 = self.lm.get_level_params(2)
        self.assertIn("alien_health", params2)
        self.assertIn("rows", params2)

    def test_add_level(self):
        self.lm.add_level(99, {"alien_health": 10, "rows": 10})
        params = self.lm.get_level_params(99)
        self.assertEqual(params["alien_health"], 10)
        self.assertEqual(params["rows"], 10)


if __name__ == "__main__":
    unittest.main()
