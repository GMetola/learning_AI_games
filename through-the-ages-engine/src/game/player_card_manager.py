"""
Player Card Manager - Handles all card collections for a player board.

This module manages:
- Production buildings
- Urban buildings
- Wonders
- Leaders
- Government
- Hand cards
- Monuments (future)
"""

from typing import Dict, List, Optional, Union
import logging
from game.card_loader import CardLoader, load_initial_technologies
from game.card_classes import (
    Card, ProductionBuilding, UrbanBuilding, Wonder,
    Leader, Government, Monument
)


class PlayerCardManager:
    """Manages all card collections for a player"""

    def __init__(self, player_id: int):
        """Initialize card manager for a player

        Args:
            player_id (int): ID of the player
        """
        self.player_id = player_id
        self._loader = CardLoader()

        # Card collections
        self.production_buildings: List[ProductionBuilding] = []
        self.urban_buildings: List[UrbanBuilding] = []
        self.wonders: List[Wonder] = []
        self.monuments: List[Monument] = []  # Future implementation
        self.hand_cards: List[Card] = []

        # Unique cards
        self.leader: Optional[Leader] = None
        self.government: Optional[Government] = None

        # Load initial setup
        self._load_initial_cards()

    def _load_initial_cards(self):
        """Load initial Age A technologies and setup"""
        initial_cards = load_initial_technologies()

        for card in initial_cards:
            if isinstance(card, ProductionBuilding):
                self.add_production_building(card)
            elif isinstance(card, UrbanBuilding):
                self.add_urban_building(card)
            elif isinstance(card, Government):
                self.set_government(card)
            else:
                # Handle other types in the future if needed
                logging.info(f"Player {self.player_id}: Skipping unknown card type '{type(card).__name__}' for '{card.name}'")


    # === PRODUCTION BUILDINGS ===

    def add_production_building(self, card_or_name: Union[ProductionBuilding, str], built: bool = True):
        """Add a production building to the player's board

        Args:
            card_or_name: ProductionBuilding card object or card name
            built: Whether the building is already built (default True for compatibility)

        Raises:
            ValueError: If card is invalid or already exists
        """
        card = self._resolve_card(card_or_name, ProductionBuilding, "ProductionBuilding")

        # Check for duplicates
        if any(building.name == card.name for building in self.production_buildings):
            raise ValueError(f"Production building '{card.name}' already exists on this board")

        self.production_buildings.append(card)

        logging.info(f"Player {self.player_id}: Added production building '{card.name}' (built: {built})")

    def remove_production_building(self, card_name: str) -> bool:
        """Remove a production building by name

        Args:
            card_name (str): Name of building to remove

        Returns:
            bool: True if removed, False if not found
        """
        for i, building in enumerate(self.production_buildings):
            if building.name == card_name:
                removed = self.production_buildings.pop(i)
                logging.info(f"Player {self.player_id}: Removed production building '{card_name}'")
                return True
        return False

    def get_production_buildings(self) -> List[ProductionBuilding]:
        """Get all production buildings"""
        return self.production_buildings.copy()

    # === URBAN BUILDINGS ===

    def add_urban_building(self, card_or_name: Union[UrbanBuilding, str], built: bool = True):
        """Add an urban building to the player's board

        Args:
            card_or_name: UrbanBuilding card object or card name
            built: Whether the building is already built (default True for compatibility)

        Raises:
            ValueError: If card is invalid or already exists
        """
        card = self._resolve_card(card_or_name, UrbanBuilding, "UrbanBuilding")

        # Check for duplicates
        if any(building.name == card.name for building in self.urban_buildings):
            raise ValueError(f"Urban building '{card.name}' already exists on this board")

        self.urban_buildings.append(card)

        logging.info(f"Player {self.player_id}: Added urban building '{card.name}' (built: {built})")

    def remove_urban_building(self, card_name: str) -> bool:
        """Remove an urban building by name

        Args:
            card_name (str): Name of building to remove

        Returns:
            bool: True if removed, False if not found
        """
        for i, building in enumerate(self.urban_buildings):
            if building.name == card_name:
                removed = self.urban_buildings.pop(i)
                logging.info(f"Player {self.player_id}: Removed urban building '{card_name}'")
                return True
        return False

    def get_urban_buildings(self) -> List[UrbanBuilding]:
        """Get all urban buildings"""
        return self.urban_buildings.copy()

    # === WONDERS ===

    def add_wonder(self, card_or_name: Union[Wonder, str]):
        """Add a wonder to the player's board

        Args:
            card_or_name: Wonder card object or card name

        Raises:
            ValueError: If card is invalid or already exists
        """
        card = self._resolve_card(card_or_name, Wonder, "Wonder")

        # Check for duplicates
        if any(wonder.name == card.name for wonder in self.wonders):
            raise ValueError(f"Wonder '{card.name}' already exists on this board")

        self.wonders.append(card)

        logging.info(f"Player {self.player_id}: Added wonder '{card.name}'")

    def remove_wonder(self, card_name: str) -> bool:
        """Remove a wonder by name

        Args:
            card_name (str): Name of wonder to remove

        Returns:
            bool: True if removed, False if not found
        """
        for i, wonder in enumerate(self.wonders):
            if wonder.name == card_name:
                removed = self.wonders.pop(i)
                logging.info(f"Player {self.player_id}: Removed wonder '{card_name}'")
                return True
        return False

    def get_wonders(self) -> List[Wonder]:
        """Get all wonders"""
        return self.wonders.copy()

    # === LEADERS ===

    def set_leader(self, card_or_name: Union[Leader, str, None]):
        """Set the player's leader

        Args:
            card_or_name: Leader card object, card name, or None to remove

        Raises:
            ValueError: If card is invalid
        """
        if card_or_name is None:
            if self.leader:
                old_name = self.leader.name
                self.leader = None
                logging.info(f"Player {self.player_id}: Removed leader '{old_name}'")
            return

        card = self._resolve_card(card_or_name, Leader, "Leader")        # Remove old leader if exists
        if self.leader:
            logging.info(f"Player {self.player_id}: Replacing leader '{self.leader.name}' with '{card.name}'")

        self.leader = card

        logging.info(f"Player {self.player_id}: Set leader to '{card.name}'")

    def get_leader(self) -> Optional[Leader]:
        """Get the current leader"""
        return self.leader

    # === GOVERNMENT ===

    def set_government(self, card_or_name: Union[Government, str]):
        """Set the player's government

        Args:
            card_or_name: Government card object or card name

        Raises:
            ValueError: If card is invalid
        """
        card = self._resolve_card(card_or_name, Government, "Government")        # Remove old government if exists
        if self.government:
            logging.info(f"Player {self.player_id}: Replacing government '{self.government.name}' with '{card.name}'")

        self.government = card

        logging.info(f"Player {self.player_id}: Set government to '{card.name}'")

    def get_government(self) -> Optional[Government]:
        """Get the current government"""
        return self.government

    # === HAND CARDS ===

    def add_card_to_hand(self, card_or_name: Union[Card, str]):
        """Add a card to the player's hand

        Args:
            card_or_name: Card object or card name

        Raises:
            ValueError: If card is invalid
        """
        if isinstance(card_or_name, str):
            card = self._loader.get_card_by_name(card_or_name)
            if not card:
                raise ValueError(f"Card '{card_or_name}' not found")
        else:
            card = card_or_name

        if not isinstance(card, Card):
            raise ValueError(f"Object {card} is not a Card instance")

        self.hand_cards.append(card)
        logging.info(f"Player {self.player_id}: Added '{card.name}' to hand")

    def remove_card_from_hand(self, card_or_name: Union[Card, str]) -> bool:
        """Remove a card from the player's hand

        Args:
            card_or_name: Card object or card name

        Returns:
            bool: True if removed, False if not found
        """
        if isinstance(card_or_name, str):
            card_name = card_or_name
        else:
            card_name = card_or_name.name

        for i, card in enumerate(self.hand_cards):
            if card.name == card_name:
                removed = self.hand_cards.pop(i)
                logging.info(f"Player {self.player_id}: Removed '{card_name}' from hand")
                return True
        return False

    def get_hand_cards(self) -> List[Card]:
        """Get all cards in hand"""
        return self.hand_cards.copy()

    # === UTILITY METHODS ===

    def get_all_buildings(self) -> List[Union[ProductionBuilding, UrbanBuilding]]:
        """Get all buildings (production + urban)"""
        return self.production_buildings + self.urban_buildings

    def get_building_by_name(self, name: str) -> Optional[Union[ProductionBuilding, UrbanBuilding]]:
        """Get a building by name

        Args:
            name (str): Building name

        Returns:
            Building object or None if not found
        """
        for building in self.get_all_buildings():
            if building.name == name:
                return building
        return None

    def has_technology(self, tech_name: str) -> bool:
        """Check if player has a developed technology (not in hand)

        This method only checks permanently developed technologies that provide benefits.
        Cards in hand are NOT considered "technologies" for game purposes.

        Args:
            tech_name (str): Name of the technology to check

        Returns:
            bool: True if technology is developed and active
        """
        # Check buildings (production + urban) - these are developed
        if self.get_building_by_name(tech_name):
            return True

        # Check wonders - these are developed
        if any(wonder.name == tech_name for wonder in self.wonders):
            return True

        # Check leader - this is active
        if self.leader and self.leader.name == tech_name:
            return True

        # Check government - this is active
        if self.government and self.government.name == tech_name:
            return True

        # Do NOT check hand cards - these are not active technologies
        return False

    def has_card_in_hand(self, card_name: str) -> bool:
        """Check if player has a specific card in hand (researched but not developed)

        Args:
            card_name (str): Name of the card to check

        Returns:
            bool: True if card is in hand
        """
        return any(card.name == card_name for card in self.hand_cards)

    def has_card_anywhere(self, card_name: str) -> bool:
        """Check if player has a card anywhere (developed OR in hand)

        This is useful for preventing duplicate research.

        Args:
            card_name (str): Name of the card to check

        Returns:
            bool: True if card exists anywhere for this player
        """
        return self.has_technology(card_name) or self.has_card_in_hand(card_name)

    def get_card_count_by_type(self) -> Dict[str, int]:
        """Get count of cards by type"""
        return {
            'production_buildings': len(self.production_buildings),
            'urban_buildings': len(self.urban_buildings),
            'wonders': len(self.wonders),
            'monuments': len(self.monuments),
            'hand_cards': len(self.hand_cards),
            'leader': 1 if self.leader else 0,
            'government': 1 if self.government else 0
        }

    # === PRIVATE HELPER METHODS ===

    def _resolve_card(self, card_or_name: Union[Card, str], expected_type: type, type_name: str) -> Card:
        """Resolve a card object from name or object, with type checking

        Args:
            card_or_name: Card object or name string
            expected_type: Expected card class type
            type_name: Human-readable type name for errors

        Returns:
            Card object

        Raises:
            ValueError: If card not found or wrong type
        """
        if isinstance(card_or_name, str):
            card = self._loader.get_card_by_name(card_or_name)
            if not card:
                raise ValueError(f"Card '{card_or_name}' not found")
        else:
            card = card_or_name

        if not isinstance(card, expected_type):
            raise ValueError(f"Card '{card.name}' is not a {type_name}")

        return card
