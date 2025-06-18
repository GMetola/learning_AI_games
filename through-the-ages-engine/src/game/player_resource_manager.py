"""
Player Resource Manager - Handles resources, production, and corruption for a player board.

This module manages:
- Current resources (food, materials, science, culture, happy, strength)
- Resource production calculation
- Blue token management
- Corruption calculation and payment
- Production phase execution
"""

from typing import Dict, List, Optional, Any
import logging


class PlayerResourceManager:
    """Manages resources, production, and corruption for a player"""

    def __init__(self, player_id: int):
        """Initialize resource manager for a player

        Args:
            player_id (int): ID of the player
        """
        self.player_id = player_id

        # Current resources
        self.resources = {
            'food': 2,
            'material': 2,
            'science': 2,
            'culture': 0,
            'happy': 0,
            'strength': 1
        }

        # Blue token reserves for resource storage
        self.blue_reserves = {
            'total_blue_tokens': 16,        # Total blue tokens available
            'production_storage': {},      # Resources stored by technology
            'groups': [                    # Blue token groups with corruption
                {'tokens': 6, 'occupied': True, 'corruption': -2},
                {'tokens': 5, 'occupied': True, 'corruption': -4},
                {'tokens': 5, 'occupied': True, 'corruption': -6}
            ],
            'stored_blue_tokens': 11       # Currently stored blue tokens
        }

    def get_resources(self) -> Dict[str, int]:
        """Get current resources"""
        return self.resources.copy()

    def add_resources(self, resource_dict: Dict[str, int]):
        """Add resources to current reserves

        Args:
            resource_dict (Dict[str, int]): Resources to add
        """
        for resource, amount in resource_dict.items():
            if resource in self.resources:
                self.resources[resource] += amount
                if amount > 0:
                    logging.debug(f"Player {self.player_id}: +{amount} {resource}")

    def spend_resources(self, resource_dict: Dict[str, int]) -> bool:
        """Spend resources if available

        Args:
            resource_dict (Dict[str, int]): Resources to spend

        Returns:
            bool: True if resources were spent, False if insufficient
        """
        # Check if we have enough resources
        for resource, amount in resource_dict.items():
            if resource in self.resources:
                if self.resources[resource] < amount:
                    return False

        # Spend the resources
        for resource, amount in resource_dict.items():
            if resource in self.resources:
                self.resources[resource] -= amount
                if amount > 0:
                    logging.debug(f"Player {self.player_id}: -{amount} {resource}")

        return True

    def can_afford(self, resource_dict: Dict[str, int]) -> bool:
        """Check if player can afford a cost

        Args:
            resource_dict (Dict[str, int]): Resources required

        Returns:
            bool: True if player can afford the cost
        """
        for resource, amount in resource_dict.items():
            if resource in self.resources:
                if self.resources[resource] < amount:
                    return False
        return True

    def calculate_production(self, worker_manager, card_manager) -> Dict[str, int]:
        """Calculate total production from all sources

        Args:
            worker_manager: PlayerWorkerManager instance
            card_manager: PlayerCardManager instance

        Returns:
            Dict[str, int]: Production amounts by resource type
        """
        production = {'food': 0, 'material': 0, 'science': 0, 'culture': 0, 'happy': 0, 'strength': 0}

        # Production from buildings with workers
        technology_workers = worker_manager.get_technology_workers()

        for tech_name, workers in technology_workers.items():
            if workers > 0:
                building = card_manager.get_building_by_name(tech_name)
                if building and hasattr(building, 'production'):
                    for resource, amount_per_worker in building.production.items():
                        production[resource] += workers * amount_per_worker

        # Production from government
        government = card_manager.get_government()
        if government and hasattr(government, 'production'):
            for resource, amount in government.production.items():
                production[resource] += amount

        # Production from leader
        leader = card_manager.get_leader()
        if leader and hasattr(leader, 'production'):
            for resource, amount in leader.production.items():
                production[resource] += amount

        return production

    def execute_production_phase(self, worker_manager, card_manager) -> Dict[str, Any]:
        """Execute the production phase for this player

        Args:
            worker_manager: PlayerWorkerManager instance
            card_manager: PlayerCardManager instance

        Returns:
            Dict[str, Any]: Production phase results
        """
        # Calculate production
        production = self.calculate_production(worker_manager, card_manager)

        # Calculate consumption
        consumption = worker_manager.get_food_consumption()

        # Calculate corruption
        corruption = self.calculate_corruption_penalty()

        # Apply production
        self.add_resources(production)

        # Apply consumption (reduce food)
        if consumption > 0:
            food_consumed = min(self.resources['food'], consumption)
            self.resources['food'] -= food_consumed

        # Apply corruption
        resources_lost = self.pay_corruption(corruption)

        logging.info(f"Player {self.player_id} production: +{production}, consumption: -{consumption}, corruption: -{corruption}")

        return {
            'production': production,
            'consumption': consumption,
            'corruption': corruption,
            'resources_lost_to_corruption': resources_lost,
            'final_resources': self.resources.copy()
        }

    def get_corruption_penalty(self) -> int:
        """Get current corruption penalty based on blue tokens

        Returns:
            int: Corruption penalty amount
        """
        return self.calculate_corruption_penalty()

    def calculate_corruption_penalty(self) -> int:
        """Calculate corruption penalty based on occupied blue token groups

        Returns:
            int: Total corruption penalty
        """
        penalty = 0
        for group in self.blue_reserves['groups']:
            if not group['occupied']:
                penalty += abs(group['corruption'])  # corruption values are negative
        return penalty

    def pay_corruption(self, corruption_amount: int = None) -> Dict[str, int]:
        """Pay corruption by removing resources

        Args:
            corruption_amount (int, optional): Specific amount to pay

        Returns:
            Dict[str, int]: Resources lost to corruption
        """
        if corruption_amount is None:
            corruption_amount = self.calculate_corruption_penalty()

        if corruption_amount <= 0:
            return {}

        resources_lost = {}
        remaining_corruption = corruption_amount

        # Pay corruption with resources in priority order
        # Priority: food, materials, science, culture, happy (strength is not lost to corruption)
        resource_priority = ['material', 'food', 'science', 'culture', 'happy']

        for resource in resource_priority:
            if remaining_corruption <= 0:
                break

            available = self.resources[resource]
            if available > 0:
                lost = min(available, remaining_corruption)
                self.resources[resource] -= lost
                resources_lost[resource] = lost
                remaining_corruption -= lost

        if resources_lost:
            logging.info(f"Player {self.player_id}: Lost to corruption: {resources_lost}")

        return resources_lost

    def collect_production_resources(self, tech_name: str, amount: int):
        """Collect production resources and store them as blue tokens

        Args:
            tech_name (str): Technology producing the resources
            amount (int): Amount of resources to collect
        """
        if tech_name not in self.blue_reserves['production_storage']:
            self.blue_reserves['production_storage'][tech_name] = 0

        # Store resources if we have blue tokens available
        if self._take_blue_token_from_group():
            self.blue_reserves['production_storage'][tech_name] += amount
            logging.info(f"Player {self.player_id}: Stored {amount} resources from {tech_name}")
        else:
            logging.warning(f"Player {self.player_id}: No blue tokens available to store {tech_name} production")

    def _take_blue_token_from_group(self) -> bool:
        """Take a blue token from an unoccupied group

        Returns:
            bool: True if token was taken successfully
        """
        for group in self.blue_reserves['groups']:
            if not group['occupied'] and group['tokens'] > 0:
                group['tokens'] -= 1
                group['occupied'] = True
                self.blue_reserves['stored_blue_tokens'] += 1
                return True
        return False

    def _update_corruption_spaces(self):
        """Update corruption penalty based on current blue token usage"""
        # This method would update corruption based on game rules
        # For now, it's a placeholder for future implementation
        pass

    def check_revolt_condition(self) -> bool:
        """Check if player is in revolt condition (negative happiness)

        Returns:
            bool: True if in revolt
        """
        return self.resources['happy'] < 0

    def get_resource_summary(self) -> Dict[str, Any]:
        """Get a summary of resource state

        Returns:
            Dict[str, Any]: Resource summary
        """
        return {
            'current_resources': self.resources.copy(),
            'blue_tokens_used': self.blue_reserves['stored_blue_tokens'],
            'blue_tokens_available': self.blue_reserves['total_blue_tokens'] - self.blue_reserves['stored_blue_tokens'],
            'corruption_penalty': self.calculate_corruption_penalty(),
            'in_revolt': self.check_revolt_condition()
        }
