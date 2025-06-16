"""
Card class hierarchy for Through the Ages game.
Based on the cards.csv structure and game requirements.
"""

from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
import logging

class Card(ABC):
    """Base card class for all cards in the game"""

    def __init__(self, name: str, age: str, card_text: str = ""):
        """Initialize base card

        Args:
            name (str): Card name
            age (str): Card age (A, I, II, III)
            card_text (str): Card description/rules text
        """
        self.name = name
        self.age = age
        self.card_text = card_text

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', age='{self.age}')"

class CivilCard(Card):
    """Base class for all civil cards"""

    def __init__(self, name: str, age: str, tech_cost: int = 0, card_text: str = ""):
        """Initialize civil card

        Args:
            name (str): Card name
            age (str): Card age
            tech_cost (int): Science cost to research this technology
            card_text (str): Card description
        """
        super().__init__(name, age, card_text)
        self.tech_cost = tech_cost

class WarCard(Card):
    """Base class for all war/military cards (not implemented in v0.1)"""
    pass

class Technology(CivilCard):
    """Base class for technology cards"""

    def __init__(self, name: str, age: str, tech_cost: int = 0, card_text: str = ""):
        super().__init__(name, age, tech_cost, card_text)

class WorkBuilding(Technology):
    """Base class for buildings that can have workers"""

    def __init__(self, name: str, age: str, tech_cost: int = 0, build_cost: int = 0,
                 card_text: str = ""):
        """Initialize work building

        Args:
            name (str): Building name
            age (str): Card age
            tech_cost (int): Science cost to research
            build_cost (int): Material cost to build/assign worker
            card_text (str): Card description
        """
        super().__init__(name, age, tech_cost, card_text)
        self.build_cost = build_cost
        self.workers = []  # List of worker tokens assigned
        self.max_workers = 2  # Default max workers (should be from government)

    def can_assign_worker(self) -> bool:
        """Check if a worker can be assigned to this building"""
        return len(self.workers) < self.max_workers

    def assign_worker(self, worker_id: str) -> bool:
        """Assign a worker to this building

        Args:
            worker_id (str): Identifier for the worker

        Returns:
            bool: True if worker was assigned successfully
        """
        if self.can_assign_worker():
            self.workers.append(worker_id)
            logging.info(f"Worker {worker_id} assigned to {self.name}")
            return True
        logging.warning(f"Cannot assign worker to {self.name}: maximum workers reached")
        return False

    def remove_worker(self, worker_id: str) -> bool:
        """Remove a worker from this building

        Args:
            worker_id (str): Identifier for the worker

        Returns:
            bool: True if worker was removed successfully
        """
        if worker_id in self.workers:
            self.workers.remove(worker_id)
            logging.info(f"Worker {worker_id} removed from {self.name}")
            return True
        logging.warning(f"Worker {worker_id} not found in {self.name}")
        return False

    def get_worker_count(self) -> int:
        """Get the number of workers assigned to this building"""
        return len(self.workers)

class ProductionBuilding(WorkBuilding):
    """Production buildings (farms, mines, labs) that can store blue tokens"""

    def __init__(self, name: str, building_type: str, age: str, tech_cost: int = 0,
                 build_cost: int = 0, production: Dict[str, int] = None,
                 card_text: str = ""):
        """Initialize production building

        Args:
            name (str): Building name
            building_type (str): Type (Farm, Mine, Lab, etc.)
            age (str): Card age
            tech_cost (int): Science cost to research
            build_cost (int): Material cost to build
            production (Dict[str, int]): Resources produced per worker
            card_text (str): Card description
        """
        super().__init__(name, age, tech_cost, build_cost, card_text)
        self.building_type = building_type
        self.production = production or {}
        self.blue_tokens = []  # List of blue tokens stored

    def store_blue_token(self, token_id: str, resource_type: str, amount: int):
        """Store a blue token in this building

        Args:
            token_id (str): Unique identifier for the token
            resource_type (str): Type of resource stored
            amount (int): Amount of resource
        """
        token = {
            'id': token_id,
            'resource_type': resource_type,
            'amount': amount
        }
        self.blue_tokens.append(token)
        logging.info(f"Blue token stored in {self.name}: {amount} {resource_type}")

    def get_stored_resources(self) -> Dict[str, int]:
        """Get total resources stored in blue tokens

        Returns:
            Dict[str, int]: Resource type -> total amount
        """
        stored = {}
        for token in self.blue_tokens:
            resource_type = token['resource_type']
            amount = token['amount']
            stored[resource_type] = stored.get(resource_type, 0) + amount
        return stored

    def get_total_production(self) -> Dict[str, int]:
        """Get total production including workers and stored resources

        Returns:
            Dict[str, int]: Resource type -> total production
        """
        total = {}

        # Production from workers
        worker_count = self.get_worker_count()
        for resource, amount_per_worker in self.production.items():
            total[resource] = worker_count * amount_per_worker

        # Add stored resources from blue tokens
        stored = self.get_stored_resources()
        for resource, amount in stored.items():
            total[resource] = total.get(resource, 0) + amount

        return total

class UrbanBuilding(WorkBuilding):
    """Urban buildings (temples, arenas, libraries, theaters)"""

    def __init__(self, name: str, building_type: str, age: str, tech_cost: int = 0,
                 build_cost: int = 0, production: Dict[str, int] = None,
                 gain: Dict[str, int] = None, card_text: str = ""):
        """Initialize urban building

        Args:
            name (str): Building name
            building_type (str): Type (Temple, Arena, Library, Theater)
            age (str): Card age
            tech_cost (int): Science cost to research
            build_cost (int): Material cost to build
            production (Dict[str, int]): Resources produced per turn
            gain (Dict[str, int]): One-time resources gained when built
            card_text (str): Card description
        """
        super().__init__(name, age, tech_cost, build_cost, card_text)
        self.building_type = building_type
        self.production = production or {}
        self.gain = gain or {}

# Classes for other card types (not fully implemented in v0.1)

class MilitaryTechnology(Technology):
    """Military technology cards (Warriors, Knights, etc.)"""

    def __init__(self, name: str, unit_type: str, age: str, tech_cost: int = 0,
                 build_cost: int = 0, strength: int = 0, card_text: str = ""):
        super().__init__(name, age, tech_cost, card_text)
        self.unit_type = unit_type  # Infantry, Cavalry, Artillery
        self.build_cost = build_cost
        self.strength = strength

class Wonder(Technology):
    """Wonder cards with multiple building steps"""

    def __init__(self, name: str, age: str, build_cost_steps: str = "",
                 production: Dict[str, int] = None, gain: Dict[str, int] = None,
                 effects: Dict[str, Any] = None, card_text: str = ""):
        super().__init__(name, age, 0, card_text)  # Wonders don't have tech cost
        self.build_cost_steps = self._parse_build_steps(build_cost_steps)
        self.num_steps = len(self.build_cost_steps)
        self.total_cost = sum(self.build_cost_steps) if self.build_cost_steps else 0
        self.current_step = 0
        self.completed = False
        self.production = production or {}
        self.gain = gain or {}
        self.effects = effects or {}

    def _parse_build_steps(self, build_cost_str: str) -> List[int]:
        """Parse build cost steps from string like '2 2 2' or '3 4 5'"""
        if not build_cost_str or build_cost_str.strip() == "":
            return []
        try:
            return [int(x.strip()) for x in build_cost_str.split() if x.strip().isdigit()]
        except ValueError:
            return []

    def get_next_step_cost(self) -> Optional[int]:
        """Get the cost of the next step to build"""
        if self.current_step < len(self.build_cost_steps):
            return self.build_cost_steps[self.current_step]
        return None

    def build_next_step(self) -> bool:
        """Build the next step of the wonder"""
        if self.current_step < len(self.build_cost_steps):
            self.current_step += 1
            if self.current_step >= len(self.build_cost_steps):
                self.completed = True
            return True
        return False

    def get_completion_percentage(self) -> float:
        """Get completion percentage (0.0 to 1.0)"""
        if not self.build_cost_steps:
            return 0.0
        return self.current_step / len(self.build_cost_steps)

    def get_step_info(self) -> Dict[str, Any]:
        """Get detailed information about wonder steps"""
        return {
            'num_steps': self.num_steps,
            'current_step': self.current_step,
            'completed_steps': self.current_step,
            'remaining_steps': self.num_steps - self.current_step,
            'total_cost': self.total_cost,
            'next_step_cost': self.get_next_step_cost(),
            'completed': self.completed,
            'completion_percentage': self.get_completion_percentage()
        }

class Government(Technology):
    """Government cards with normal and revolution costs"""

    def __init__(self, name: str, age: str, tech_cost_str: str = "",
                 civil_actions: int = 4, military_actions: int = 2,
                 building_limit: int = 2, production: Dict[str, int] = None,
                 gain: Dict[str, int] = None, effects: Dict[str, Any] = None,
                 card_text: str = ""):
        # Parse tech cost string like "3 (9)" or "8 (21)"
        normal_cost, revolution_cost = self._parse_government_costs(tech_cost_str)
        super().__init__(name, age, normal_cost, card_text)

        self.normal_cost = normal_cost
        self.revolution_cost = revolution_cost
        self.civil_actions = civil_actions
        self.military_actions = military_actions
        self.building_limit = building_limit
        self.production = production or {}
        self.gain = gain or {}
        self.effects = effects or {}

    def _parse_government_costs(self, cost_str: str) -> tuple:
        """Parse government costs from string like '3 (9)' where 3 is revolution cost and 9 is normal cost"""
        import re
        if not cost_str or cost_str.strip() == "":
            return 0, 0

        # Look for pattern like "3 (9)" where 3 = revolution cost, 9 = normal cost
        match = re.match(r'(\d+)\s*\((\d+)\)', cost_str.strip())
        if match:
            revolution_cost = int(match.group(1))
            normal_cost = int(match.group(2))
            return normal_cost, revolution_cost

        # If no revolution cost in parentheses, assume normal cost only
        try:
            normal_cost = int(cost_str.strip())
            return normal_cost, normal_cost  # Same cost for both
        except ValueError:
            return 0, 0

    def get_research_cost(self, is_revolution: bool = False) -> int:
        """Get the cost to research this government"""
        return self.revolution_cost if is_revolution else self.normal_cost

    def get_cost_info(self) -> Dict[str, int]:
        """Get detailed cost information"""
        return {
            'normal_cost': self.normal_cost,
            'revolution_cost': self.revolution_cost,
            'civil_actions': self.civil_actions,
            'military_actions': self.military_actions,
            'building_limit': self.building_limit
        }

class Special(Technology):
    """Special technology cards"""

    def __init__(self, name: str, special_type: str, age: str, tech_cost: int = 0,
                 effects: Dict[str, Any] = None, card_text: str = ""):
        super().__init__(name, age, tech_cost, card_text)
        self.special_type = special_type  # Military, Civil
        self.effects = effects or {}

class ActionCard(CivilCard):
    """Action cards that provide immediate effects"""

    def __init__(self, name: str, age: str, effects: Dict[str, Any] = None,
                 card_text: str = ""):
        super().__init__(name, age, 0, card_text)  # Action cards don't have tech cost
        self.effects = effects or {}

class Leader(CivilCard):
    """Leader cards"""

    def __init__(self, name: str, age: str, effects: Dict[str, Any] = None,
                 card_text: str = ""):
        super().__init__(name, age, 0, card_text)  # Leaders don't have tech cost
        self.effects = effects or {}

# Factory functions to create cards from CSV data

def create_card_from_csv_row(row: Dict[str, str]) -> Card:
    """Create appropriate card object from CSV row data

    Args:
        row (Dict[str, str]): CSV row data as dictionary

    Returns:
        Card: Appropriate card object    """
    category = row['Category']
    card_type = row['Type']
    name = row['Card Name']
    age = row['Age']
    card_text = row['Card text and comments']

    # Parse tech cost (handle government format like "3 (9)")
    tech_cost = 0
    if category == 'Govt':
        # For governments, pass the string as is for parsing
        tech_cost_str = row['Tech cost']
    else:
        # For other cards, parse as integer
        tech_cost = int(row['Tech cost']) if row['Tech cost'] and row['Tech cost'] != '' else 0

    # Parse build cost (handle wonder format like "2 2 2")
    build_cost = 0
    build_cost_str = row['Build cost']
    if category != 'Wonder':
        build_cost = int(build_cost_str) if build_cost_str and build_cost_str != '' else 0

    # Parse production values
    production = {}
    if row['Production Food']: production['food'] = int(row['Production Food'])
    if row['Production Material']: production['material'] = int(row['Production Material'])
    if row['Production Culture']: production['culture'] = int(row['Production Culture'])
    if row['Production Strength']: production['strength'] = int(row['Production Strength'])
    if row['Production Happy']: production['happy'] = int(row['Production Happy'])
    if row['Production Science']: production['science'] = int(row['Production Science'])

    # Parse gain values
    gain = {}
    if row['Gain Food']: gain['food'] = int(row['Gain Food'])
    if row['Gain Material']: gain['material'] = int(row['Gain Material'])
    if row['Gain Culture']: gain['culture'] = int(row['Gain Culture'])
    if row['Gain Strength']: gain['strength'] = int(row['Gain Strength'])
    if row['Gain Happy']: gain['happy'] = int(row['Gain Happy'])
    if row['Gain Science']: gain['science'] = int(row['Gain Science'])

    # Create appropriate card type
    if category == 'Production':
        return ProductionBuilding(
            name=name,
            building_type=card_type,
            age=age,
            tech_cost=tech_cost,
            build_cost=build_cost,
            production=production,
            card_text=card_text
        )
    elif category == 'Urban':
        return UrbanBuilding(
            name=name,
            building_type=card_type,
            age=age,
            tech_cost=tech_cost,
            build_cost=build_cost,
            production=production,
            gain=gain,
            card_text=card_text
        )
    elif category == 'Military':
        strength = production.get('strength', 0)
        return MilitaryTechnology(
            name=name,
            unit_type=card_type,
            age=age,
            tech_cost=tech_cost,            build_cost=build_cost,
            strength=strength,
            card_text=card_text
        )
    elif category == 'Wonder':
        return Wonder(
            name=name,
            age=age,
            build_cost_steps=build_cost_str,  # Pass the string for parsing
            production=production,
            gain=gain,
            card_text=card_text
        )
    elif category == 'Govt':
        # Parse government-specific values
        civil_actions = int(row['Produce civil action']) if row['Produce civil action'] else 4
        military_actions = int(row['Produce military action']) if row['Produce military action'] else 2

        # Extract building limit from card text
        building_limit = 2  # Default
        if 'Building limit:' in card_text:
            import re
            match = re.search(r'Building limit: (\d+)', card_text)
            if match:
                building_limit = int(match.group(1))

        return Government(
            name=name,
            age=age,
            tech_cost_str=tech_cost_str,  # Pass the string for parsing
            civil_actions=civil_actions,
            military_actions=military_actions,
            building_limit=building_limit,
            production=production,
            gain=gain,
            card_text=card_text
        )
    elif category == 'Special':
        return Special(
            name=name,
            special_type=card_type,
            age=age,
            tech_cost=tech_cost,
            card_text=card_text
        )
    elif category == 'Action':
        return ActionCard(
            name=name,
            age=age,
            card_text=card_text
        )
    elif category == 'Leader':
        return Leader(
            name=name,
            age=age,
            card_text=card_text
        )
    else:
        # Fallback to basic civil card
        return CivilCard(
            name=name,
            age=age,
            tech_cost=tech_cost,
            card_text=card_text
        )
