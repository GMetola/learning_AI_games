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

class Building(Technology):
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

class ProductionBuilding(Building):
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

class UrbanBuilding(Building):
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

class Monument(Technology):
    """Monument technology cards"""

    def __init__(self, name: str, special_type: str, age: str, tech_cost: int = 0,
                 effects: Dict[str, Any] = None, card_text: str = ""):
        super().__init__(name, age, tech_cost, card_text)
        self.special_type = special_type  # Military, Civil
        self.effects = effects or {}

class ActionCard(CivilCard):
    """Action cards that provide immediate effects with complex cost notations"""

    def __init__(self, name: str, age: str, cost_notation: str = "",
                 effects: Dict[str, Any] = None, card_text: str = ""):
        super().__init__(name, age, 0, card_text)  # Action cards don't have tech cost
        self.cost_notation = cost_notation  # Raw cost string like "2 W", "P 1", etc.
        self.parsed_cost = parse_action_cost(cost_notation)
        self.effects = effects or {}

    def get_cost_description(self) -> str:
        """Get human-readable cost description"""
        if not self.parsed_cost:
            return "No cost"
        return self.parsed_cost.get('description', self.cost_notation)

class Leader(CivilCard):
    """Leader cards"""

    def __init__(self, name: str, age: str, effects: Dict[str, Any] = None,
                 card_text: str = ""):
        super().__init__(name, age, 0, card_text)  # Leaders don't have tech cost
        self.effects = effects or {}

# Factory functions to create cards from CSV data

def safe_parse_int(value: str) -> int:
    """Safely parse string to integer, handling special notations

    Args:
        value (str): String value to parse

    Returns:
        int: Parsed integer or 0 if cannot parse
    """
    if not value or value.strip() == "":
        return 0

    value = value.strip()

    # Handle quotes (remove them first)
    if '"' in value:
        value = value.replace('"', '')

    # Handle special notations
    if value == "?" or "?" in value:
        return 0  # Unknown values default to 0

    # Handle single letters or complex notations
    if any(char in value for char in ['W', 'P', 'U', 'M', 'T']) and len(value) <= 3:
        return 0  # Complex action card costs default to 0

    # Try to parse as integer
    try:
        return int(value)
    except ValueError:
        # Extract first number if present
        import re
        numbers = re.findall(r'\d+', value)
        if numbers:
            return int(numbers[0])
        return 0

def safe_parse_value(value: str) -> int:
    """Safely parse a value that might contain special notations

    Args:
        value (str): Value to parse

    Returns:
        int: Parsed integer or 0 for special notations
    """
    if not value or value.strip() == '':
        return 0

    value = value.strip()

    # Handle special cases that should return 0 for now
    # These are complex action card costs that need special handling
    if value == '?' or 'W' in value or 'P' in value or 'U' in value or 'M' in value or 'T' in value:
        return 0

    # Remove quotes if present
    if '"' in value:
        value = value.replace('"', '')

    # Try to parse as integer
    try:
        return int(value)
    except ValueError:
        # Extract first number if present
        import re
        numbers = re.findall(r'\d+', value)
        if numbers:
            return int(numbers[0])
        return 0

def parse_action_cost(cost_str: str) -> Dict[str, Any]:
    """Parse action card cost notation

    Action card costs follow this logic:
    - Divide by spaces
    - If first character is number: reduces material cost
    - If first character is letter: gives materials back after construction
    - Letters: W=wonder, U=urban, M=military, P=production, PU=both prod/urban, T=technology(science)
    - ? = multiplier based on number of players (check card description)

    Args:
        cost_str (str): Cost string like "2 W", "P 1", "?", etc.

    Returns:
        Dict[str, Any]: Parsed cost information
    """
    if not cost_str or cost_str.strip() == '':
        return {}

    cost_str = cost_str.strip()

    # Handle multiplier
    if cost_str == '?':
        return {'type': 'multiplier', 'description': 'Based on number of players'}

    # Split by spaces
    parts = cost_str.split()
    if len(parts) != 2:
        return {'raw': cost_str}  # Complex format, store as raw

    first_part, second_part = parts

    # Determine if first character is number or letter
    if first_part[0].isdigit():
        # Number first: reduces cost
        amount = int(first_part)
        target = second_part.upper()
        return {
            'type': 'cost_reduction',
            'amount': amount,
            'target': target,
            'description': f'Reduces {target} cost by {amount}'
        }
    else:
        # Letter first: gives materials back
        target = first_part.upper()
        amount = int(second_part)
        return {
            'type': 'material_return',
            'target': target,
            'amount': amount,
            'description': f'Returns {amount} materials after {target} construction'
        }

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
        build_cost = int(build_cost_str) if build_cost_str and build_cost_str != '' else 0    # Parse production values safely
    production = {}
    if row['Production Food']: production['food'] = safe_parse_int(row['Production Food'])
    if row['Production Material']: production['material'] = safe_parse_int(row['Production Material'])
    if row['Production Culture']: production['culture'] = safe_parse_int(row['Production Culture'])
    if row['Production Strength']: production['strength'] = safe_parse_int(row['Production Strength'])
    if row['Production Happy']: production['happy'] = safe_parse_int(row['Production Happy'])
    if row['Production Science']: production['science'] = safe_parse_int(row['Production Science'])

    # Parse gain values safely
    gain = {}
    if row['Gain Food']: gain['food'] = safe_parse_int(row['Gain Food'])
    if row['Gain Material']: gain['material'] = safe_parse_int(row['Gain Material'])
    if row['Gain Culture']: gain['culture'] = safe_parse_int(row['Gain Culture'])
    if row['Gain Strength']: gain['strength'] = safe_parse_int(row['Gain Strength'])
    if row['Gain Happy']: gain['happy'] = safe_parse_int(row['Gain Happy'])
    if row['Gain Science']: gain['science'] = safe_parse_int(row['Gain Science'])

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
    elif category == 'Monument':
        return Monument(
            name=name,
            special_type=card_type,
            age=age,
            tech_cost=tech_cost,
            card_text=card_text
        )
    elif category == 'Action':
        # For action cards, the cost notation might be in various columns
        # Check common columns that might contain action costs
        cost_notation = ""
        for col in ['Build cost', 'Gain Material', 'Production Material']:
            if row.get(col) and row[col].strip():
                cost_notation = row[col].strip()
                break

        return ActionCard(
            name=name,
            age=age,
            cost_notation=cost_notation,
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
