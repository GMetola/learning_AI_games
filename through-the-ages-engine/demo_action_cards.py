#!/usr/bin/env python3
"""
Demonstration of the improved card parsing for action cards
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game.card_loader import load_all_cards

def demonstrate_action_card_parsing():
    """Demonstrate the improved action card parsing"""
    print("=== Through the Ages: Action Card Parsing Demo ===\n")

    # Load all cards
    all_cards = load_all_cards()

    # Filter action cards
    action_cards = [card for card in all_cards if card.__class__.__name__ == 'ActionCard']

    print(f"Found {len(action_cards)} action cards")
    print("\nSample Action Cards with Cost Parsing:")
    print("=" * 60)

    # Show some examples of different cost notations
    examples = []
    cost_types = set()

    for card in action_cards:
        if hasattr(card, 'cost_notation') and card.cost_notation:
            examples.append(card)
            if hasattr(card, 'parsed_cost') and card.parsed_cost:
                cost_types.add(card.parsed_cost.get('target', 'unknown'))

    # Show examples by cost type
    shown_types = set()
    for card in examples[:15]:  # Show first 15 examples
        if hasattr(card, 'parsed_cost') and card.parsed_cost:
            target = card.parsed_cost.get('target', 'unknown')
            if target not in shown_types or len(shown_types) < 8:
                shown_types.add(target)
                print(f"Card: {card.name} (Age {card.age})")
                print(f"  Cost notation: '{card.cost_notation}'")
                print(f"  Parsed: {card.parsed_cost}")
                print(f"  Effect: {card.parsed_cost.get('description', 'Unknown effect')}")
                print()

    # Summary of cost types found
    print("Cost Target Types Found:")
    print("-" * 30)
    for cost_type in sorted(cost_types):
        count = sum(1 for card in examples
                   if hasattr(card, 'parsed_cost') and card.parsed_cost
                   and card.parsed_cost.get('target') == cost_type)

        type_description = {
            'W': 'Wonder construction',
            'U': 'Urban building construction',
            'P': 'Production building construction',
            'M': 'Military unit construction',
            'T': 'Technology research (science cost)',
            'PU': 'Any building construction'
        }.get(cost_type, 'Unknown')

        print(f"  {cost_type}: {count} cards - {type_description}")

    print(f"\nTotal parsed action cards: {len(examples)}")
    print("=== Demo completed ===")

if __name__ == "__main__":
    demonstrate_action_card_parsing()
