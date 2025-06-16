#!/usr/bin/env python3
"""
Test script to verify the new card collections in PlayerBoard
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game.board import PlayerBoard
from game.card_loader import load_all_cards

def test_player_board_card_collections():
    """Test the new card collections in PlayerBoard"""
    print("=== Testing PlayerBoard Card Collections ===")

    # Create a player board
    player_board = PlayerBoard(player_id=1)

    # Test unique attributes
    print(f"Leader: {player_board.leader}")
    print(f"Government: {player_board.government}")
    if player_board.government:
        print(f"  - Civil Actions: {player_board.government.civil_actions}")
        print(f"  - Military Actions: {player_board.government.military_actions}")

    # Test multiple attributes (lists)
    print(f"\nWonders: {len(player_board.wonders)} cards")
    print(f"Monuments: {len(player_board.monuments)} cards")
    print(f"Hand Cards: {len(player_board.hand_cards)} cards")
    print(f"Production Buildings: {len(player_board.production_buildings)} cards")
    print(f"Urban Buildings: {len(player_board.urban_buildings)} cards")

    # Show initial buildings
    print(f"\nInitial Production Buildings:")
    for building in player_board.production_buildings:
        print(f"  - {building.name} (Age {building.age})")
        if hasattr(building, 'production'):
            print(f"    Production: {building.production}")

    print(f"\nInitial Urban Buildings:")
    for building in player_board.urban_buildings:
        print(f"  - {building.name} (Age {building.age})")
        if hasattr(building, 'production'):
            print(f"    Production: {building.production}")

    # Test methods
    print(f"\nAll Buildings: {len(player_board.get_all_buildings())} total")

    # Test building lookup
    agriculture = player_board.get_building_by_name('Agriculture')
    print(f"Agriculture building: {agriculture}")

    philosophy = player_board.get_building_by_name('Philosophy')
    print(f"Philosophy building: {philosophy}")

    # Test has_technology
    print(f"Has Agriculture: {player_board.has_technology('Agriculture')}")
    print(f"Has Bronze: {player_board.has_technology('Bronze')}")
    print(f"Has Irrigation: {player_board.has_technology('Irrigation')}")

def test_adding_cards():
    """Test adding new cards to collections"""
    print("\n=== Testing Adding Cards ===")

    player_board = PlayerBoard(player_id=1)

    # Load some cards to test with
    all_cards = load_all_cards()

    # Find some cards to test with
    test_wonder = None
    test_leader = None
    test_production = None

    for card in all_cards:
        if card.__class__.__name__ == 'Wonder' and test_wonder is None:
            test_wonder = card
        elif card.__class__.__name__ == 'Leader' and test_leader is None:
            test_leader = card
        elif card.__class__.__name__ == 'ProductionBuilding' and card.name != 'Agriculture' and card.name != 'Bronze' and test_production is None:
            test_production = card

        if test_wonder and test_leader and test_production:
            break

    # Test adding cards
    if test_wonder:
        print(f"Adding wonder: {test_wonder.name}")
        player_board.add_wonder(test_wonder)
        print(f"Wonders count: {len(player_board.wonders)}")

    if test_leader:
        print(f"Setting leader: {test_leader.name}")
        player_board.set_leader(test_leader)
        print(f"Leader: {player_board.leader}")

    if test_production:
        print(f"Adding production building: {test_production.name}")
        initial_count = len(player_board.production_buildings)
        player_board.add_production_building(test_production)
        print(f"Production buildings count: {initial_count} -> {len(player_board.production_buildings)}")
        print(f"Has {test_production.name}: {player_board.has_technology(test_production.name)}")

    # Test hand cards
    if test_production:
        print(f"Adding card to hand: {test_production.name}")
        player_board.add_card_to_hand(test_production)
        print(f"Hand cards count: {len(player_board.hand_cards)}")

        print(f"Removing card from hand: {test_production.name}")
        removed = player_board.remove_card_from_hand(test_production)
        print(f"Removed: {removed}, Hand cards count: {len(player_board.hand_cards)}")

def test_government_actions():
    """Test that government provides correct actions"""
    print("\n=== Testing Government Actions ===")

    player_board = PlayerBoard(player_id=1)

    print(f"Civil actions per turn: {player_board.get_civil_actions_per_turn()}")
    print(f"Military actions per turn: {player_board.get_military_actions_per_turn()}")
    print(f"Building limit: {player_board.get_building_limit()}")

    # Test using actions
    print(f"Civil actions available: {player_board.get_civil_actions_available()}")
    print(f"Military actions available: {player_board.get_military_actions_available()}")

    # Use some actions
    player_board.used_civil_actions = 2
    player_board.used_military_actions = 1

    print(f"After using 2 civil and 1 military action:")
    print(f"  Civil actions remaining: {player_board.get_civil_actions_available()}")
    print(f"  Military actions remaining: {player_board.get_military_actions_available()}")

if __name__ == "__main__":
    test_player_board_card_collections()
    test_adding_cards()
    test_government_actions()
    print("\n=== All tests completed ===")
