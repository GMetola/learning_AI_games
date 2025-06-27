import unittest
from src.bots.algorithmic_bot import AlgorithmicBot
from src.bots.ai_bot import AIBot
from src.game.game_state import GameState

class TestBots(unittest.TestCase):

    def setUp(self):
        self.game_state = GameState()
        # Initialize game with players
        players = ["TestBot1", "TestBot2"]
        bot_types = ["algorithmic", "ai"]
        self.game_state.initialize_game(players, bot_types)

        self.algorithmic_bot = AlgorithmicBot("bot1", "AlgoBot")
        self.ai_bot = AIBot("bot2", "AIBot")

    def test_algorithmic_bot_strategy(self):
        # Test the algorithmic bot's strategy implementation
        initial_state = self.game_state.get_state()
        available_actions = [
            {"action_type": "tomar_carta", "card_position": 0},
            {"action_type": "aumentar_poblacion"},
            {"action_type": "terminar_turno"}
        ]
        action = self.algorithmic_bot.make_move(initial_state, available_actions)
        self.assertIsNotNone(action, "Algorithmic bot should return a valid action")

    def test_ai_bot_learning(self):
        # Test the AI bot's learning mechanism
        initial_state = self.game_state.get_state()
        available_actions = [
            {"action_type": "tomar_carta", "card_position": 0},
            {"action_type": "aumentar_poblacion"},
            {"action_type": "terminar_turno"}
        ]
        action = self.ai_bot.make_move(initial_state, available_actions)
        self.assertIsNotNone(action, "AI bot should return a valid action")

        # Test learning from reward
        self.ai_bot.learn_from_reward(1.0, initial_state)

    def test_bot_interaction(self):
        # Test interaction between bots and game state
        initial_state = self.game_state.get_state()
        available_actions = [
            {"action_type": "tomar_carta", "card_position": 0},
            {"action_type": "aumentar_poblacion"},
            {"action_type": "terminar_turno"}
        ]
        algo_action = self.algorithmic_bot.make_move(initial_state, available_actions)
        ai_action = self.ai_bot.make_move(initial_state, available_actions)

        self.assertIsNotNone(algo_action, "Algorithmic bot should provide an action")
        self.assertIsNotNone(ai_action, "AI bot should provide an action")

if __name__ == '__main__':
    unittest.main()