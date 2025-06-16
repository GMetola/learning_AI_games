#!/usr/bin/env python3
"""
Test the new modular PlayerBoard system
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game.player_board_new import PlayerBoard
from game.card_classes import UrbanBuilding, ProductionBuilding, Government


def test_modular_player_board():
    """Test the new modular PlayerBoard system"""
    print("=== Testing Modular PlayerBoard System ===\n")

    # Create a player board
    player_board = PlayerBoard(1)

    print("1. Initial State:")
    summary = player_board.get_full_summary()
    print(f"   Cards: {summary['cards']}")
    print(f"   Resources: {summary['resources']['current_resources']}")
    print(f"   Workers: Available={summary['workers']['available_workers']}, Assigned={summary['workers']['technology_assignments']}")
    print(f"   Actions: Civil={summary['actions']['civil_actions']['available']}/{summary['actions']['civil_actions']['total']}")

    print("\n2. Adding Buildings:")

    # Test adding buildings
    try:
        # Add a custom urban building
        custom_theater = UrbanBuilding(
            name="Grand Theater",
            building_type="Theater",
            age="II",
            tech_cost=5,
            build_cost=6,
            production={'culture': 3, 'happy': 2},
            card_text="A magnificent theater"
        )
        player_board.add_urban_building(custom_theater)
        print("   ✓ Added custom urban building")

        # Add by name (should work if card exists)
        try:
            player_board.add_urban_building("Drama")
            print("   ✓ Added Drama by name")
        except Exception as e:
            print(f"   ⚠ Could not add Drama: {e}")

    except Exception as e:
        print(f"   ✗ Error adding buildings: {e}")

    print("\n3. Resource Management:")

    # Test resource operations
    initial_resources = player_board.resources.copy()
    print(f"   Initial: {initial_resources}")

    # Add some resources
    player_board.add_resources({'science': 3, 'culture': 2})
    print(f"   After +3 science, +2 culture: {player_board.resources}")

    # Test spending
    if player_board.spend_resources({'science': 2}):
        print(f"   After spending 2 science: {player_board.resources}")
    else:
        print("   Could not spend 2 science")

    print("\n4. Worker Management:")

    # Test population increase
    initial_workers = player_board.worker_manager.get_available_workers()
    print(f"   Initial workers: {initial_workers}")

    food_cost = player_board.get_population_cost()
    if player_board.resources['food'] >= food_cost:
        if player_board.increase_population(food_cost):
            player_board.spend_resources({'food': food_cost})
            new_workers = player_board.worker_manager.get_available_workers()
            print(f"   After population increase: {new_workers} workers (+{new_workers - initial_workers})")
        else:
            print("   Could not increase population")
    else:
        print(f"   Not enough food for population increase (need {food_cost}, have {player_board.resources['food']})")

    print("\n5. Action Management:")

    # Test action tracking
    actions_before = player_board.get_civil_actions_available()
    print(f"   Civil actions available: {actions_before}")

    # Use an action
    player_board.action_manager.use_civil_action()
    actions_after = player_board.get_civil_actions_available()
    print(f"   After using 1 action: {actions_after}")

    print("\n6. Production Calculation:")

    # Test production
    production = player_board.calculate_production()
    print(f"   Current production: {production}")

    print("\n7. Final Summary:")
    final_summary = player_board.get_full_summary()
    print(f"   Cards: {final_summary['cards']}")
    print(f"   Resources: {final_summary['resources']['current_resources']}")
    print(f"   Workers: {final_summary['workers']['available_workers']} available")
    print(f"   Actions: {final_summary['actions']['civil_actions']['available']}/{final_summary['actions']['civil_actions']['total']} civil")

    print(f"\n8. Card Collections:")
    print(f"   Production Buildings: {len(player_board.production_buildings)}")
    for building in player_board.production_buildings:
        workers = player_board.worker_manager.get_workers_in_technology(building.name)
        print(f"     - {building.name} ({workers} workers)")

    print(f"   Urban Buildings: {len(player_board.urban_buildings)}")
    for building in player_board.urban_buildings:
        workers = player_board.worker_manager.get_workers_in_technology(building.name)
        print(f"     - {building.name} ({workers} workers)")

    print(f"   Government: {player_board.government.name if player_board.government else 'None'}")
    print(f"   Leader: {player_board.leader.name if player_board.leader else 'None'}")

    print("\n✓ Modular PlayerBoard test completed successfully!")


if __name__ == "__main__":
    test_modular_player_board()
