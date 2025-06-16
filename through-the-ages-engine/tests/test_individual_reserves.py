#!/usr/bin/env python3
"""
Test individual player reserves system
Verifies that each player has their own yellow and blue token reserves
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from game.game_state import GameState
from tests.test_utils import prevent_revolt_for_testing, verify_no_revolt

def test_individual_reserves():
    """Test that each player has individual yellow and blue reserves"""
    print("=== Test: Individual Player Reserves ===")

    # Create game with 3 players
    game = GameState()
    game.initialize_game(
        players=["Alice", "Bob", "Charlie"],
        bot_types=["human", "human", "human"]
    )

    print(f"✓ Game initialized with {len(game.players)} players")

    # Verify each player has their own reserves
    for i, player in enumerate(game.players):
        player_id = player.player_id
        board = player.board

        print(f"\n--- Player {player_id}: {player.name} ---")
        print(f"Yellow reserves: {board.yellow_reserves}")
        print(f"Blue reserves: {board.blue_reserves}")
        print(f"Resources: {board.resources}")
        print(f"Population cost: {board.get_population_cost()}")        # Test initial state - using new group system
        # Check that player has yellow tokens available in groups
        has_available_tokens = board._has_available_yellow_tokens()
        assert has_available_tokens, f"Player {player_id} should have available yellow tokens in groups"

        assert board.yellow_reserves['available_workers'] == 1, f"Player {player_id} should start with 1 available worker"

        # Check that groups are properly initialized
        assert len(board.yellow_reserves['groups']) == 8, f"Player {player_id} should have 8 yellow token groups"

        # Check that blue groups are properly initialized
        assert len(board.blue_reserves['groups']) == 3, f"Player {player_id} should have 3 blue token groups"

        print(f"✓ Player {player_id} has correct initial reserves")

    # Test population increase for Player 1
    print(f"\n--- Testing Population Increase ---")
    player1 = game.players[0]
    player1_board = player1.board    # Give player 1 enough food
    player1_board.resources['food'] = 10

    # Track initial state using new group system
    initial_has_tokens = player1_board._has_available_yellow_tokens()
    initial_available = player1_board.yellow_reserves['available_workers']
    initial_food = player1_board.resources['food']
    cost = player1_board.get_population_cost()

    print(f"Player 1 before increase: has tokens in groups: {initial_has_tokens}, {initial_available} available workers, {initial_food} food")
    print(f"Cost to increase: {cost} food")

    # Increase population
    success = player1_board.increase_population(cost)
    assert success, "Population increase should succeed"

    print(f"Player 1 after increase: {player1_board.yellow_reserves['available_workers']} available workers, {player1_board.resources['food']} food")

    # Verify changes only affected Player 1
    assert player1_board.yellow_reserves['available_workers'] == initial_available + 1
    assert player1_board.resources['food'] == initial_food - cost

    print("✓ Player 1 population increased correctly")    # Verify other players unchanged
    for i, player in enumerate(game.players[1:], 2):
        assert player.board._has_available_yellow_tokens(), f"Player {i} should still have available tokens"
        assert player.board.yellow_reserves['available_workers'] == 1, f"Player {i} should still have 1 available worker"
        print(f"✓ Player {i} reserves unchanged")

    print("\n=== Individual Reserves Test PASSED ===")
    return True

def test_worker_assignment():
    """Test worker assignment to technologies"""
    print("\n=== Test: Worker Assignment ===")

    game = GameState()
    game.initialize_game(["Player1"], ["human"])

    player = game.players[0]
    board = player.board    # Assign worker to Agriculture (already has 2, so will become 3)
    initial_available = board.yellow_reserves['available_workers']
    initial_agricultura = board.yellow_reserves['technology_workers']['Agricultura']
    success = board.assign_worker_to_technology('Agricultura')

    assert success, "Worker assignment should succeed"
    assert board.yellow_reserves['available_workers'] == initial_available - 1
    assert board.yellow_reserves['technology_workers']['Agricultura'] == initial_agricultura + 1

    print("✓ Worker successfully assigned to Agriculture")

    # PREVENCIÓN REVUELTAS PARA PRUEBAS
    # Ajusta felicidad para evitar revueltas durante testing
    print(f"Available workers: {board.yellow_reserves['available_workers']}")
    print(f"Happiness points: {board.indicators['happiness']}")

    prevent_revolt_for_testing(board)
    verify_no_revolt(board)    # Test production calculation
    production = board.calculate_production()
    print(f"Production: {production}")

    # Should have no revolt and some food production
    assert not board.check_revolt_condition(), "Should not have revolt with proper worker assignment"
    assert production['food'] >= 1, "Should produce at least 1 food from Agriculture"
    print("✓ Production calculation working without revolt")

    return True

def test_corruption_system():
    """Test blue token corruption system"""
    print("\n=== Test: Corruption System ===")

    game = GameState()
    game.initialize_game(["Player1"], ["human"])

    player = game.players[0]
    board = player.board    # Simulate using blue tokens to trigger corruption
    # We need to make some groups unoccupied to trigger corruption penalty
    # Remove tokens from the first group to make it unoccupied
    board.blue_reserves['groups'][0]['tokens'] = 0
    board.blue_reserves['groups'][0]['occupied'] = False

    penalty = board.calculate_corruption_penalty()
    print(f"Corruption penalty with first group empty: {penalty}")

    assert penalty > 0, "Should have corruption penalty with unoccupied blue group"
    print("✓ Corruption system working")

    return True

if __name__ == "__main__":
    print("THROUGH THE AGES - Individual Reserves Test")
    print("=" * 50)

    try:
        test_individual_reserves()
        test_worker_assignment()
        test_corruption_system()

        print("\n" + "=" * 50)
        print("✓ ALL INDIVIDUAL RESERVES TESTS PASSED!")
        print("✓ Each player now has their own yellow/blue reserves")
        print("✓ Population, workers, and corruption work individually")

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
