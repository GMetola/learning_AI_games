#!/usr/bin/env python3
"""
Test script to verify initial technologies are loaded correctly
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game.card_loader import load_initial_technologies, get_initial_government
from game.board import PlayerBoard

def test_initial_technologies():
    """Test loading initial technologies from CSV"""
    print("=== Testing Initial Technologies Loading ===")

    # Load initial technologies
    initial_techs = load_initial_technologies()
    print(f"Loaded {len(initial_techs)} initial technologies:")

    for card in initial_techs:
        print(f"  - {card.name} (Age {card.age}, {card.__class__.__name__})")
        if hasattr(card, 'production'):
            print(f"    Production: {card.production}")
        if hasattr(card, 'civil_actions'):
            print(f"    Civil Actions: {card.civil_actions}, Military Actions: {card.military_actions}")

    # Test initial government
    initial_govt = get_initial_government()
    print(f"\nInitial Government: {initial_govt}")
    if initial_govt:
        print(f"  Civil Actions: {initial_govt.civil_actions}")
        print(f"  Military Actions: {initial_govt.military_actions}")
        print(f"  Building Limit: {initial_govt.building_limit}")

def test_player_board_initialization():
    """Test PlayerBoard initialization with initial technologies"""
    print("\n=== Testing PlayerBoard Initialization ===")

    # Create a player board
    player_board = PlayerBoard(player_id=1)

    # Check active government
    print(f"Active Government: {player_board.active_government}")
    if player_board.active_government:
        print(f"  Civil Actions: {player_board.get_civil_actions_per_turn()}")
        print(f"  Military Actions: {player_board.get_military_actions_per_turn()}")
        print(f"  Building Limit: {player_board.get_building_limit()}")

    # Check initial technologies
    print(f"\nInitial Technologies ({len(player_board.current_technologies)}):")
    for name, tech_info in player_board.current_technologies.items():
        card = tech_info['card_object']
        production = tech_info['production']
        print(f"  - {name}: {card.__class__.__name__}, Production: {production}")

    # Check worker assignments
    print(f"\nWorker Assignments:")
    for tech_name, workers in player_board.yellow_reserves['technology_workers'].items():
        print(f"  - {tech_name}: {workers} workers")

def test_action_system():
    """Test the new action system based on government"""
    print("\n=== Testing Action System ===")

    player_board = PlayerBoard(player_id=1)

    print(f"Civil actions available: {player_board.get_civil_actions_available()}")
    print(f"Military actions available: {player_board.get_military_actions_available()}")

    # Use some actions
    player_board.used_civil_actions = 2
    player_board.used_military_actions = 1

    print(f"After using 2 civil and 1 military action:")
    print(f"  Civil actions remaining: {player_board.get_civil_actions_available()}")
    print(f"  Military actions remaining: {player_board.get_military_actions_available()}")

if __name__ == "__main__":
    test_initial_technologies()
    test_player_board_initialization()
    test_action_system()
    print("\n=== All tests completed ===")
