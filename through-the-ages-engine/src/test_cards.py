"""
Simple test to verify the card hierarchy works
"""

from game.card_classes import *
from game.card_loader import CardLoader, get_card_by_name

def test_basic_functionality():
    print("Testing Card Class Hierarchy")
    print("=" * 30)

    # Test creating a production building manually
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
    print(f"Workers: {farm.get_worker_count()}")

    # Test blue token storage
    farm.store_blue_token("token_1", "food", 3)
    print(f"Stored: {farm.get_stored_resources()}")
    print(f"Total production: {farm.get_total_production()}")

    print("\nTesting CSV Loading:")
    print("-" * 20)

    # Test loading from CSV
    loader = CardLoader()
    cards = loader.load_all_cards()
    print(f"Loaded {len(cards)} cards")

    # Test specific cards
    irrigation = get_card_by_name("Irrigation")
    if irrigation:
        print(f"Found Irrigation: {type(irrigation).__name__}")
        if hasattr(irrigation, 'production'):
            print(f"Production: {irrigation.production}")

    philosophy = get_card_by_name("Philosophy")
    if philosophy:
        print(f"Found Philosophy: {type(philosophy).__name__}")
        if hasattr(philosophy, 'production'):
            print(f"Production: {philosophy.production}")

    print("\nTest completed successfully!")

if __name__ == "__main__":
    test_basic_functionality()
