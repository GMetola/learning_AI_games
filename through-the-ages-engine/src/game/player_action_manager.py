"""
Player Action Manager - Handles action tracking and availability for a player board.

This module manages:
- Civil and military action tracking
- Action bonuses and penalties
- Turn-based action reset
- Available action calculation
"""

from typing import Dict, List, Optional, Any
import logging


class PlayerActionManager:
    """Manages actions and action tracking for a player"""

    def __init__(self, player_id: int):
        """Initialize action manager for a player

        Args:
            player_id (int): ID of the player
        """
        self.player_id = player_id

        # Action tracking
        self.used_civil_actions = 0
        self.used_military_actions = 0

        # Action bonuses (from cards, events, etc.)
        self.civil_action_bonus = 0
        self.military_action_bonus = 0

        # Turn tracking for bonuses
        self.technologies_researched_this_turn = []

    def get_total_civil_actions(self, card_manager) -> int:
        """Get total civil actions available per turn

        Args:
            card_manager: PlayerCardManager instance

        Returns:
            int: Total civil actions per turn
        """
        base_actions = 4  # Default civil actions

        # Get government bonus
        government = card_manager.get_government()
        if government and hasattr(government, 'civil_actions'):
            base_actions = government.civil_actions

        # Add leader bonus
        leader = card_manager.get_leader()
        if leader and hasattr(leader, 'civil_action_bonus'):
            base_actions += leader.civil_action_bonus

        # Add temporary bonuses
        base_actions += self.civil_action_bonus

        return base_actions

    def get_total_military_actions(self, card_manager) -> int:
        """Get total military actions available per turn

        Args:
            card_manager: PlayerCardManager instance

        Returns:
            int: Total military actions per turn
        """
        base_actions = 2  # Default military actions

        # Get government bonus
        government = card_manager.get_government()
        if government and hasattr(government, 'military_actions'):
            base_actions = government.military_actions

        # Add leader bonus
        leader = card_manager.get_leader()
        if leader and hasattr(leader, 'military_action_bonus'):
            base_actions += leader.military_action_bonus

        # Add temporary bonuses
        base_actions += self.military_action_bonus

        return base_actions

    def get_civil_actions_available(self, card_manager) -> int:
        """Get remaining civil actions for this turn

        Args:
            card_manager: PlayerCardManager instance

        Returns:
            int: Remaining civil actions
        """
        total = self.get_total_civil_actions(card_manager)
        return max(0, total - self.used_civil_actions)

    def get_military_actions_available(self, card_manager) -> int:
        """Get remaining military actions for this turn

        Args:
            card_manager: PlayerCardManager instance

        Returns:
            int: Remaining military actions
        """
        total = self.get_total_military_actions(card_manager)
        return max(0, total - self.used_military_actions)

    def use_civil_action(self, count: int = 1) -> bool:
        """Use civil action(s)

        Args:
            count (int): Number of actions to use

        Returns:
            bool: True if actions were used successfully
        """
        if count <= 0:
            return False

        self.used_civil_actions += count
        logging.debug(f"Player {self.player_id}: Used {count} civil action(s)")
        return True

    def use_military_action(self, count: int = 1) -> bool:
        """Use military action(s)

        Args:
            count (int): Number of actions to use

        Returns:
            bool: True if actions were used successfully
        """
        if count <= 0:
            return False

        self.used_military_actions += count
        logging.debug(f"Player {self.player_id}: Used {count} military action(s)")
        return True

    def can_perform_civil_action(self, card_manager, count: int = 1) -> bool:
        """Check if player can perform civil action(s)

        Args:
            card_manager: PlayerCardManager instance
            count (int): Number of actions needed

        Returns:
            bool: True if actions are available
        """
        return self.get_civil_actions_available(card_manager) >= count

    def can_perform_military_action(self, card_manager, count: int = 1) -> bool:
        """Check if player can perform military action(s)

        Args:
            card_manager: PlayerCardManager instance
            count (int): Number of actions needed

        Returns:
            bool: True if actions are available
        """
        return self.get_military_actions_available(card_manager) >= count

    def add_civil_action_bonus(self, bonus: int):
        """Add temporary civil action bonus

        Args:
            bonus (int): Bonus actions to add
        """
        self.civil_action_bonus += bonus
        logging.info(f"Player {self.player_id}: +{bonus} civil action bonus")

    def add_military_action_bonus(self, bonus: int):
        """Add temporary military action bonus

        Args:
            bonus (int): Bonus actions to add
        """
        self.military_action_bonus += bonus
        logging.info(f"Player {self.player_id}: +{bonus} military action bonus")

    def add_technology_researched(self, tech_name: str):
        """Track technology researched this turn

        Args:
            tech_name (str): Name of technology researched
        """
        if tech_name not in self.technologies_researched_this_turn:
            self.technologies_researched_this_turn.append(tech_name)
            logging.debug(f"Player {self.player_id}: Researched {tech_name} this turn")

    def reset_turn(self):
        """Reset action counters for new turn"""
        self.used_civil_actions = 0
        self.used_military_actions = 0
        self.technologies_researched_this_turn = []

        # Reset temporary bonuses (they last only one turn)
        self.civil_action_bonus = 0
        self.military_action_bonus = 0

        logging.debug(f"Player {self.player_id}: Action counters reset for new turn")

    def get_action_summary(self, card_manager) -> Dict[str, Any]:
        """Get a summary of action state

        Args:
            card_manager: PlayerCardManager instance

        Returns:
            Dict[str, Any]: Action summary
        """
        return {
            'civil_actions': {
                'total': self.get_total_civil_actions(card_manager),
                'used': self.used_civil_actions,
                'available': self.get_civil_actions_available(card_manager),
                'bonus': self.civil_action_bonus
            },
            'military_actions': {
                'total': self.get_total_military_actions(card_manager),
                'used': self.used_military_actions,
                'available': self.get_military_actions_available(card_manager),
                'bonus': self.military_action_bonus
            },
            'technologies_researched_this_turn': self.technologies_researched_this_turn.copy()
        }

    def get_available_civil_actions(self, player_id: int, resource_manager, card_manager, worker_manager) -> List[Dict[str, Any]]:
        """Get list of available civil actions for this player

        Args:
            player_id (int): Player ID
            resource_manager: PlayerResourceManager instance
            card_manager: PlayerCardManager instance
            worker_manager: PlayerWorkerManager instance

        Returns:
            List[Dict[str, Any]]: Available actions
        """
        available_actions = []

        # Check if player has civil actions left
        if not self.can_perform_civil_action(card_manager):
            return available_actions

        resources = resource_manager.get_resources()

        # Action: Increase Population (if player has food)
        if resources['food'] >= worker_manager.get_population_cost() and worker_manager.has_available_yellow_tokens():
            available_actions.append({
                'type': 'aumentar_poblacion',
                'cost': {'civil_actions': 1, 'military_actions': 0},
                'resource_cost': {'food': worker_manager.get_population_cost()},
                'description': f'Aumentar población por {worker_manager.get_population_cost()} comida'
            })        # Action: Assign Worker (if player has workers and materials)
        if worker_manager.get_available_workers() > 0:
            # Check each building for worker assignment possibilities
            all_buildings = card_manager.get_all_buildings()
            for building in all_buildings:
                if worker_manager.can_assign_worker_to_building(building.name, card_manager):
                    material_cost = getattr(building, 'build_cost', 0)
                    if resources['material'] >= material_cost:
                        available_actions.append({
                            'type': 'asignar_trabajador',
                            'cost': {'civil_actions': 1, 'military_actions': 0},
                            'resource_cost': {'material': material_cost},
                            'description': f'Asignar trabajador a {building.name} por {material_cost} materiales',
                            'target': building.name
                        })        # Action: Build Building (for cards in hand that can be built)
        hand_cards = card_manager.get_hand_cards()
        for card in hand_cards:
            if hasattr(card, 'build_cost'):
                available_actions.append({
                    'type': 'construir_edificio',
                    'cost': {'civil_actions': 1, 'military_actions': 0},
                    'resource_cost': {},
                    'description': f'Construir edificio {card.name}',
                    'target': card.name
                })

        # Action: Research Technology (if player has science)
        if resources['science'] > 0:
            available_actions.append({
                'type': 'investigar_tecnologia',
                'cost': {'civil_actions': 1, 'military_actions': 0},
                'resource_cost': {'science': 1},  # Minimum cost
                'description': 'Investigar nueva tecnología'
            })

        return available_actions
