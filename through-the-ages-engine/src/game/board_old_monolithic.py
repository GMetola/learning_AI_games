from typing import Dict, List, Optional, Tuple, Any
import logging
from .cards import Card

class GameBoard:
    """Tablero principal del juego que gestiona elementos compartidos"""

    def __init__(self, num_players: int):
        """Inicializa el tablero principal del juego

        Args:
            num_players (int): Número de jugadores en la partida
        """
        self.num_players = num_players

        # TABLEROS INDIVIDUALES DE JUGADORES
        self.player_boards = {}
        for player_id in range(1, num_players + 1):
            self.player_boards[player_id] = PlayerBoard(player_id)

        # CARTAS VISIBLES EN EL TABLERO
        self.civil_cards_row = []      # Fila de cartas civiles visibles
        self.military_cards_row = []   # Fila de cartas militares visibles
        self.current_events = []       # Eventos actuales del turno

        # CARTAS VISIBLES (NUEVO - para compatibilidad con tests)
        self.visible_civil_cards = []  # Lista de cartas civiles visibles
        self.visible_military_cards = [] # Lista de cartas militares visibles

        # MAZOS DE CARTAS
        self.civil_deck_a = []         # Mazo de cartas civiles edad A
        self.civil_deck_b = []         # Mazo de cartas civiles edad B
        self.civil_deck_c = []         # Mazo de cartas civiles edad C
        self.military_deck = []        # Mazo de cartas militares
        self.event_deck = []           # Mazo de eventos

        # CONFIGURACIÓN GLOBAL
        self.current_age = "A"         # Edad actual del juego
        self.peaceful_version = True   # Versión pacífica del juego
        self.max_visible_civil_cards = 13  # Número máximo de cartas civiles visibles

        # TECNOLOGÍAS INICIALES DISPONIBLES
        self.initial_technologies = [
            "Agriculture", "Bronze", "Filosofía", "Religión",
            "Guerreros", "Despotismo"
        ]

        # COUNTERS GLOBALES
        self.turn_number = 1
        self.phase = "political"       # "political", "action", "production"

    def get_player_board(self, player_id: int) -> Optional['PlayerBoard']:
        """Obtiene el tablero de un jugador específico

        Args:
            player_id (int): ID del jugador

        Returns:
            Optional[PlayerBoard]: Tablero del jugador o None si no existe
        """
        return self.player_boards.get(player_id)

    def advance_age(self):
        """Avanza la edad del juego"""
        if self.current_age == "A":
            self.current_age = "B"
        elif self.current_age == "B":
            self.current_age = "C"

        logging.info(f"Edad avanzada a: {self.current_age}")

    def get_available_civil_cards(self) -> List[Card]:
        """Obtiene las cartas civiles disponibles en la fila

        Returns:
            List[Card]: Lista de cartas civiles disponibles
        """
        return self.civil_cards_row.copy()

    def get_available_military_cards(self) -> List[Card]:
        """Obtiene las cartas militares disponibles

        Returns:
            List[Card]: Lista de cartas militares disponibles
        """
        return self.military_cards_row.copy()

    def setup_initial_civil_row(self):
        """Configura la fila inicial de cartas civiles"""
        pass


class PlayerBoard:
    """Player's individual board with card collections and resource management

    The PlayerBoard now contains organized card collections as specified:

    Unique Attributes (single card instances):
    - leader: Leader card (None by default)
    - government: Government card (Despotism by default)

    Multiple Attributes (lists of card instances):
    - wonders: List of Wonder cards
    - monuments: List of Monument cards (not in v0.1)
    - hand_cards: List of cards in player's hand
    - production_buildings: List of ProductionBuilding cards
    - urban_buildings: List of UrbanBuilding cards

    The board automatically loads initial Age A technologies from initial_technologies.csv
    and provides government-based action limits and building restrictions.
    """

    def __init__(self, player_id: int):
        """Inicializa tablero individual del jugador

        Args:
            player_id (int): ID único del jugador
        """
        self.player_id = player_id

        # RESERVAS INDIVIDUALES DEL JUGADOR
        # Reserva amarilla (población y trabajadores)
        self.yellow_reserves = {
            'total_tokens': 24,
            'groups': [                    # Grupos de fichas amarillas
                {'tokens': 2, 'occupied': True, 'consumo': -1, 'coste_nuevo': 3},
                {'tokens': 4, 'occupied': True, 'consumo': -2, 'coste_nuevo': 4},
                {'tokens': 2, 'occupied': True, 'consumo': -2, 'coste_nuevo': 4},
                {'tokens': 2, 'occupied': True, 'consumo': -3, 'coste_nuevo': 5},
                {'tokens': 2, 'occupied': True, 'consumo': -3, 'coste_nuevo': 5},
                {'tokens': 2, 'occupied': True, 'consumo': -4, 'coste_nuevo': 7},
                {'tokens': 2, 'occupied': True, 'consumo': -4, 'coste_nuevo': 7},
                {'tokens': 2, 'occupied': True, 'consumo': -6, 'coste_nuevo': 7},
            ],
            'available_workers': 1,        # Trabajadores disponibles
            'technology_workers': {        # Trabajadores asignados a tecnologías iniciales
                'Agriculture': 2,          # 2 trabajadores en Agriculture nivel A
                'Bronze': 2,              # 2 trabajadores en Bronze
                'Philosophy': 1,           # 1 trabajador en Philosophy
                'Religion': 0             # 0 trabajadores en Religion (aunque esté investigada)
            }
        }

        # Reserva azul (recursos y corrupción)
        self.blue_reserves = {
            'total_blue_tokens': 16,        # Fichas azules totales
            'production_storage': {},      # Recursos almacenados por tecnología
            'groups': [                    # Grupos de fichas azules
                {'tokens': 6, 'occupied': True, 'corruption': -2},
                {'tokens': 5, 'occupied': True, 'corruption': -4},
                {'tokens': 5, 'occupied': True, 'corruption': -6}
            ]
        }

        # RECURSOS DEL JUGADOR
        self.resources = {
            'food': 0,
            'material': 0,
            'science': 1,      # Comienza con 1 ciencia
            'culture': 0,
            'happy': 0,
            'strength': 1      # Comienza con 1 fuerza militar
        }

        # INDICADORES Y PUNTOS
        self.indicators = {
            'science': 1,      # Indicador de ciencia
            'culture': 0,      # Indicador de cultura
            'happiness': 1,    # Puntos de felicidad iniciales
            'military': 1      # Indicador militar
        }

        self.points = {
            'culture': 0,      # Puntos de cultura acumulados
            'science': 0       # Puntos de ciencia acumulados
        }

        # PLAYER CARD COLLECTIONS
        # Load initial technologies from CSV
        from .card_loader import load_initial_technologies, get_initial_government

        # Load initial technologies
        initial_techs = load_initial_technologies()

        # Separate technologies and government
        initial_buildings = []
        initial_government = None

        for card in initial_techs:
            if hasattr(card, 'revolution_cost'):  # This is a government
                initial_government = card
            else:  # This is a building/technology
                initial_buildings.append(card)

        # Unique attributes (single card instances)
        self.leader = None  # Leader card (None by default)
        self.government = initial_government  # Government card (Despotism by default)

        # Multiple attributes (lists of card instances)
        self.wonders = []  # List of Wonder cards
        self.monuments = []  # List of Monument cards (not in v0.1)
        self.hand_cards = []  # List of cards in hand
        self.production_buildings = []  # List of ProductionBuilding cards
        self.urban_buildings = []  # List of UrbanBuilding cards

        # Initialize with starting buildings from CSV
        for card in initial_buildings:
            if card.__class__.__name__ == 'ProductionBuilding':
                self.production_buildings.append(card)
            elif card.__class__.__name__ == 'UrbanBuilding':
                self.urban_buildings.append(card)

        # Legacy technology tracking (for compatibility with existing code)
        self.current_technologies = {}
        for card in initial_buildings:
            self.current_technologies[card.name] = {
                'card_object': card,
                'production': getattr(card, 'production', {})
            }

        # Set active government (alias for backward compatibility)
        self.active_government = self.government

        # CONFIGURACIÓN POBLACIÓN
        # Costes incrementales para aumentar población (por jugador individual)
        self.population_costs = [3, 4, 5, 5, 7, 7, 7, 7]  # Comida por aumento
        self.population_increases = 0  # Cuántas veces ha aumentado población

        # TRACKING DE MEJORAS POR TURNO
        self.turn_improvements = {
            'technologies_researched': [],      # Tecnologías investigadas este turno
            'cards_in_hand': 0,                # Cartas en mano
            'civil_actions_bonus': 0,          # Bonificación a acciones civiles
            'military_actions_bonus': 0        # Bonificación a acciones militares
        }

        # TRACKING DE ACCIONES USADAS (para el sistema de acciones)
        self.used_civil_actions = 0
        self.used_military_actions = 0

        # Triggers de consumo de comida (se activan al llenar grupos específicos)
        self.consumption_triggers = {
            2: -1,  # Grupo 2: -1 comida por turno
            4: -2,  # Grupo 4: -2 comida por turno
            6: -3,  # Grupo 6: -3 comida por turno
            8: -4   # Grupo 8: -4 comida por turno
        }
        self.active_consumption = 0  # Consumo de comida activo

        # CONTADORES DE ACCIONES POR TURNO
        self.used_civil_actions = 0     # Acciones civiles usadas en el turno actual
        self.used_military_actions = 0  # Acciones militares usadas en el turno actual

    def increase_population(self, food_cost: int) -> bool:
        """Aumenta la población moviendo una ficha amarilla de grupo ocupado

        Args:
            food_cost (int): Coste en comida para aumentar población

        Returns:
            bool: True si se pudo aumentar la población
        """
        # VERIFICACIÓN FICHAS AMARILLAS DISPONIBLES
        if not self._has_available_yellow_tokens():
            return False

        # VERIFICACIÓN COMIDA
        if self.resources['food'] < food_cost:
            return False

        # PAGO COMIDA
        self.resources['food'] -= food_cost

        # TOMA FICHA AMARILLA DEL PRIMER GRUPO OCUPADO
        self._take_yellow_token_from_group()

        # MUEVE A TRABAJADORES DISPONIBLES
        self.yellow_reserves['available_workers'] += 1

        # ACTUALIZA CONTADOR
        self.population_increases += 1

        logging.info(f"Jugador {self.player_id}: población aumentada, coste {food_cost} comida")
        return True

    def _has_available_yellow_tokens(self) -> bool:
        """Verifica si hay fichas amarillas disponibles en grupos ocupados"""
        for group in self.yellow_reserves['groups']:
            if group['occupied'] and group['tokens'] > 0:
                return True
        return False

    def _take_yellow_token_from_group(self) -> bool:
        """Toma una ficha amarilla del primer grupo ocupado disponible"""
        for group in self.yellow_reserves['groups']:
            if group['occupied'] and group['tokens'] > 0:
                group['tokens'] -= 1

                # MARCAR GRUPO COMO NO OCUPADO SI SE VACÍA
                if group['tokens'] == 0:
                    group['occupied'] = False
                    logging.info(f"Jugador {self.player_id}: grupo amarillo vaciado, marcado como no ocupado")

                return True
        return False

    def get_population_cost(self) -> int:
        """Obtiene el coste en comida para aumentar población desde el primer grupo no ocupado

        Returns:
            int: Coste en comida (2 si todos los grupos están ocupados)
        """
        # BUSCA PRIMER GRUPO NO OCUPADO
        for group in self.yellow_reserves['groups']:
            if not group['occupied']:
                return group['coste_nuevo']

        # SI TODOS LOS GRUPOS ESTÁN OCUPADOS, COSTO ES 2
        return 2

    def get_food_consumption(self) -> int:
        """Obtiene el consumo de comida actual desde el primer grupo no ocupado

        Returns:
            int: Consumo de comida por turno (0 si todos los grupos están ocupados)
        """
        # BUSCA PRIMER GRUPO NO OCUPADO
        for group in self.yellow_reserves['groups']:
            if not group['occupied']:
                return abs(group['consumo'])  # Valor positivo del consumo

        # SI TODOS LOS GRUPOS ESTÁN OCUPADOS, NO HAY CONSUMO
        return 0

    def can_increase_population(self) -> bool:
        """Verifica si puede aumentar población

        Returns:
            bool: True si puede aumentar población
        """
        return (self._has_available_yellow_tokens() and
                self.resources['food'] >= self.get_population_cost())

    def assign_worker_to_building(self, tech_card: Card) -> bool:
        """Asigna un trabajador a una tecnología específica

        Args:
            tech_card (Card): Objeto de carta de la tecnología

        Returns:
            bool: True si se pudo asignar el trabajador
        """
        tech_name = tech_card.name
        # Verifica si hay trabajadores disponibles
        if self.yellow_reserves['available_workers'] <= 0:
            return False

        # Verifica si la tecnología existe
        if tech_name not in self.current_technologies:
            return False

        # Verifica si ya hay trabajadores asignados a esta tecnología
        if tech_name in self.yellow_reserves['technology_workers']:
            # TODO: el máximo de trabajadores deberá ser definido por el tipo de gobierno.
            # TODO: Los gobiernos están definidos como Govt en el archivo cards.py y el máximo de trabajadores por tecnología está definido en la columna 'Card text and comments'
            MAX_WORKERS_PER_TECH = 2  # TEMPORAL
            if self.yellow_reserves['technology_workers'][tech_name] >= MAX_WORKERS_PER_TECH:
                logging.warning(f"Máximo de trabajadores alcanzado para {tech_name}")
                return False

        # Verifica que se puede pagar el coste de asignación (materiales)
        if self.resources['material'] < tech_card.build_cost:
            logging.warning(f"Jugador {self.player_id}: insuficientes materiales para asignar trabajador a {tech_name} (necesita {tech_card.build_cost}, tiene {self.resources['material']})")
            return False

        # ASIGNACIÓN
        # Paga el coste de asignación
        self.resources['material'] -= tech_card.build_cost
        logging.info(f"Jugador {self.player_id}: pagó {tech_card.build_cost} materiales para asignar trabajador a {tech_name}")

        # Mueve trabajador: disponibles -> tecnología específica
        self.yellow_reserves['available_workers'] -= 1

        if tech_name not in self.yellow_reserves['technology_workers']:
            self.yellow_reserves['technology_workers'][tech_name] = 0
        self.yellow_reserves['technology_workers'][tech_name] += 1

        return True

    def collect_production_resources(self, tech_name: str, amount: int):
        """Recoge recursos de producción y los almacena con fichas azules

        Args:
            tech_name (str): Tecnología que produce
            amount (int): Cantidad de recursos producidos
        """
        # ALMACENA RECURSOS POR TECNOLOGÍA
        if tech_name not in self.blue_reserves['production_storage']:
            self.blue_reserves['production_storage'][tech_name] = 0

        self.blue_reserves['production_storage'][tech_name] += amount

        # TOMA FICHAS AZULES DEL PRIMER GRUPO OCUPADO
        for _ in range(amount):
            if not self._take_blue_token_from_group():
                logging.warning(f"Jugador {self.player_id}: no hay más fichas azules disponibles")
                break

    def _take_blue_token_from_group(self) -> bool:
        """Toma una ficha azul del primer grupo ocupado disponible"""
        for i, group in enumerate(self.blue_reserves['groups']):
            if group['occupied'] and group['tokens'] > 0:
                group['tokens'] -= 1
                # MARCAR GRUPO COMO NO OCUPADO SI SE VACÍA
                if group['tokens'] == 0:
                    group['occupied'] = False
                    logging.info(f"Jugador {self.player_id}: grupo azul {i} vaciado, marcado como no ocupado")
                return True
        return False

    def get_corruption_penalty(self) -> int:
        """Obtiene la penalización por corrupción desde el primer grupo no ocupado

        Returns:
            int: Puntos de corrupción por turno (0 si todos los grupos están ocupados)
        """
        # BUSCA PRIMER GRUPO NO OCUPADO
        for group in self.blue_reserves['groups']:
            if not group['occupied']:
                return abs(group['corruption'])  # Valor positivo de la corrupción

        # SI TODOS LOS GRUPOS ESTÁN OCUPADOS, NO HAY CORRUPCIÓN
        return 0

    def _update_corruption_spaces(self):
        """Actualiza espacios de corrupción según fichas azules disponibles - OBSOLETO con nuevo sistema de grupos"""
        # Este método es obsoleto con el nuevo sistema de grupos
        # La corrupción ahora se calcula directamente desde get_corruption_penalty()
        pass

    def calculate_corruption_penalty(self) -> int:
        """Calcula penalización total por corrupción

        Returns:
            int: Puntos de corrupción a pagar
        """
        return self.get_corruption_penalty()

    def check_revolt_condition(self) -> bool:
        """Verifica condición de revuelta según las reglas

        Returns:
            bool: True si hay revuelta (trabajadores desocupados > felicidad)
        """
        unemployed_workers = self.yellow_reserves['available_workers']
        happiness_points = self.indicators['happiness']

        return unemployed_workers > happiness_points

    def pay_corruption(self) -> Dict[str, int]:
        """Paga corrupción al final del turno

        Returns:
            Dict: Detalles del pago realizado
        """
        corruption_cost = self.calculate_corruption_penalty()

        if corruption_cost <= 0:
            return {'corruption': 0, 'resources_paid': 0}

        resources_paid = 0
        food_paid = 0
        culture_lost = 0

        # PAGO CORRUPCIÓN
        if self.resources['material'] >= corruption_cost:
            self.resources['material'] -= corruption_cost
            resources_paid = corruption_cost
        else:
            resources_paid = self.resources['material'].copy()
            self.resources['material'] = 0
            remaining_cost = corruption_cost - resources_paid

            # 2. Usar comida para el resto
            logging.debug(f"Jugador {self.player_id} pagando corrupción restante: {remaining_cost} con comida")
            if self.resources['food'] >= remaining_cost:
                self.resources['food'] -= remaining_cost
                food_paid = remaining_cost
            else:
                food_paid = self.resources['food']
                self.resources['food'] = 0
                remaining_cost -= food_paid

                # 3. Perder cultura por lo que no se pudo pagar
                culture_lost = remaining_cost
                self.resources['culture'] = max(0, self.resources['culture'] - culture_lost)

        return {
            'corruption': corruption_cost,
            'resources_paid': resources_paid,
            'food_paid': food_paid,
            'culture_lost': culture_lost
        }

    def calculate_production(self) -> Dict[str, int]:
        """Calcula la producción total de todos los recursos

        Returns:
            Dict[str, int]: Producción de cada recurso
        """
        production = {'food': 0, 'material': 0, 'science': 0, 'culture': 0, 'happy': 0}

        # PRODUCCIÓN POR TECNOLOGÍAS
        for tech_name, workers_assigned in self.yellow_reserves['technology_workers'].items():
            if tech_name in self.current_technologies and workers_assigned > 0:
                tech_production = self.current_technologies[tech_name].get('production', {})

                # Multiplicar producción por trabajadores asignados
                for resource, base_amount in tech_production.items():
                    production[resource] = production.get(resource, 0) + (base_amount * workers_assigned)

        return production

    def execute_production_phase(self) -> Dict[str, Any]:
        """Ejecuta la fase de producción al final del turno

        Returns:
            Dict[str, Any]: Detalles de la producción ejecutada
        """
        # VERIFICAR REVUELTA
        if self.check_revolt_condition():
            logging.warning(f"Jugador {self.player_id} en revuelta - producción bloqueada")
            return {
                'revolt': True,
                'production': {'food': 0, 'material': 0, 'science': 0, 'culture': 0, 'happy': 0},
                'consumption': {},
                'corruption': {'corruption': 0, 'resources_paid': 0, 'food_paid': 0, 'culture_lost': 0},
                'net_resources': {'food': 0, 'material': 0, 'science': 0, 'culture': 0}
            }

        # CALCULAR PRODUCCIÓN
        production = self.calculate_production()

        # CULTURA Y CIENCIA
        self.resources['culture'] += production['culture']
        self.resources['science'] += production['science']

        # CORRUPCIÓN
        corruption_payment = self.pay_corruption()

        # PRODUCCIÓN DE COMIDA
        self.resources['food'] += net_food

        # CONSUMO DE COMIDA
        food_consumption = abs(self.active_consumption)
        net_food = production['food'] - food_consumption

        # PRODUCCIÓN MATERIAL
        self.resources['material'] += production['material']

        # ACTUALIZAR INDICADORES DE FELICIDAD
        if production['happiness'] > 0:
            self.indicators['happiness'] += production['happiness']

        # CALCULAR RECURSOS NETOS
        net_resources = {
            'food': net_food - corruption_payment['food_paid'],
            'material': production['material'] - corruption_payment['resources_paid'],
            'science': production['science'],
            'culture': production['culture'] - corruption_payment['culture_lost']
        }

        logging.info(f"Jugador {self.player_id} - Producción: {production}, Consumo: -{food_consumption}, Corrupción: -{corruption_payment['corruption']}")

        return {
            'revolt': False,
            'production': production,
            'consumption': {'food': food_consumption},
            'corruption': corruption_payment,
            'net_resources': net_resources
        }

    def complete_turn(self) -> Dict[str, Any]:
        """Completa el turno del jugador aplicando todas las mejoras y costes

        Returns:
            Dict: Detalles de lo que sucedió en el turno
        """
        turn_summary = {
            'production': {},
            'consumption': 0,
            'corruption': 0,
            'technologies_researched': self.turn_improvements['technologies_researched'].copy(),
            'cards_in_hand': self.turn_improvements['cards_in_hand'],
            'civil_actions_total': self.get_total_civil_actions(),
            'military_actions_total': self.get_total_military_actions()
        }

        # PRODUCCIÓN DE RECURSOS
        production_results = self.calculate_production()
        turn_summary['production'] = production_results

        # APLICAR PRODUCCIÓN A RECURSOS
        for resource, amount in production_results.items():
            if resource in self.resources:
                self.resources[resource] += amount

        # CONSUMO DE COMIDA
        food_consumption = self.get_food_consumption()
        if food_consumption > 0:
            self.resources['food'] = max(0, self.resources['food'] - food_consumption)
            turn_summary['consumption'] = food_consumption

        # PAGO DE CORRUPCIÓN
        corruption_penalty = self.get_corruption_penalty()
        if corruption_penalty > 0:
            # TODO: Implementar orden de pago de corrupción (ciencia -> acciones civiles -> acciones militares)
            corruption_paid = self._pay_corruption_resources(corruption_penalty)
            turn_summary['corruption'] = corruption_paid

        # RESETEAR MEJORAS DEL TURNO
        self.turn_improvements['technologies_researched'] = []
        self.used_civil_actions = 0
        self.used_military_actions = 0

        logging.info(f"Jugador {self.player_id}: turno completado - {turn_summary}")
        return turn_summary

    def _pay_corruption_resources(self, corruption_amount: int) -> int:
        """Paga corrupción usando el orden correcto de recursos

        Args:
            corruption_amount (int): Cantidad de corrupción a pagar

        Returns:
            int: Cantidad de corrupción realmente pagada
        """
        paid = 0
        remaining = corruption_amount

        # ORDEN DE PAGO: ciencia -> acciones civiles -> acciones militares
        # 1. CIENCIA
        science_payment = min(remaining, self.resources['science'])
        self.resources['science'] -= science_payment
        paid += science_payment
        remaining -= science_payment

        # 2. ACCIONES CIVILES (representadas como recursos temporales)
        if remaining > 0:
            civil_payment = min(remaining, self.get_civil_actions_available())
            # TODO: Reducir acciones civiles disponibles para próximo turno
            paid += civil_payment
            remaining -= civil_payment

        # 3. ACCIONES MILITARES
        if remaining > 0:
            military_payment = min(remaining, self.get_military_actions_available())
            # TODO: Reducir acciones militares disponibles para próximo turno
            paid += military_payment
            remaining -= military_payment

        return paid

    def get_total_civil_actions(self) -> int:
        """Obtiene el total de acciones civiles disponibles por turno"""
        return self.get_civil_actions_per_turn()

    def get_total_military_actions(self) -> int:
        """Obtiene el total de acciones militares disponibles por turno"""
        return self.get_military_actions_per_turn()

    def get_civil_actions_available(self) -> int:
        """Obtiene acciones civiles restantes en el turno actual"""
        return max(0, self.get_total_civil_actions() - self.used_civil_actions)

    def get_military_actions_available(self) -> int:
        """Obtiene acciones militares restantes en el turno actual"""
        return max(0, self.get_total_military_actions() - self.used_military_actions)

    def add_technology_researched(self, tech_name: str):
        """Añade una tecnología a la lista de investigadas este turno"""
        if tech_name not in self.turn_improvements['technologies_researched']:
            self.turn_improvements['technologies_researched'].append(tech_name)

    def update_cards_in_hand(self, count: int):
        """Actualiza el número de cartas en mano"""
        self.turn_improvements['cards_in_hand'] = count

    def add_civil_action_bonus(self, bonus: int):
        """Añade bonificación a acciones civiles"""
        self.turn_improvements['civil_actions_bonus'] += bonus

    def add_military_action_bonus(self, bonus: int):
        """Añade bonificación a acciones militares"""
        self.turn_improvements['military_actions_bonus'] += bonus

    def get_civil_actions_per_turn(self) -> int:
        """Get total civil actions per turn based on active government and bonuses

        Returns:
            int: Total civil actions available per turn
        """
        base_actions = 0
        if self.active_government and hasattr(self.active_government, 'civil_actions'):
            base_actions = self.active_government.civil_actions

        bonus_actions = self.turn_improvements.get('civil_actions_bonus', 0)
        return base_actions + bonus_actions

    def get_military_actions_per_turn(self) -> int:
        """Get total military actions per turn based on active government and bonuses

        Returns:
            int: Total military actions available per turn
        """
        base_actions = 0
        if self.active_government and hasattr(self.active_government, 'military_actions'):
            base_actions = self.active_government.military_actions

        bonus_actions = self.turn_improvements.get('military_actions_bonus', 0)
        return base_actions + bonus_actions

    def get_building_limit(self) -> int:
        """Get building limit based on active government

        Returns:
            int: Maximum number of buildings that can be built
        """
        if self.active_government and hasattr(self.active_government, 'building_limit'):
            return self.active_government.building_limit
        return 2  # Default for Despotism

    def set_government(self, government_card):
        """Set a new active government

        Args:
            government_card: Government card object
        """
        self.active_government = government_card

    def add_card_to_hand(self, card):
        """Add a card to the player's hand

        Args:
            card: Card object to add to hand
        """
        self.hand_cards.append(card)

    def remove_card_from_hand(self, card):
        """Remove a card from the player's hand

        Args:
            card: Card object to remove from hand

        Returns:
            bool: True if card was removed, False if not found
        """
        if card in self.hand_cards:
            self.hand_cards.remove(card)
            return True
        return False

    def add_production_building(self, card):
        """Add a production building to the player's board

        Args:
            card: ProductionBuilding card object
        """
        self.production_buildings.append(card)
        # Also add to legacy tracking for compatibility
        self.current_technologies[card.name] = {
            'card_object': card,
            'production': getattr(card, 'production', {})
        }

    def add_urban_building(self, card):
        """Add an urban building to the player's board

        Args:
            card: UrbanBuilding card object or card name (str)
        
        Raises:
            ValueError: If card is not found or not an urban building
        """
        from .card_classes import UrbanBuilding
        from .card_loader import CardLoader
        
        # Handle string input (card name) by loading the card
        if isinstance(card, str):
            loader = CardLoader()
            card = loader.get_card_by_name(card)
            if not card:
                raise ValueError(f"Card '{card}' not found")
        
        # Validate that it's an UrbanBuilding
        if not isinstance(card, UrbanBuilding):
            raise ValueError(f"Card '{card.name}' is not an UrbanBuilding (got {type(card).__name__})")
        
        # Check if already added
        if any(building.name == card.name for building in self.urban_buildings):
            raise ValueError(f"Urban building '{card.name}' already exists on this board")
        
        self.urban_buildings.append(card)
        
        # Also add to legacy tracking for compatibility
        self.current_technologies[card.name] = {
            'card_object': card,
            'production': getattr(card, 'production', {})
        }

    def add_wonder(self, card):
        """Add a wonder to the player's board

        Args:
            card: Wonder card object
        """
        self.wonders.append(card)

    def set_leader(self, card):
        """Set the player's leader

        Args:
            card: Leader card object
        """
        self.leader = card

    def set_government(self, card):
        """Set the player's government

        Args:
            card: Government card object
        """
        self.government = card
        self.active_government = card  # Update alias

    def get_all_buildings(self):
        """Get all buildings (production + urban) owned by the player

        Returns:
            List: All building cards
        """
        return self.production_buildings + self.urban_buildings

    def get_building_by_name(self, name: str):
        """Get a building by name

        Args:
            name (str): Name of the building

        Returns:
            Card object or None if not found
        """
        all_buildings = self.get_all_buildings()
        for building in all_buildings:
            if building.name == name:
                return building
        return None

    def has_technology(self, tech_name: str) -> bool:
        """Check if player has a specific technology

        Args:
            tech_name (str): Name of the technology

        Returns:
            bool: True if player has the technology
        """
        return self.get_building_by_name(tech_name) is not None

    def get_available_civil_actions(self, player_id: int) -> List[Dict[str, Any]]:
        """Obtiene acciones civiles disponibles para un jugador específico

        Args:
            player_id (int): ID del jugador

        Returns:
            List[Dict]: Lista de acciones civiles disponibles
        """
        logging.debug(f"Obteniendo acciones civiles disponibles para el jugador {player_id}")
        if player_id not in self.player_boards:
            return []

        player_board = self.player_boards[player_id]
        available_actions = []

        # Check available civil actions
        civil_actions_left = player_board.get_civil_actions_available()
        if civil_actions_left <= 0:
            return available_actions  # No civil actions left

        # Action: Increase Population
        if player_board.can_increase_population():
            available_actions.append({
                'type': 'aumentar_poblacion',
                'cost': {'civil_actions': 1, 'military_actions': 0},
                'resource_cost': {'food': 3},  # Base cost, actual cost may vary
                'description': 'Aumentar población'
            })

        # Action: Assign Worker to Technologies
        if player_board.yellow_reserves['available_workers'] > 0:
            for tech_name, tech_data in self.urban_buildings.items() + player_board.production_buildings.items():
                material_cost = tech_data.build_cost

                # Check if player has enough materials
                if player_board.resources['material'] >= material_cost:
                    # Check if not at max workers for this technology
                    current_workers = player_board.yellow_reserves['technology_workers'].get(tech_name, 0)
                    MAX_WORKERS_PER_TECH = 2  # TODO: This should come from government

                    if current_workers < MAX_WORKERS_PER_TECH:
                        available_actions.append({
                            'type': 'asignar_trabajador',
                            'cost': {'civil_actions': 1, 'military_actions': 0},
                            'resource_cost': {'material': material_cost},
                            'parameters': {'tech_name': tech_name},
                            'description': f'Asignar trabajador a {tech_name} (costo: {material_cost} materiales)'
                        })

        # Action: Take Card (if visible cards available)
        if hasattr(self, 'visible_civil_cards') and self.visible_civil_cards:
            for i, card in enumerate(self.visible_civil_cards):
                available_actions.append({
                    'type': 'tomar_carta',
                    'cost': {'civil_actions': 1, 'military_actions': 0},
                    'resource_cost': {},  # Usually no resource cost for taking cards
                    'parameters': {'card_position': i},
                    'description': f'Tomar carta: {card.get("name", "Carta desconocida")}'
                })

        # Action: Research Technology (if player has science)
        if player_board.resources['science'] > 0:
            # This would need to check available technologies to research
            # For now, add a generic research action
            available_actions.append({
                'type': 'investigar_tecnologia',
                'cost': {'civil_actions': 1, 'military_actions': 0},
                'resource_cost': {'science': 1},  # Minimum cost
                'description': 'Investigar nueva tecnología'
            })

        return available_actions