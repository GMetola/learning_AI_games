#!/usr/bin/env python3
"""
Test script to verify action card parsing fixes
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game.card_loader import load_all_cards

def test_action_card_parsing():
    """Test that action cards parse without errors"""
    print("=== Testing Action Card Parsing ===")

    # Load all cards and count successes/errors
    cards = load_all_cards()

    # Count by category
    categories = {}
    action_cards = []

    for card in cards:
        class_name = card.__class__.__name__
        categories[class_name] = categories.get(class_name, 0) + 1

        if class_name == 'ActionCard':
            action_cards.append(card)

    print(f"Successfully loaded {len(cards)} cards:")
    for category, count in sorted(categories.items()):
        print(f"  {category}: {count}")

    print(f"\nAction Cards ({len(action_cards)}):")
    for card in action_cards[:10]:  # Show first 10
        print(f"  - {card.name} (Age {card.age})")
        if hasattr(card, 'cost_notation') and card.cost_notation:
            print(f"    Cost notation: '{card.cost_notation}'")
            print(f"    Parsed cost: {card.parsed_cost}")
            print(f"    Description: {card.get_cost_description()}")

    if len(action_cards) > 10:
        print(f"  ... and {len(action_cards) - 10} more")

if __name__ == "__main__":
    test_action_card_parsing()
    print("\n=== Test completed ===")
