#!/usr/bin/env python3
"""
Test script to validate the enhanced Wonder and Government classes
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game.card_classes import Wonder, Government, create_card_from_csv_row

def test_wonder_parsing():
    """Test Wonder class with sample data"""
    print("=== Testing Wonder Class ===")

    # Test Hanging Gardens: "2 2 2"
    hanging_gardens = Wonder(
        name="Hanging Gardens",
        age="A",
        build_cost_steps="2 2 2",
        production={"culture": 1, "happy": 2}
    )

    print(f"Hanging Gardens: {hanging_gardens}")
    print(f"Build steps: {hanging_gardens.build_cost_steps}")
    print(f"Total cost: {hanging_gardens.total_cost}")
    print(f"Step info: {hanging_gardens.get_step_info()}")

    # Test building steps
    print(f"Next step cost: {hanging_gardens.get_next_step_cost()}")
    hanging_gardens.build_next_step()
    print(f"After building step 1: {hanging_gardens.get_step_info()}")
    hanging_gardens.build_next_step()
    print(f"After building step 2: {hanging_gardens.get_step_info()}")
    hanging_gardens.build_next_step()
    print(f"After building step 3 (completed): {hanging_gardens.get_step_info()}")

    # Test Great Wall: "2 2 3 2"
    great_wall = Wonder(
        name="Great Wall",
        age="I",
        build_cost_steps="2 2 3 2",
        production={"culture": 1, "strength": 1}
    )

    print(f"\nGreat Wall: {great_wall}")
    print(f"Build steps: {great_wall.build_cost_steps}")
    print(f"Total cost: {great_wall.total_cost}")
    print(f"Step info: {great_wall.get_step_info()}")

def test_government_parsing():
    """Test Government class with sample data"""
    print("\n=== Testing Government Class ===")

    # Test Monarchy: "3 (9)"
    monarchy = Government(
        name="Monarchy",
        age="I",
        tech_cost_str="3 (9)",
        civil_actions=5,
        military_actions=3,
        building_limit=3
    )

    print(f"Monarchy: {monarchy}")
    print(f"Normal cost: {monarchy.normal_cost}")
    print(f"Revolution cost: {monarchy.revolution_cost}")
    print(f"Cost info: {monarchy.get_cost_info()}")
    print(f"Research cost (normal): {monarchy.get_research_cost(False)}")
    print(f"Research cost (revolution): {monarchy.get_research_cost(True)}")

    # Test Democracy: "8 (21)"
    democracy = Government(
        name="Democracy",
        age="III",
        tech_cost_str="8 (21)",
        civil_actions=7,
        military_actions=3,
        building_limit=4,
        production={"culture": 2}
    )

    print(f"\nDemocracy: {democracy}")
    print(f"Normal cost: {democracy.normal_cost}")
    print(f"Revolution cost: {democracy.revolution_cost}")
    print(f"Cost info: {democracy.get_cost_info()}")

    # Test Despotism (no tech cost)
    despotism = Government(
        name="Despotism",
        age="A",
        tech_cost_str="",
        civil_actions=4,
        military_actions=2,
        building_limit=2
    )

    print(f"\nDespotism: {despotism}")
    print(f"Normal cost: {despotism.normal_cost}")
    print(f"Revolution cost: {despotism.revolution_cost}")
    print(f"Cost info: {despotism.get_cost_info()}")

def test_csv_factory():
    """Test creating cards from CSV-like data"""
    print("\n=== Testing CSV Factory ===")

    # Test Wonder from CSV
    wonder_row = {
        'Category': 'Wonder',
        'Type': 'Wonder',
        'Card Name': 'Hanging Gardens',
        'Age': 'A',
        'Tech cost': '',
        'Build cost': '2 2 2',
        'Production Food': '',
        'Production Material': '',
        'Production Culture': '1',
        'Production Strength': '',
        'Production Happy': '2',
        'Production Science': '',
        'Produce civil action': '',
        'Produce military action': '',
        'Gain Food': '',
        'Gain Material': '',
        'Gain Culture': '',
        'Gain Strength': '',
        'Gain Happy': '',
        'Gain Science': '',
        'Gain civil action': '',
        'Gain military action': '',
        'Blue token': '',
        'Yellow token': '',
        'Included v0.1': '1',
        'Card text and comments': ''
    }

    wonder_card = create_card_from_csv_row(wonder_row)
    print(f"Wonder from CSV: {wonder_card}")
    print(f"Type: {type(wonder_card)}")
    if hasattr(wonder_card, 'build_cost_steps'):
        print(f"Build steps: {wonder_card.build_cost_steps}")
        print(f"Total cost: {wonder_card.total_cost}")
        print(f"Step info: {wonder_card.get_step_info()}")

    # Test Government from CSV
    govt_row = {
        'Category': 'Govt',
        'Type': 'Govt',
        'Card Name': 'Monarchy',
        'Age': 'I',
        'Tech cost': '3 (9)',
        'Build cost': '',
        'Production Food': '',
        'Production Material': '',
        'Production Culture': '',
        'Production Strength': '',
        'Production Happy': '',
        'Production Science': '',
        'Produce civil action': '5',
        'Produce military action': '3',
        'Gain Food': '',
        'Gain Material': '',
        'Gain Culture': '',
        'Gain Strength': '',
        'Gain Happy': '',
        'Gain Science': '',
        'Gain civil action': '',
        'Gain military action': '',
        'Blue token': '',
        'Yellow token': '',
        'Included v0.1': '1',
        'Card text and comments': 'Building limit: 3'
    }

    govt_card = create_card_from_csv_row(govt_row)
    print(f"\nGovernment from CSV: {govt_card}")
    print(f"Type: {type(govt_card)}")
    if hasattr(govt_card, 'normal_cost'):
        print(f"Normal cost: {govt_card.normal_cost}")
        print(f"Revolution cost: {govt_card.revolution_cost}")
        print(f"Cost info: {govt_card.get_cost_info()}")

if __name__ == "__main__":
    test_wonder_parsing()
    test_government_parsing()
    test_csv_factory()
    print("\n=== All tests completed ===")
