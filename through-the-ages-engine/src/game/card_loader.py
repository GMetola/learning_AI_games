"""
Card loader utility to read cards from CSV and create card objects.
"""

import csv
import os
from typing import List, Dict
from .card_classes import Card, create_card_from_csv_row

class CardLoader:
    """Utility class to load cards from CSV data"""

    def __init__(self, csv_path: str = None):
        """Initialize card loader

        Args:
            csv_path (str): Path to cards CSV file
        """
        if csv_path is None:
            # Default path relative to project root
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            csv_path = os.path.join(project_root, 'data', 'cards.csv')

        self.csv_path = csv_path
        self._cards_cache = None

    def load_all_cards(self) -> List[Card]:
        """Load all cards from CSV

        Returns:
            List[Card]: List of all card objects
        """
        if self._cards_cache is not None:
            return self._cards_cache

        cards = []

        try:
            with open(self.csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    # Skip rows that are not included in v0.1
                    if row.get('Included v0.1') != '1':
                        continue

                    try:
                        card = create_card_from_csv_row(row)
                        cards.append(card)
                    except Exception as e:
                        print(f"Error creating card from row {row.get('Card Name', 'Unknown')}: {e}")
                        continue

        except FileNotFoundError:
            print(f"Cards CSV file not found at: {self.csv_path}")
            return []
        except Exception as e:
            print(f"Error reading cards CSV: {e}")
            return []

        self._cards_cache = cards
        return cards

    def get_cards_by_category(self, category: str) -> List[Card]:
        """Get all cards of a specific category

        Args:
            category (str): Category name (Production, Urban, Military, etc.)

        Returns:
            List[Card]: Cards matching the category
        """
        all_cards = self.load_all_cards()

        # Map category names to class types
        category_mapping = {
            'Production': 'ProductionBuilding',
            'Urban': 'UrbanBuilding',
            'Military': 'MilitaryTechnology',
            'Wonder': 'Wonder',
            'Govt': 'Government',
            'Special': 'Special',
            'Action': 'ActionCard',
            'Leader': 'Leader'
        }

        target_class = category_mapping.get(category)
        if not target_class:
            return []

        return [card for card in all_cards if card.__class__.__name__ == target_class]

    def get_cards_by_age(self, age: str) -> List[Card]:
        """Get all cards of a specific age

        Args:
            age (str): Age identifier (A, I, II, III)

        Returns:
            List[Card]: Cards matching the age
        """
        all_cards = self.load_all_cards()
        return [card for card in all_cards if card.age == age]

    def get_card_by_name(self, name: str) -> Card:
        """Get a specific card by name

        Args:
            name (str): Card name

        Returns:
            Card: Card object or None if not found
        """
        all_cards = self.load_all_cards()
        for card in all_cards:
            if card.name == name:
                return card
        return None

    def get_initial_technologies(self) -> List[Card]:
        """Get the initial Age A technologies

        Returns:
            List[Card]: Initial technology cards
        """
        initial_names = ['Philosophy', 'Warriors', 'Despotism']
        return [self.get_card_by_name(name) for name in initial_names if self.get_card_by_name(name)]

    def get_production_buildings(self) -> List[Card]:
        """Get all production buildings (farms, mines, labs)

        Returns:
            List[Card]: Production building cards
        """
        return self.get_cards_by_category('Production')

    def get_urban_buildings(self) -> List[Card]:
        """Get all urban buildings (temples, arenas, libraries, theaters)

        Returns:
            List[Card]: Urban building cards
        """
        return self.get_cards_by_category('Urban')

    def print_card_summary(self):
        """Print a summary of all loaded cards"""
        cards = self.load_all_cards()

        print(f"Loaded {len(cards)} cards from {self.csv_path}")
        print("\nCard breakdown by category:")

        categories = {}
        for card in cards:
            class_name = card.__class__.__name__
            categories[class_name] = categories.get(class_name, 0) + 1

        for category, count in sorted(categories.items()):
            print(f"  {category}: {count}")

        print("\nCard breakdown by age:")
        ages = {}
        for card in cards:
            ages[card.age] = ages.get(card.age, 0) + 1

        for age, count in sorted(ages.items()):
            print(f"  Age {age}: {count}")

# Global card loader instance
_card_loader = None

def get_card_loader() -> CardLoader:
    """Get global card loader instance

    Returns:
        CardLoader: Singleton card loader
    """
    global _card_loader
    if _card_loader is None:
        _card_loader = CardLoader()
    return _card_loader

def load_all_cards() -> List[Card]:
    """Convenience function to load all cards

    Returns:
        List[Card]: All card objects
    """
    return get_card_loader().load_all_cards()

def get_card_by_name(name: str) -> Card:
    """Convenience function to get card by name

    Args:
        name (str): Card name

    Returns:
        Card: Card object or None
    """
    return get_card_loader().get_card_by_name(name)
