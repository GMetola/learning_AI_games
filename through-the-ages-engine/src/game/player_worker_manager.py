"""
Player Worker Manager - Handles population, workers, and worker assignments for a player board.

This module manages:
- Yellow token population groups
- Available workers
- Worker assignments to technologies/buildings
- Population increase mechanics
- Food consumption calculation
"""

from typing import Dict, List, Optional, Any
import logging


class PlayerWorkerManager:
    """Manages workers, population, and worker assignments for a player"""

    def __init__(self, player_id: int):
        """Initialize worker manager for a player

        Args:
            player_id (int): ID of the player
        """
        self.player_id = player_id

        # Yellow token reserves (population and workers)
        self.yellow_reserves = {
            'total_tokens': 24,
            'groups': [                    # Population groups
                {'tokens': 2, 'occupied': True, 'consumo': -1, 'coste_nuevo': 3},
                {'tokens': 4, 'occupied': True, 'consumo': -2, 'coste_nuevo': 4},
                {'tokens': 2, 'occupied': True, 'consumo': -2, 'coste_nuevo': 4},
                {'tokens': 2, 'occupied': True, 'consumo': -3, 'coste_nuevo': 5},
                {'tokens': 2, 'occupied': True, 'consumo': -3, 'coste_nuevo': 5},
                {'tokens': 2, 'occupied': True, 'consumo': -4, 'coste_nuevo': 7},
                {'tokens': 2, 'occupied': True, 'consumo': -4, 'coste_nuevo': 7},
                {'tokens': 2, 'occupied': True, 'consumo': -6, 'coste_nuevo': 7},
            ],
            'available_workers': 1,        # Workers available for assignment
            'technology_workers': {        # Workers assigned to technologies
                'Agriculture': 2,          # 2 workers in Agriculture (Age A)
                'Bronze': 2,              # 2 workers in Bronze
                'Philosophy': 1,           # 1 worker in Philosophy
                'Religion': 0             # 0 workers in Religion (available but not assigned)
            }
        }

    def get_available_workers(self) -> int:
        """Get number of available workers"""
        return self.yellow_reserves['available_workers']

    def get_technology_workers(self) -> Dict[str, int]:
        """Get workers assigned to technologies"""
        return self.yellow_reserves['technology_workers'].copy()

    def move_yellow_token_to_unemployment(self) -> bool:
        """Increase population by taking a worker from a yellow group

        Returns:
            bool: True if population was increased successfully
        """
        # Find the next available yellow token group
        if not self.has_available_yellow_tokens():
            logging.warning(f"Player {self.player_id}: No yellow tokens available for population increase")
            return False

        # Take token from group and add to available workers
        if self._take_yellow_token_from_group():
            self.yellow_reserves['available_workers'] += 1
            logging.info(f"Player {self.player_id}: Population increased, +1 worker available")
            return True

        return False

    def get_population_cost(self) -> int:
        """Get food cost for next population increase

        Returns:
            int: Food cost for next worker (currently fixed at 2)
        """
        # In the current implementation, population costs 2 food
        # In the full game, this would vary based on game state
        return 2

    def assign_worker_to_technology(self, tech_name: str, material_cost: int = 0) -> bool:
        """Assign a worker to a technology/building

        Args:
            tech_name (str): Name of technology to assign worker to
            material_cost (int): Material cost for assignment (default 0)

        Returns:
            bool: True if worker was assigned successfully
        """
        if self.yellow_reserves['available_workers'] <= 0:
            logging.warning(f"Player {self.player_id}: No available workers to assign")
            return False

        # Initialize technology if not tracked
        if tech_name not in self.yellow_reserves['technology_workers']:
            self.yellow_reserves['technology_workers'][tech_name] = 0

        # Assign worker
        self.yellow_reserves['available_workers'] -= 1
        self.yellow_reserves['technology_workers'][tech_name] += 1

        logging.info(f"Player {self.player_id}: Assigned worker to {tech_name} (cost: {material_cost} materials)")
        return True

    def remove_worker_from_technology(self, tech_name: str) -> bool:
        """Remove a worker from a technology

        Args:
            tech_name (str): Name of technology to remove worker from

        Returns:
            bool: True if worker was removed successfully
        """
        if (tech_name not in self.yellow_reserves['technology_workers'] or
            self.yellow_reserves['technology_workers'][tech_name] <= 0):
            logging.warning(f"Player {self.player_id}: No workers assigned to {tech_name}")
            return False

        # Remove worker and make available
        self.yellow_reserves['technology_workers'][tech_name] -= 1
        self.yellow_reserves['available_workers'] += 1

        logging.info(f"Player {self.player_id}: Removed worker from {tech_name}")
        return True

    def get_workers_in_technology(self, tech_name: str) -> int:
        """Get number of workers assigned to a specific technology

        Args:
            tech_name (str): Technology name

        Returns:
            int: Number of workers assigned
        """
        return self.yellow_reserves['technology_workers'].get(tech_name, 0)

    def get_food_consumption(self) -> int:
        """Calculate total food consumption from population

        Returns:
            int: Total food consumption
        """
        consumption = 0
        for group in self.yellow_reserves['groups']:
            if not group['occupied']:
                consumption += abs(group['consumo'])  # consumo values are negative
        return consumption

    def get_total_population(self) -> int:
        """Get total population (occupied tokens + available workers + assigned workers)

        Returns:
            int: Total population
        """
        occupied_tokens = sum(group['tokens'] for group in self.yellow_reserves['groups'] if group['occupied'])
        available_workers = self.yellow_reserves['available_workers']
        assigned_workers = sum(self.yellow_reserves['technology_workers'].values())

        return occupied_tokens + available_workers + assigned_workers

    def get_worker_summary(self) -> Dict[str, Any]:
        """Get a summary of worker state

        Returns:
            Dict[str, Any]: Worker summary
        """
        return {
            'available_workers': self.yellow_reserves['available_workers'],
            'technology_assignments': self.yellow_reserves['technology_workers'].copy(),
            'total_population': self.get_total_population(),
            'food_consumption': self.get_food_consumption(),
            'has_available_yellow_tokens': self.has_available_yellow_tokens(),
            'population_cost': self.get_population_cost()
        }

    def has_available_yellow_tokens(self) -> bool:
        """Check if there are yellow tokens available to take

        Returns:
            bool: True if tokens are available
        """
        for group in self.yellow_reserves['groups']:
            if group['occupied'] and group['tokens'] > 0:
                return True
        return False

    # === PRIVATE HELPER METHODS ===

    def _take_yellow_token_from_group(self) -> bool:
        """Take a yellow token from an unoccupied group

        Returns:
            bool: True if token was taken successfully
        """
        for group in self.yellow_reserves['groups']:
            if group['occupied'] and group['tokens'] > 0:
                group['tokens'] -= 1
                if group['tokens'] == 0:
                    group['occupied'] = True
                    logging.info(f"Player {self.player_id}: Yellow group emptied, marked as occupied")
                return True
        return False

    def get_building_limit(self, government_manager=None) -> int:
        """Get building limit based on government

        Args:
            government_manager: Reference to government/card manager (optional)

        Returns:
            int: Maximum number of buildings allowed
        """
        # Default building limit
        base_limit = 2

        # Get government bonus if available
        if government_manager and hasattr(government_manager, 'get_government'):
            government = government_manager.get_government()
            if government and hasattr(government, 'building_limit'):
                return government.building_limit

        return base_limit

    def can_assign_worker_to_building(self, tech_name: str, card_manager=None) -> bool:
        """Check if a worker can be assigned to a specific building

        Args:
            tech_name (str): Technology/building name
            card_manager: Reference to card manager (optional)

        Returns:
            bool: True if worker can be assigned
        """
        # Check if we have available workers
        if self.yellow_reserves['available_workers'] <= 0:
            return False

        # Check building limit if card manager is available
        if card_manager:
            building = card_manager.get_building_by_name(tech_name)
            if building:
                current_workers = self.get_workers_in_technology(tech_name)
                max_workers = getattr(building, 'max_workers', 2)
                if current_workers >= max_workers:
                    return False

        return True
