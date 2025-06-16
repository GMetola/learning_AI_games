import unittest
from src.bots.algorithmic_bot import AlgorithmicBot
from src.bots.ai_bot import AIBot
from src.game.game_state import GameState

class TestBots(unittest.TestCase):

    def setUp(self):
        self.game_state = GameState()
        self.algorithmic_bot = AlgorithmicBot("bot1", "AlgoBot")
        self.ai_bot = AIBot("bot2", "AIBot")

    def test_algorithmic_bot_strategy(self):
        # Test the algorithmic bot's strategy implementation
        initial_state = self.game_state.get_state()
        action = self.algorithmic_bot.make_move(initial_state)
        self.assertIsNotNone(action, "Algorithmic bot should return a valid action")

    def test_ai_bot_learning(self):
        # Test the AI bot's learning mechanism
        initial_state = self.game_state.get_state()
        self.ai_bot.learn_from_outcome(initial_state, success=True)
        action = self.ai_bot.make_move(initial_state)
        self.assertIsNotNone(action, "AI bot should return a valid action after learning")

    def test_bot_interaction(self):
        # Test interaction between bots and game state
        initial_state = self.game_state.get_state()
        algo_action = self.algorithmic_bot.make_move(initial_state)
        ai_action = self.ai_bot.make_move(initial_state)

        self.game_state.apply_action(algo_action)
        self.game_state.apply_action(ai_action)

        self.assertTrue(self.game_state.is_valid_state(), "Game state should be valid after bot actions")

if __name__ == '__main__':
    unittest.main()