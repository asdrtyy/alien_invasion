import unittest
import os
import sys
from game_state import GameState

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class TestGameState(unittest.TestCase):
    def setUp(self):
        self.state = GameState(level=1, lives=3, score=0)

    def test_add_score(self):
        self.state.add_score(100)
        self.assertEqual(self.state.score, 100)
        self.state.add_score(50)
        self.assertEqual(self.state.score, 150)

    def test_high_score(self):
        self.state.add_score(1000)
        self.assertGreaterEqual(self.state.high_score, 1000)

    def test_lose_life(self):
        self.state.lose_life()
        self.assertEqual(self.state.lives, 2)
        self.state.lose_life()
        self.state.lose_life()
        self.assertTrue(self.state.game_over)

    def test_next_level(self):
        self.state.next_level()
        self.assertEqual(self.state.level, 2)

    def test_reset(self):
        self.state.add_score(100)
        self.state.lose_life()
        self.state.reset(level=1, lives=3, score=0)
        self.assertEqual(self.state.level, 1)
        self.assertEqual(self.state.lives, 3)
        self.assertEqual(self.state.score, 0)


if __name__ == "__main__":
    unittest.main()
