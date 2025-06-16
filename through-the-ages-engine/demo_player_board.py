#!/usr/bin/env python3
"""
Demonstration of the updated PlayerBoard with card collections
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game.board import PlayerBoard
from game.card_loader import load_all_cards

def demonstrate_player_board():
    """Demonstrate the new PlayerBoard functionality"""
    print("=== Through the Ages: PlayerBoard Card Collections Demo ===\n")

    # Create a player board
    print("Creating new player...")
    player_board = PlayerBoard(player_id=1)

    # Show unique attributes
    print("UNIQUE ATTRIBUTES:")
    print(f"  Leader: {player_board.leader or 'None'}")
    print(f"  Government: {player_board.government.name} (Age {player_board.government.age})")
    print(f"    - Provides {player_board.get_civil_actions_per_turn()} civil actions per turn")
    print(f"    - Provides {player_board.get_military_actions_per_turn()} military actions per turn")
    print(f"    - Building limit: {player_board.get_building_limit()}")

    # Show multiple attributes
    print(f"\nMULTIPLE ATTRIBUTES:")
    print(f"  Wonders: {len(player_board.wonders)} cards")
    print(f"  Monuments: {len(player_board.monuments)} cards")
    print(f"  Hand Cards: {len(player_board.hand_cards)} cards")
    print(f"  Production Buildings: {len(player_board.production_buildings)} cards")
    print(f"  Urban Buildings: {len(player_board.urban_buildings)} cards")

    # Show initial buildings
    print(f"\nINITIAL BUILDINGS:")
    print("  Production Buildings:")
    for building in player_board.production_buildings:
        print(f"    - {building.name}: {building.production}")

    print("  Urban Buildings:")
    for building in player_board.urban_buildings:
        print(f"    - {building.name}: {building.production}")

    # Show total resources and workers
    print(f"\nRESOURCES:")
    for resource, amount in player_board.resources.items():
        print(f"  {resource}: {amount}")

    print(f"\nWORKER ASSIGNMENTS:")
    for tech, workers in player_board.yellow_reserves['technology_workers'].items():
        print(f"  {tech}: {workers} workers")
    print(f"  Available workers: {player_board.yellow_reserves['available_workers']}")

    # Demonstrate card management
    print(f"\nCARD MANAGEMENT DEMO:")

    # Load some cards to demonstrate with
    all_cards = load_all_cards()

    # Find some test cards
    irrigation = None
    hanging_gardens = None
    julius_caesar = None

    for card in all_cards:
        if card.name == 'Irrigation':
            irrigation = card
        elif card.name == 'Hanging Gardens':
            hanging_gardens = card
        elif card.name == 'Julius Caesar':
            julius_caesar = card

    # Demonstrate adding cards
    if irrigation:
        print(f"  Adding {irrigation.name} to hand...")
        player_board.add_card_to_hand(irrigation)
        print(f"  Hand cards: {len(player_board.hand_cards)}")

        print(f"  Building {irrigation.name}...")
        player_board.add_production_building(irrigation)
        print(f"  Production buildings: {len(player_board.production_buildings)}")
        print(f"  Has {irrigation.name}: {player_board.has_technology(irrigation.name)}")

    if hanging_gardens:
        print(f"  Building wonder: {hanging_gardens.name}...")
        player_board.add_wonder(hanging_gardens)
        print(f"  Wonders: {len(player_board.wonders)}")
        print(f"  Wonder steps: {hanging_gardens.get_step_info()}")

    if julius_caesar:
        print(f"  Setting leader: {julius_caesar.name}...")
        player_board.set_leader(julius_caesar)
        print(f"  Leader: {player_board.leader.name}")

    print(f"\nFINAL STATE:")
    print(f"  Total buildings: {len(player_board.get_all_buildings())}")
    print(f"  Hand cards: {len(player_board.hand_cards)}")
    print(f"  Wonders: {len(player_board.wonders)}")
    print(f"  Leader: {player_board.leader.name if player_board.leader else 'None'}")

    print(f"\n=== Demo completed ===")

if __name__ == "__main__":
    demonstrate_player_board()
