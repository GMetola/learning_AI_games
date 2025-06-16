#!/usr/bin/env python3
"""
Simple example showing how to create and add urban buildings
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game.card_loader import CardLoader
from game.card_classes import UrbanBuilding
from game.board import GameBoard
from game.player import Player


def simple_example():
    """Simple example of creating and adding urban buildings"""
    print("=== Simple Urban Building Example ===\n")

    # 1. Create a player board
    game_board = GameBoard(1)  # 1 player game
    player = Player("TestPlayer")
    player.player_id = 1
    player_board = game_board.player_boards[1]
    player.set_board(player_board)

    print(f"Initial urban buildings: {len(player_board.urban_buildings)}")

    # 2. Method 1: Create urban building manually
    custom_theater = UrbanBuilding(
        name="Custom Theater",
        building_type="Theater",
        age="I",
        tech_cost=4,
        build_cost=5,
        production={'culture': 2, 'happy': 1},
        gain={},  # No immediate gain
        card_text="A custom theater for entertainment"
    )

    # Add the building
    player_board.add_urban_building(custom_theater)
    print(f"Added custom theater successfully!")

    # 3. Method 2: Load existing building by name
    loader = CardLoader()
    drama_card = loader.get_card_by_name("Drama")
    if drama_card:
        try:
            player_board.add_urban_building(drama_card)
            print(f"Added Drama card successfully!")
        except ValueError as e:
            print(f"Could not add Drama: {e}")

    # 4. Method 3: Add by string name (uses the improved method)
    try:
        player_board.add_urban_building("Printing Press")
        print(f"Added Printing Press by name successfully!")
    except ValueError as e:
        print(f"Could not add Printing Press: {e}")

    # Show final results
    print(f"\nFinal urban buildings: {len(player_board.urban_buildings)}")
    print("\nBuildings on board:")
    for building in player_board.urban_buildings:
        workers = player_board.yellow_reserves['technology_workers'].get(building.name, 0)
        print(f"  • {building.name} ({building.building_type}) - {workers} workers")
        print(f"    Production: {building.production}")
        if building.gain:
            print(f"    Gain: {building.gain}")


if __name__ == "__main__":
    simple_example()
