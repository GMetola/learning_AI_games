#!/usr/bin/env python3
"""
Demo script showing how to create and add urban buildings to a player board
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game.card_loader import CardLoader
from game.card_classes import UrbanBuilding
from game.board import PlayerBoard
from game.game_state import GameState


def demo_urban_building_creation():
    """Demonstrate different ways to create and add urban buildings"""
    print("=== Urban Building Creation Demo ===\n")

    # Initialize card loader
    loader = CardLoader()

    # Method 1: Load urban building from CSV by name
    print("Method 1: Loading urban building from CSV by name")
    temple_card = loader.get_card_by_name("Temple")
    if temple_card:
        print(f"  Loaded: {temple_card}")
        print(f"  Type: {type(temple_card).__name__}")
        print(f"  Building type: {getattr(temple_card, 'building_type', 'N/A')}")
        print(f"  Production: {getattr(temple_card, 'production', {})}")
        print(f"  Gain: {getattr(temple_card, 'gain', {})}")
    else:
        print("  Temple card not found in CSV")
    print()

    # Method 2: Create urban building manually
    print("Method 2: Creating urban building manually")
    custom_library = UrbanBuilding(
        name="Custom Library",
        building_type="Library",
        age="I",
        tech_cost=3,
        build_cost=2,
        production={'science': 1, 'culture': 1},
        gain={'science': 2},
        card_text="A custom library building for demonstration"
    )
    print(f"  Created: {custom_library}")
    print(f"  Production: {custom_library.production}")
    print(f"  Gain: {custom_library.gain}")
    print()
      # Method 3: Adding to player board
    print("Method 3: Adding urban buildings to player board")

    # Create a simple player board
    from game.player import Player
    from game.board import GameBoard

    # Create a game board and player
    game_board = GameBoard(1)  # 1 player game
    player = Player("TestPlayer")
    player.player_id = 1
    player_board = game_board.player_boards[1]
    player.set_board(player_board)

    print(f"  Initial urban buildings: {len(player_board.urban_buildings)}")

    # Add using card object - Let's try with a different card
    library_card = loader.get_card_by_name("Library")
    if library_card:
        try:
            player_board.add_urban_building(library_card)
            print(f"  Added Library card: Success")
        except Exception as e:
            print(f"  Error adding Library: {e}")

    # Add using card name (string) - Try Theater
    try:
        player_board.add_urban_building("Theater")
        print(f"  Added Theater by name: Success")
    except Exception as e:
        print(f"  Error adding Theater: {e}")

    # Add custom building
    try:
        player_board.add_urban_building(custom_library)
        print(f"  Added custom library: Success")
    except Exception as e:
        print(f"  Error adding custom library: {e}")

    print(f"  Final urban buildings: {len(player_board.urban_buildings)}")

    # List all urban buildings
    print("\n  Urban buildings on board:")
    for i, building in enumerate(player_board.urban_buildings, 1):
        workers = player_board.yellow_reserves['technology_workers'].get(building.name, 0)
        print(f"    {i}. {building.name} ({building.building_type}) - {workers} workers")
        print(f"       Production: {building.production}")
        if building.gain:
            print(f"       Gain: {building.gain}")
    print()


def demo_all_urban_buildings():
    """Show all available urban buildings from CSV"""
    print("=== All Available Urban Buildings ===\n")

    loader = CardLoader()
    urban_buildings = loader.get_urban_buildings()

    print(f"Found {len(urban_buildings)} urban buildings:\n")

    for building in urban_buildings:
        print(f"  {building.name} ({building.age}) - {building.building_type}")
        print(f"    Tech Cost: {building.tech_cost}, Build Cost: {building.build_cost}")
        if building.production:
            print(f"    Production: {building.production}")
        if building.gain:
            print(f"    Gain: {building.gain}")
        print(f"    Text: {building.card_text[:60]}...")
        print()


if __name__ == "__main__":
    demo_urban_building_creation()
    demo_all_urban_buildings()
