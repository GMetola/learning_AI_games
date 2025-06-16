"""
Test the card class hierarchy and CSV loading functionality.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game.card_classes import *
from game.card_loader import CardLoader, load_all_cards, get_card_by_name

def test_card_creation():
    """Test manual card creation"""
    print("=== Testing Manual Card Creation ===")

    # Test ProductionBuilding
    farm = ProductionBuilding(
        name="Test Farm",
        building_type="Farm",
        age="I",
        tech_cost=3,
        build_cost=4,
        production={'food': 2}
    )

    print(f"Created: {farm}")
    print(f"Can assign worker: {farm.can_assign_worker()}")

    # Test worker assignment
    farm.assign_worker("worker_1")
    farm.assign_worker("worker_2")
    print(f"Workers assigned: {farm.get_worker_count()}")
    print(f"Can assign more: {farm.can_assign_worker()}")

    # Test blue token storage
    farm.store_blue_token("token_1", "food", 3)
    farm.store_blue_token("token_2", "food", 2)
    print(f"Stored resources: {farm.get_stored_resources()}")
    print(f"Total production: {farm.get_total_production()}")

    print()

def test_csv_loading():
    """Test loading cards from CSV"""
    print("=== Testing CSV Card Loading ===")

    loader = CardLoader()

    # Print summary
    loader.print_card_summary()
    print()

    # Test specific cards
    print("Testing specific cards:")

    # Test a production building
    irrigation = get_card_by_name("Irrigation")
    if irrigation:
        print(f"Found: {irrigation}")
        print(f"Type: {type(irrigation).__name__}")
        if hasattr(irrigation, 'production'):
            print(f"Production: {irrigation.production}")
        if hasattr(irrigation, 'build_cost'):
            print(f"Build cost: {irrigation.build_cost}")

    # Test an urban building
    philosophy = get_card_by_name("Philosophy")
    if philosophy:
        print(f"Found: {philosophy}")
        print(f"Type: {type(philosophy).__name__}")
        if hasattr(philosophy, 'production'):
            print(f"Production: {philosophy.production}")

    # Test a government
    despotism = get_card_by_name("Despotism")
    if despotism:
        print(f"Found: {despotism}")
        print(f"Type: {type(despotism).__name__}")
        if hasattr(despotism, 'civil_actions'):
            print(f"Civil actions: {despotism.civil_actions}")
        if hasattr(despotism, 'military_actions'):
            print(f"Military actions: {despotism.military_actions}")

    print()

def test_card_categories():
    """Test filtering cards by category"""
    print("=== Testing Card Categories ===")

    loader = CardLoader()

    # Test production buildings
    production_cards = loader.get_cards_by_category('Production')
    print(f"Production buildings: {len(production_cards)}")
    for card in production_cards[:3]:  # Show first 3
        print(f"  - {card.name} ({card.building_type})")

    # Test urban buildings
    urban_cards = loader.get_cards_by_category('Urban')
    print(f"Urban buildings: {len(urban_cards)}")
    for card in urban_cards[:3]:  # Show first 3
        print(f"  - {card.name} ({card.building_type})")

    # Test by age
    age_a_cards = loader.get_cards_by_age('A')
    print(f"Age A cards: {len(age_a_cards)}")
    for card in age_a_cards:
        print(f"  - {card.name} ({type(card).__name__})")

    print()

def test_building_functionality():
    """Test building-specific functionality"""
    print("=== Testing Building Functionality ===")

    # Get a production building from CSV
    irrigation = get_card_by_name("Irrigation")
    if irrigation and isinstance(irrigation, ProductionBuilding):
        print(f"Testing {irrigation.name}:")

        # Test worker assignment
        print(f"Initial workers: {irrigation.get_worker_count()}")
        irrigation.assign_worker("farmer_1")
        irrigation.assign_worker("farmer_2")
        print(f"After assignment: {irrigation.get_worker_count()}")
        print(f"Production with workers: {irrigation.get_total_production()}")

        # Test blue token storage
        irrigation.store_blue_token("stored_1", "food", 4)
        print(f"Production with storage: {irrigation.get_total_production()}")

        # Test worker removal
        irrigation.remove_worker("farmer_1")
        print(f"After removing worker: {irrigation.get_worker_count()}")
        print(f"Final production: {irrigation.get_total_production()}")

    print()

if __name__ == "__main__":
    print("Testing Card Class Hierarchy\n")

    try:
        test_card_creation()
        test_csv_loading()
        test_card_categories()
        test_building_functionality()

        print("All tests completed successfully!")

    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
