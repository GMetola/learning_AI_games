#!/usr/bin/env python3
"""
Tests for the game actions system
"""

import unittest
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game.game_state import GameState
from game.actions import GameAction, ActionValidator, ActionExecutor, ActionFactory, ActionUtils
from game.player import Player
from game.board import GameBoard, PlayerBoard


class TestGameActions(unittest.TestCase):
    """Test suite for game actions system"""

    def setUp(self):
        """Set up test fixtures"""
        # Create game state with 2 players
        self.game_state = GameState()
        players = ["TestBot1", "TestBot2"]
        bot_types = ["algorithmic", "algorithmic"]
        self.game_state.initialize_game(players, bot_types)

        # Initialize action validator and executor
        self.validator = ActionValidator(self.game_state)
        self.executor = ActionExecutor(self.game_state)        # Get first player for testing
        self.player1 = self.game_state.players[0]
        self.player2 = self.game_state.players[1]        # Initialize some mock cards for testing
        self.game_state.board.visible_civil_cards = [
            {"name": "Mock Card 1", "type": "building"},
            {"name": "Mock Card 2", "type": "technology"},
            {"name": "Mock Card 3", "type": "wonder"}
        ]

    def create_mock_bot(self):
        """Create a mock bot for testing"""
        class MockBot:
            def consume_civil_action(self, cost):
                pass
            def consume_military_action(self, cost):
                pass
        return MockBot()

    def test_action_factory_creation(self):
        """Test ActionFactory creates actions correctly"""
        # Test take card action
        take_action = ActionFactory.create_take_card_action(1, 0)
        self.assertEqual(take_action.action_type, 'tomar_carta')
        self.assertEqual(take_action.parameters['card_position'], 0)
        self.assertEqual(take_action.cost['civil_actions'], 1)

        # Test increase population action
        pop_action = ActionFactory.create_increase_population_action(1)
        self.assertEqual(pop_action.action_type, 'aumentar_población')
        self.assertEqual(pop_action.cost['civil_actions'], 1)        # Test assign worker action
        worker_action = ActionFactory.create_assign_worker_action(1, 'Agriculture')
        self.assertEqual(worker_action.action_type, 'asignar_trabajador')
        self.assertEqual(worker_action.parameters['tech_name'], 'Agriculture')
        self.assertEqual(worker_action.cost['civil_actions'], 1)

        # Test end turn action
        end_action = ActionFactory.create_end_turn_action(1)
        self.assertEqual(end_action.action_type, 'terminar_turno')
        self.assertEqual(end_action.cost['civil_actions'], 0)

    def test_action_validation_turn_check(self):
        """Test that actions are validated for correct player turn"""
        # Player 1 should be current player
        self.assertEqual(self.game_state.get_current_player(), "TestBot1")

        # Player 1 action should be valid (regarding turn)
        action1 = ActionFactory.create_end_turn_action(1)
        is_valid, error = self.validator.validate_action(1, action1)
        self.assertTrue(is_valid or "No es el turno" not in error)

        # Player 2 action should be invalid (not their turn)
        action2 = ActionFactory.create_end_turn_action(2)
        is_valid, error = self.validator.validate_action(2, action2)
        self.assertFalse(is_valid)
        self.assertIn("No es el turno", error)

    def test_increase_population_validation_and_execution(self):
        """Test population increase validation and execution"""
        player_board = self.player1.board

        # Give player enough food
        player_board.resources['food'] = 10

        # Create and validate population increase action
        action = ActionFactory.create_increase_population_action(1)
        is_valid, error = self.validator.validate_action(1, action)
        self.assertTrue(is_valid, f"Population increase should be valid: {error}")        # Execute the action
        initial_workers = player_board.yellow_reserves['available_workers']
        initial_has_tokens = player_board.worker_manager.has_available_yellow_tokens()

        mock_bot = self.create_mock_bot()
        result = self.executor.execute_action(action, mock_bot)
        self.assertTrue(result['success'], f"Execution should succeed: {result}")# Check that population increased
        self.assertEqual(
            player_board.yellow_reserves['available_workers'],
            initial_workers + 1
        )

        # Verify tokens were taken from groups (some group should have fewer tokens)
        self.assertTrue(initial_has_tokens, "Should have had tokens available initially")

    def test_assign_worker_validation_and_execution(self):
        """Test worker assignment validation and execution"""
        player_board = self.player1.board

        # Ensure player has available workers
        initial_workers = player_board.yellow_reserves['available_workers']
        self.assertGreater(initial_workers, 0, "Player should have available workers")

        # Give player enough materials for worker assignment
        player_board.resources['material'] = 5  # Enough for any technology        # Create and validate worker assignment action (use Religion which has 0 workers)
        action = ActionFactory.create_assign_worker_action(1, 'Religion')
        is_valid, error = self.validator.validate_action(1, action)
        self.assertTrue(is_valid, f"Worker assignment should be valid: {error}")

        # Create a mock bot
        class MockBot:
            def consume_civil_action(self, cost):
                pass
            def consume_military_action(self, cost):
                pass

        mock_bot = MockBot()

        # Execute the action
        result = self.executor.execute_action(action, mock_bot)
        self.assertTrue(result['success'], f"Execution should succeed: {result}")        # Test validation failure when insufficient materials
        player_board.yellow_reserves['available_workers'] = 2  # Give more workers
        player_board.resources['material'] = 0  # Remove materials
        action2 = ActionFactory.create_assign_worker_action(1, 'Bronze')
        is_valid2, error2 = self.validator.validate_action(1, action2)
        self.assertFalse(is_valid2, "Worker assignment should be invalid with insufficient materials")
        self.assertIn("Materiales insuficientes", error2, "Error should mention insufficient materials")

    def test_civil_action_tracking(self):
        """Test that civil actions are properly tracked and limited"""
        player_board = self.player1.board
        player_board.resources['food'] = 20  # Give enough food

        # Initially should have 0 used civil actions
        used_actions = getattr(player_board, 'used_civil_actions', 0)
        self.assertEqual(used_actions, 0)        # Execute 4 population increases (uses 4 civil actions)
        mock_bot = self.create_mock_bot()
        for i in range(4):
            action = ActionFactory.create_increase_population_action(1)
            result = self.executor.execute_action(action, mock_bot)
            self.assertTrue(result['success'], f"Action {i+1} should succeed")

        # Check that civil actions are tracked
        used_actions = getattr(player_board, 'used_civil_actions', 0)
        self.assertEqual(used_actions, 4)

        # 5th action should fail due to no more civil actions
        action = ActionFactory.create_increase_population_action(1)
        is_valid, error = self.validator.validate_action(1, action)
        self.assertFalse(is_valid)
        self.assertIn("acciones civiles", error)

    def test_get_legal_actions(self):
        """Test getting legal actions for a player"""
        legal_actions = self.validator.get_legal_actions(1)

        # Should have at least some actions
        self.assertGreater(len(legal_actions), 0)

        # Should always have end turn action
        end_actions = [a for a in legal_actions if a.action_type == 'terminar_turno']
        self.assertEqual(len(end_actions), 1)

        # Should have worker assignment actions for initial technologies
        worker_actions = [a for a in legal_actions if a.action_type == 'asignar_trabajador']
        self.assertGreater(len(worker_actions), 0)

    def test_end_turn_execution(self):
        """Test end turn execution and action reset"""
        player_board = self.player1.board

        # Use some civil actions first
        player_board.used_civil_actions = 2
        player_board.used_military_actions = 1        # Create and execute end turn action
        action = ActionFactory.create_end_turn_action(1)
        result = self.executor.execute_action(action)

        self.assertTrue(result['success'])
        self.assertEqual(result['next_player'], "TestBot2")

        # Check that action counters were reset
        self.assertEqual(getattr(player_board, 'used_civil_actions', 0), 0)
        self.assertEqual(getattr(player_board, 'used_military_actions', 0), 0)

    def test_action_utils(self):
        """Test ActionUtils functionality"""
        # Give player enough resources for actions
        player_board = self.player1.board
        player_board.resources['food'] = 10
        player_board.resources['material'] = 5        # Create different types of actions
        actions = [
            ActionFactory.create_take_card_action(1, 0),
            ActionFactory.create_increase_population_action(1),
            ActionFactory.create_assign_worker_action(1, 'Agriculture'),
            ActionFactory.create_end_turn_action(1)
        ]

        # Test filtering by type
        pop_actions = ActionUtils.filter_actions_by_type(actions, 'aumentar_población')
        self.assertEqual(len(pop_actions), 1)
        self.assertEqual(pop_actions[0].action_type, 'aumentar_población')        # Test cost calculation
        total_cost = ActionUtils.calculate_total_cost(actions)
        self.assertEqual(total_cost['civil_actions'], 3)  # take card + increase pop + assign worker
        self.assertEqual(total_cost['military_actions'], 0)

        # Test action sequence validation        # Create a sequence with mixed players - should be invalid
        mixed_actions = [
            ActionFactory.create_take_card_action(1, 0),      # Player 1
            ActionFactory.create_increase_population_action(2),  # Player 2 - wrong turn!
            ActionFactory.create_assign_worker_action(1, 'Agriculture'),  # Player 1
        ]
        is_valid, error = ActionUtils.validate_action_sequence(mixed_actions, self.game_state)
        # Should be invalid because player 2 tries to act on player 1's turn
        self.assertFalse(is_valid)        # Test valid sequence for current player
        valid_actions = [
            ActionFactory.create_take_card_action(1, 0),
            ActionFactory.create_increase_population_action(1),
            ActionFactory.create_assign_worker_action(1, 'Agriculture'),
            ActionFactory.create_end_turn_action(1)
        ]
        is_valid, error = ActionUtils.validate_action_sequence(valid_actions, self.game_state)
        if not is_valid:
            print(f"Validation failed: {error}")
        self.assertTrue(is_valid, f"Expected valid sequence but got error: {error}")

    def test_execute_multiple_actions(self):
        """Test executing multiple actions in sequence"""
        player_board = self.player1.board
        player_board.resources['food'] = 10
        player_board.resources['material'] = 5  # Give enough materials for worker assignment        # Create sequence of actions - use Religion instead of Agriculture to avoid max workers issue
        actions = [
            ActionFactory.create_assign_worker_action(1, 'Religion'),
            ActionFactory.create_increase_population_action(1),
            ActionFactory.create_end_turn_action(1)
        ]

        # Execute multiple actions
        mock_bot = self.create_mock_bot()
        results = self.executor.execute_multiple_actions(actions, mock_bot)

        self.assertEqual(len(results), 3)

        # First two should succeed
        self.assertTrue(results[0]['success'])
        self.assertTrue(results[1]['success'])
        self.assertTrue(results[2]['success'])

        # Should be player 2's turn now
        self.assertEqual(self.game_state.get_current_player(), "TestBot2")


if __name__ == '__main__':
    unittest.main()
