"""
Refactored Player Board - Coordinates all player management modules.

This is the main PlayerBoard class that delegates responsibilities to specialized managers:
- PlayerCardManager: Card collections (buildings, wonders, leaders, etc.)
- PlayerResourceManager: Resources, production, corruption
- PlayerWorkerManager: Population, workers, assignments
- PlayerActionManager: Action tracking and availability
"""

from typing import Dict, List, Optional, Any
import logging
from .player_card_manager import PlayerCardManager
from .player_resource_manager import PlayerResourceManager
from .player_worker_manager import PlayerWorkerManager
from .player_action_manager import PlayerActionManager


class PlayerBoard:
    """Refactored player board that coordinates specialized managers"""

    def __init__(self, player_id: int):
        """Initialize player board with all managers

        Args:
            player_id (int): ID of the player
        """
        self.player_id = player_id

        # Initialize specialized managers
        self.card_manager = PlayerCardManager(player_id)
        self.resource_manager = PlayerResourceManager(player_id)
        self.worker_manager = PlayerWorkerManager(player_id)
        self.action_manager = PlayerActionManager(player_id)

        logging.info(f"Player {player_id}: Board initialized with modular managers")

    # === DELEGATION METHODS FOR CARDS ===

    @property
    def production_buildings(self):
        """Access to production buildings"""
        return self.card_manager.production_buildings

    @property
    def urban_buildings(self):
        """Access to urban buildings"""
        return self.card_manager.urban_buildings

    @property
    def wonders(self):
        """Access to wonders"""
        return self.card_manager.wonders

    @property
    def hand_cards(self):
        """Access to hand cards"""
        return self.card_manager.hand_cards

    @property
    def leader(self):
        """Access to leader"""
        return self.card_manager.leader

    @property
    def government(self):
        """Access to government"""
        return self.card_manager.government

    @property
    def current_technologies(self):
        """Access to legacy technology tracking"""
        return self.card_manager.current_technologies

    def add_production_building(self, card_or_name):
        """Add production building"""
        return self.card_manager.add_production_building(card_or_name)

    def add_urban_building(self, card_or_name):
        """Add urban building"""
        return self.card_manager.add_urban_building(card_or_name)

    def add_wonder(self, card_or_name):
        """Add wonder"""
        return self.card_manager.add_wonder(card_or_name)

    def set_leader(self, card_or_name):
        """Set leader"""
        return self.card_manager.set_leader(card_or_name)

    def set_government(self, card_or_name):
        """Set government"""
        return self.card_manager.set_government(card_or_name)

    def add_card_to_hand(self, card_or_name):
        """Add card to hand"""
        return self.card_manager.add_card_to_hand(card_or_name)

    def remove_card_from_hand(self, card_or_name):
        """Remove card from hand"""
        return self.card_manager.remove_card_from_hand(card_or_name)

    def get_all_buildings(self):
        """Get all buildings"""
        return self.card_manager.get_all_buildings()

    def get_building_by_name(self, name):
        """Get building by name"""
        return self.card_manager.get_building_by_name(name)

    def has_technology(self, tech_name):
        """Check if has technology"""
        return self.card_manager.has_technology(tech_name)

    # === DELEGATION METHODS FOR RESOURCES ===

    @property
    def resources(self):
        """Access to resources"""
        return self.resource_manager.resources

    def add_resources(self, resource_dict):
        """Add resources"""
        return self.resource_manager.add_resources(resource_dict)

    def spend_resources(self, resource_dict):
        """Spend resources"""
        return self.resource_manager.spend_resources(resource_dict)

    def can_afford(self, resource_dict):
        """Check if can afford cost"""
        return self.resource_manager.can_afford(resource_dict)

    def calculate_production(self):
        """Calculate production"""
        return self.resource_manager.calculate_production(self.worker_manager, self.card_manager)

    def execute_production_phase(self):
        """Execute production phase"""
        return self.resource_manager.execute_production_phase(self.worker_manager, self.card_manager)

    def get_corruption_penalty(self):
        """Get corruption penalty"""
        return self.resource_manager.get_corruption_penalty()

    def pay_corruption(self, amount=None):
        """Pay corruption"""
        return self.resource_manager.pay_corruption(amount)

    # === DELEGATION METHODS FOR WORKERS ===

    @property
    def yellow_reserves(self):
        """Access to yellow reserves (for backward compatibility)"""
        return self.worker_manager.yellow_reserves

    def increase_population(self, food_cost):
        """Increase population"""
        return self.worker_manager.increase_population(food_cost)

    def get_population_cost(self):
        """Get population cost"""
        return self.worker_manager.get_population_cost()

    def can_increase_population(self):
        """Check if can increase population"""
        return self.worker_manager.can_increase_population()

    def assign_worker_to_building(self, tech_card):
        """Assign worker to building (legacy method name)"""
        if hasattr(tech_card, 'name'):
            tech_name = tech_card.name
            material_cost = getattr(tech_card, 'build_cost', 0)
        else:
            tech_name = str(tech_card)
            material_cost = 0

        return self.worker_manager.assign_worker_to_technology(tech_name, material_cost)

    def get_food_consumption(self):
        """Get food consumption"""
        return self.worker_manager.get_food_consumption()

    def get_building_limit(self):
        """Get building limit"""
        return self.worker_manager.get_building_limit(self.card_manager)

    # === DELEGATION METHODS FOR ACTIONS ===

    @property
    def used_civil_actions(self):
        """Access to used civil actions"""
        return self.action_manager.used_civil_actions

    @used_civil_actions.setter
    def used_civil_actions(self, value):
        """Set used civil actions"""
        self.action_manager.used_civil_actions = value

    @property
    def used_military_actions(self):
        """Access to used military actions"""
        return self.action_manager.used_military_actions

    @used_military_actions.setter
    def used_military_actions(self, value):
        """Set used military actions"""
        self.action_manager.used_military_actions = value

    def get_total_civil_actions(self):
        """Get total civil actions"""
        return self.action_manager.get_total_civil_actions(self.card_manager)

    def get_total_military_actions(self):
        """Get total military actions"""
        return self.action_manager.get_total_military_actions(self.card_manager)

    def get_civil_actions_available(self):
        """Get available civil actions"""
        return self.action_manager.get_civil_actions_available(self.card_manager)

    def get_military_actions_available(self):
        """Get available military actions"""
        return self.action_manager.get_military_actions_available(self.card_manager)

    def add_technology_researched(self, tech_name):
        """Add technology researched"""
        return self.action_manager.add_technology_researched(tech_name)

    def add_civil_action_bonus(self, bonus):
        """Add civil action bonus"""
        return self.action_manager.add_civil_action_bonus(bonus)

    def add_military_action_bonus(self, bonus):
        """Add military action bonus"""
        return self.action_manager.add_military_action_bonus(bonus)

    # === ADDITIONAL METHODS (delegated to appropriate managers) ===

    def update_cards_in_hand(self, count):
        """Update cards in hand count (legacy method)"""
        # This is handled automatically by the card manager
        pass

    def get_civil_actions_per_turn(self):
        """Get civil actions per turn"""
        return self.action_manager.get_total_civil_actions(self.card_manager)

    def get_military_actions_per_turn(self):
        """Get military actions per turn"""
        return self.action_manager.get_total_military_actions(self.card_manager)

    def check_revolt_condition(self):
        """Check revolt condition"""
        return self.resource_manager.check_revolt_condition()

    def calculate_corruption_penalty(self):
        """Calculate corruption penalty"""
        return self.resource_manager.calculate_corruption_penalty()

    def collect_production_resources(self, tech_name, amount):
        """Collect production resources"""
        return self.resource_manager.collect_production_resources(tech_name, amount)

    # === TURN MANAGEMENT ===

    def complete_turn(self):
        """Complete turn and reset action counters"""
        self.action_manager.reset_turn()

        # Execute production phase
        production_results = self.execute_production_phase()

        logging.info(f"Player {self.player_id}: Turn completed")

        return {
            'success': True,
            'production_results': production_results,
            'final_resources': self.resources.copy()
        }

    # === SUMMARY AND DEBUG METHODS ===

    def get_full_summary(self) -> Dict[str, Any]:
        """Get complete summary of player state

        Returns:
            Dict[str, Any]: Complete player summary
        """
        return {
            'player_id': self.player_id,
            'cards': self.card_manager.get_card_count_by_type(),
            'resources': self.resource_manager.get_resource_summary(),
            'workers': self.worker_manager.get_worker_summary(),
            'actions': self.action_manager.get_action_summary(self.card_manager)
        }

    def get_available_civil_actions(self, player_id):
        """Get available civil actions (for compatibility with game logic)"""
        return self.action_manager.get_available_civil_actions(
            player_id, self.resource_manager, self.card_manager, self.worker_manager
        )
