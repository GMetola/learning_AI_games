from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import logging

@dataclass
class GameAction:
    """Representa una acción del juego estandarizada para bots"""
    action_type: str  # 'tomar_carta', 'construir_edificio', 'aumentar_población'
    parameters: Dict[str, Any]  # Parámetros específicos de la acción
    cost: Dict[str, int]  # Coste en acciones civiles/militares
    player_id: int  # ID del jugador que ejecuta la acción

    def __post_init__(self):
        """Inicializa costes por defecto si no se especifican"""
        if not self.cost:
            self.cost = {'civil_actions': 1, 'military_actions': 0}

class ActionValidator:
    """Valida acciones del juego según las reglas"""

    def __init__(self, game_state):
        """Inicializa validador con estado del juego

        Args:
            game_state: Estado actual del juego
        """
        self.game_state = game_state

    def validate_action(self, player_id: int, action: GameAction) -> tuple:
        """Valida si una acción es legal para un jugador

        Args:
            player_id (int): ID del jugador
            action (GameAction): Acción a validar

        Returns:
            tuple: (is_valid: bool, error_message: str)
        """
        player = self.game_state.players[player_id - 1]
        player_board = player.board

        # VALIDACIÓN GENERAL: Turno del jugador
        current_player_index = self.game_state.current_turn
        if player_id - 1 != current_player_index:
            return False, "No es el turno de este jugador"        # VALIDACIÓN ACCIONES CIVILES Y MILITARES
        if action.cost.get('civil_actions', 0) > 0:
            # Use the modular action manager to check civil actions
            civil_actions_needed = action.cost.get('civil_actions', 0)
            if not player_board.action_manager.can_perform_civil_action(player_board.card_manager, civil_actions_needed):
                available = player_board.get_civil_actions_available()
                return False, f"No quedan acciones civiles suficientes (necesita {civil_actions_needed}, disponibles {available})"

        if action.cost.get('military_actions', 0) > 0:
            # Use the modular action manager to check military actions
            military_actions_needed = action.cost.get('military_actions', 0)
            if not player_board.action_manager.can_perform_military_action(player_board.card_manager, military_actions_needed):
                available = player_board.get_military_actions_available()
                return False, f"No quedan acciones militares suficientes (necesita {military_actions_needed}, disponibles {available})"

        # VALIDACIÓN ESPECÍFICA POR TIPO
        if action.action_type == 'tomar_carta':
            return self._validate_take_card(player_board, action)
        elif action.action_type == 'aumentar_población':
            return self._validate_increase_population(player_board, action)
        elif action.action_type == 'construir_edificio':
            return self._validate_build_building(player_board, action)
        elif action.action_type == 'asignar_trabajador':
            return self._validate_assign_worker(player_board, action)
        elif action.action_type == 'research_technology':
            return self._validate_research_technology(player_board, action)
        elif action.action_type == 'terminar_turno':
            return True, ""  # Siempre se puede terminar turno
        else:
            return False, f"Tipo de acción desconocido: {action.action_type}"

    def _validate_take_card(self, player_board, action: GameAction) -> tuple:
        """Valida tomar carta civil"""
        card_position = action.parameters.get('card_position')

        if card_position is None or card_position < 0 or card_position >= 13:
            return False, "Posición de carta inválida"

        if card_position >= len(self.game_state.board.visible_civil_cards):
            return False, "Posición de carta fuera de rango"

        # Verificar si la carta existe en esa posición
        if not self.game_state.board.visible_civil_cards[card_position]:
            return False, "No hay carta en esa posición"

        return True, ""

    def _validate_increase_population(self, player_board, action: GameAction) -> tuple:
        """Valida aumento de población"""
        if not player_board.can_increase_population():
            return False, "No se puede aumentar población: recursos insuficientes o sin fichas disponibles"

        return True, ""

    def _validate_build_building(self, player_board, action: GameAction) -> tuple:
        """Valida construcción de edificio"""
        card_name = action.parameters.get('card_name')

        if not card_name:
            return False, "Nombre de carta requerido para construir"        # Verificar si el jugador tiene la carta en mano (para construir)
        if not player_board.card_manager.has_card_in_hand(card_name):
            return False, f"Jugador no tiene la carta en mano: {card_name}"

        return True, ""

    def _validate_assign_worker(self, player_board, action: GameAction) -> tuple:
        """Valida asignación de trabajador"""
        tech_name = action.parameters.get('tech_name')

        if not tech_name:
            return False, "Nombre de tecnología requerido"

        if player_board.yellow_reserves['available_workers'] <= 0:
            return False, "No hay trabajadores disponibles"

        if not player_board.has_technology(tech_name):
            return False, f"Tecnología no disponible: {tech_name}"

        # Check if player has enough materials to assign worker
        # Only production buildings and some urban buildings need material cost for workers
        building = player_board.card_manager.get_building_by_name(tech_name)
        if building and hasattr(building, 'build_cost'):
            material_cost = building.build_cost
            if player_board.resources['material'] < material_cost:
                return False, f"Materiales insuficientes para asignar trabajador a {tech_name}: necesitas {material_cost}, tienes {player_board.resources['material']}"

        return True, ""

    def _validate_research_technology(self, player_board, action: GameAction) -> tuple:
        """Valida investigación de nueva tecnología"""
        card_name = action.parameters.get('card_name')
        science_cost = action.parameters.get('science_cost', 0)

        if not card_name:
            return False, "Nombre de carta requerido para investigar"

        if player_board.resources['science'] < science_cost:
            return False, f"Ciencia insuficiente: necesitas {science_cost}, tienes {player_board.resources['science']}"        # Verificar si ya tiene esta tecnología (desarrollada o en mano)
        if player_board.card_manager.has_card_anywhere(card_name):
            return False, f"Ya posee la tecnología: {card_name}"

        return True, ""

    def get_legal_actions(self, player_id: int) -> List[GameAction]:
        """Obtiene todas las acciones legales disponibles para un jugador

        Args:
            player_id (int): ID del jugador

        Returns:
            List[GameAction]: Lista de acciones legales
        """
        player = self.game_state.players[player_id - 1]
        player_board = player.board
        legal_actions = []        # Verificar acciones civiles disponibles (using modular action manager)
        available_civil_actions = player_board.get_civil_actions_available()

        # Verificar acciones militares disponibles (using modular action manager)
        available_military_actions = player_board.get_military_actions_available()

        # ACCIONES TOMAR CARTA (requiere acción civil)
        if available_civil_actions > 0:
            for i, card in enumerate(self.game_state.board.visible_civil_cards):
                if card:
                    action = GameAction(
                        action_type='tomar_carta',
                        parameters={'card_position': i},
                        cost={'civil_actions': 1},
                        player_id=player_id
                    )
                    if self.validate_action(player_id, action)[0]:
                        legal_actions.append(action)

        # ACCIÓN AUMENTAR POBLACIÓN (requiere acción civil)
        if available_civil_actions > 0 and player_board.can_increase_population():
            action = GameAction(
                action_type='aumentar_población',
                parameters={},
                cost={'civil_actions': 1},
                player_id=player_id
            )
            legal_actions.append(action)        # ACCIONES ASIGNAR TRABAJADOR (requiere acción civil)
        # Get all buildings that can have workers assigned
        all_buildings = player_board.card_manager.get_all_buildings()
        for building in all_buildings:
            if player_board.yellow_reserves['available_workers'] > 0:
                action = GameAction(
                    action_type='asignar_trabajador',
                    parameters={'tech_name': building.name},
                    cost={'civil_actions': 1},
                    player_id=player_id
                )
                legal_actions.append(action)

        # ACCIONES CONSTRUIR EDIFICIO (requiere acción civil)        if available_civil_actions > 0:
            # Buildings to construct come from hand cards or available cards
            hand_cards = player_board.card_manager.get_hand_cards()
            for card in hand_cards:
                # Only buildings can be constructed
                if hasattr(card, 'build_cost'):
                    action = GameAction(
                        action_type='construir_edificio',
                        parameters={'card_name': card.name},
                        cost={'civil_actions': 1},
                        player_id=player_id
                    )
                    legal_actions.append(action)

        # ACCIÓN TERMINAR TURNO (siempre disponible)
        action = GameAction(
            action_type='terminar_turno',
            parameters={},
            cost={'civil_actions': 0},
            player_id=player_id
        )
        legal_actions.append(action)

        return legal_actions

class ActionExecutor:
    """Ejecuta acciones validadas en el juego"""

    def __init__(self, game_state, bots: List = None):
        """Inicializa ejecutor con estado del juego

        Args:
            game_state: Estado del juego donde ejecutar acciones
            bots (List): Lista de bots para actualizar contadores de acciones
        """
        self.game_state = game_state
        self.validator = ActionValidator(game_state)
        self.bots = bots or []

    def execute_action(self, action: GameAction, bot = None) -> Dict[str, Any]:
        """Ejecuta una acción validada

        Args:
            action (GameAction): Acción a ejecutar
            bot: Bot que ejecuta la acción (opcional)

        Returns:
            Dict: Resultado de la ejecución
        """
        # Validar acción antes de ejecutar
        is_valid, error_msg = self.validator.validate_action(action.player_id, action)

        if not is_valid:
            return {
                'success': False,
                'error': error_msg,
                'action': action
            }

        # Obtener jugador
        player = self.game_state.players[action.player_id - 1]

        # CONSUMIR ACCIONES DEL BOT Y TABLERO
        civil_cost = action.cost.get('civil_actions', 0)
        military_cost = action.cost.get('military_actions', 0)

        if civil_cost > 0:
            bot.consume_civil_action(civil_cost)
        if military_cost > 0:
            bot.consume_military_action(military_cost)

        # ACTUALIZAR CONTADORES EN EL TABLERO DEL JUGADOR
        player_board = player.board
        if civil_cost > 0:
            current_used = getattr(player_board, 'used_civil_actions', 0)
            player_board.used_civil_actions = current_used + civil_cost
        if military_cost > 0:
            current_used = getattr(player_board, 'used_military_actions', 0)
            player_board.used_military_actions = current_used + military_cost

        # EJECUCIÓN POR TIPO
        result = None
        if action.action_type == 'tomar_carta':
            result = self._execute_take_card(action)
        elif action.action_type == 'aumentar_población':
            result = self._execute_increase_population(action)
        elif action.action_type == 'asignar_trabajador':
            result = self._execute_assign_worker(action)
        elif action.action_type == 'construir_edificio':
            result = self._execute_build_building(action)
        elif action.action_type == 'research_technology':
            result = self._execute_research_technology(action)
        elif action.action_type == 'terminar_turno':
            result = self._execute_end_turn(action)
        else:
            result = {'success': False, 'error': f'Tipo de acción no implementado: {action.action_type}'}

        # Log detailed player state after action
        self._log_player_state_debug(action.player_id, action.action_type, result.get('success', False))

        return result

    def _execute_take_card(self, action: GameAction) -> Dict[str, Any]:
        """Ejecuta tomar carta civil"""
        card_position = action.parameters['card_position']
        player = self.game_state.players[action.player_id - 1]

        # Tomar carta del tablero
        card = self.game_state.board.visible_civil_cards[card_position]
        self.game_state.board.visible_civil_cards[card_position] = None        # Añadir a tecnologías del jugador using the new card manager
        try:
            if card.card_type in ['Farm', 'Mine']:
                player.board.card_manager.add_production_building(card)
            elif card.card_type in ['Temple', 'Library']:
                player.board.card_manager.add_urban_building(card)
            else:
                # Add to hand for other types of cards
                player.board.card_manager.add_card_to_hand(card)
        except ValueError as e:
            logging.warning(f"Failed to add card {card.name} to player {action.player_id}: {e}")
            # Add to hand as fallback
            player.board.card_manager.add_card_to_hand(card)

        logging.info(f"Jugador {action.player_id} tomó carta: {card.name}")

        return {
            'success': True,
            'card_taken': card.name,
            'player_id': action.player_id
        }

    def _execute_increase_population(self, action: GameAction) -> Dict[str, Any]:
        """Ejecuta aumento de población"""
        player = self.game_state.players[action.player_id - 1]
        cost = player.board.get_population_cost()

        success = player.board.increase_population(cost)

        if success:
            logging.info(f"Jugador {action.player_id} aumentó población por {cost} comida")

        return {
            'success': success,
            'food_cost': cost,
            'player_id': action.player_id
        }

    def _execute_assign_worker(self, action: GameAction) -> Dict[str, Any]:
        """Ejecuta asignación de trabajador"""
        player = self.game_state.players[action.player_id - 1]
        tech_name = action.parameters['tech_name']        # Get the Card object from the card manager
        building = player.board.card_manager.get_building_by_name(tech_name)
        if building:
            success = player.board.assign_worker_to_building(building)
        else:
            success = False

        if success:
            logging.info(f"Jugador {action.player_id} asignó trabajador a {tech_name}")

        return {
            'success': success,
            'tech_name': tech_name,
            'player_id': action.player_id
        }

    def _execute_build_building(self, action: GameAction) -> Dict[str, Any]:
        """Ejecuta construcción de edificio"""
        player = self.game_state.players[action.player_id - 1]
        card_name = action.parameters['card_name']
        building_type = action.parameters.get('building_type', 'building')        # Implement proper building construction logic with modular system
        # First check if the card is in hand
        hand_cards = player.board.card_manager.get_hand_cards()
        building_card = None

        for card in hand_cards:
            if card.name == card_name:
                building_card = card
                break

        if building_card:
            # Remove from hand and add to appropriate building collection
            player.board.card_manager.remove_card_from_hand(building_card)

            try:
                if hasattr(building_card, 'card_type'):
                    if building_card.card_type in ['Farm', 'Mine']:
                        player.board.card_manager.add_production_building(building_card)
                    elif building_card.card_type in ['Temple', 'Library']:
                        player.board.card_manager.add_urban_building(building_card)
                    else:
                        # For other building types, add back to hand for now
                        player.board.card_manager.add_card_to_hand(building_card)

                logging.info(f"Jugador {action.player_id} construyó edificio: {card_name}")

                return {
                    'success': True,
                    'card_name': card_name,
                    'building_type': getattr(building_card, 'building_type', 'building'),
                    'player_id': action.player_id
                }
            except ValueError as e:
                # If failed to add, put back in hand
                player.board.card_manager.add_card_to_hand(building_card)
                logging.error(f"Failed to build {card_name}: {e}")
                return {
                    'success': False,
                    'error': str(e),
                    'player_id': action.player_id
                }
            else:
                # Technology exists but no building card - this shouldn't happen with new system
                logging.warning(f"Technology {card_name} exists but no building card found")
                return {
                    'success': False,
                    'error': f"Tecnología {card_name} no tiene edificio asociado",
                    'player_id': action.player_id
                }
        else:
            return {
                'success': False,
                'error': f"No posee la tecnología: {card_name}",
                'player_id': action.player_id
            }

    def _execute_research_technology(self, action: GameAction) -> Dict[str, Any]:
        """Ejecuta investigación de tecnología"""
        player = self.game_state.players[action.player_id - 1]
        card_name = action.parameters['card_name']
        science_cost = action.parameters.get('science_cost', 0)

        # Pagar coste de ciencia
        player.board.resources['science'] -= science_cost        # Agregar nueva tecnología to hand for now
        # In the future, this should create the appropriate card object and add it to hand
        # For now, we'll add it as a basic card to hand
        try:
            from .card_loader import CardLoader
            loader = CardLoader()
            card = loader.get_card_by_name(card_name)
            if card:
                player.board.card_manager.add_card_to_hand(card)
            else:
                logging.warning(f"Card {card_name} not found in loader, research action may have issues")
        except Exception as e:
            logging.warning(f"Failed to load researched card {card_name}: {e}")

        # REGISTRAR MEJORA DEL TURNO
        player.board.add_technology_researched(card_name)

        logging.info(f"Jugador {action.player_id} investigó tecnología: {card_name}")

        return {
            'success': True,
            'card_name': card_name,
            'science_cost': science_cost,
            'player_id': action.player_id
        }

    def _execute_take_card(self, action: GameAction) -> Dict[str, Any]:
        """Ejecuta tomar carta civil"""
        card_position = action.parameters['card_position']
        player = self.game_state.players[action.player_id - 1]

        # Tomar carta del tablero
        card = self.game_state.board.visible_civil_cards[card_position]
        self.game_state.board.visible_civil_cards[card_position] = None

        # Añadir a tecnologías del jugador using the new card manager
        if card:
            try:
                if card.card_type in ['Farm', 'Mine']:
                    player.board.card_manager.add_production_building(card, built=False)
                elif card.card_type in ['Temple', 'Library']:
                    player.board.card_manager.add_urban_building(card, built=False)
                else:
                    # Add to hand for other types of cards
                    player.board.card_manager.add_card_to_hand(card)
            except ValueError as e:
                logging.warning(f"Failed to add card {card.name} to player {action.player_id}: {e}")
                # Add to hand as fallback
                player.board.card_manager.add_card_to_hand(card)

            # REGISTRAR COMO TECNOLOGÍA INVESTIGADA
            player.board.add_technology_researched(card.name)

        logging.info(f"Jugador {action.player_id} tomó carta: {card.name}")

        return {
            'success': True,
            'card_taken': card.name,
            'player_id': action.player_id
        }

    def _execute_end_turn(self, action: GameAction) -> Dict[str, Any]:
        """Ejecuta terminar turno"""
        player = self.game_state.players[action.player_id - 1]

        # Resetear contadores de acciones para el próximo turno
        player.board.used_civil_actions = 0
        player.board.used_military_actions = 0

        logging.info(f"Jugador {action.player_id} terminó su turno")

        # Avanza al siguiente turno en el game state
        self.game_state.next_turn()

        return {
            'success': True,
            'turn_ended': True,
            'player_id': action.player_id,
            'next_player': self.game_state.get_current_player()
        }

    def execute_multiple_actions(self, actions: List[GameAction], bot=None) -> List[Dict[str, Any]]:
        """Ejecuta múltiples acciones en secuencia

        Args:
            actions (List[GameAction]): Lista de acciones a ejecutar
            bot: Bot que ejecuta las acciones (opcional)

        Returns:
            List[Dict]: Lista de resultados de cada acción
        """
        results = []

        for action in actions:
            result = self.execute_action(action, bot)
            results.append(result)

            # Si una acción falla, detener ejecución
            if not result.get('success', False):
                break

        return results

    def _log_player_state_debug(self, player_id: int, action_type: str, success: bool):
        """Log detailed player state for debugging after an action

        Args:
            player_id (int): ID of the player
            action_type (str): Type of action that was executed
            success (bool): Whether the action was successful
        """
        try:
            player = self.game_state.players[player_id - 1]
            player_board = player.board

            # Get current resources
            resources = player_board.resources.copy()

            # Calculate current production
            production = {'food': 0, 'material': 0, 'science': 0, 'culture': 0, 'happy': 0, 'strength': 0}

            # Production from buildings with workers
            for tech_name, workers in player_board.yellow_reserves['technology_workers'].items():
                building = player_board.get_building_by_name(tech_name)
                if building and hasattr(building, 'production') and workers > 0:
                    for resource, amount_per_worker in building.production.items():
                        production[resource] += workers * amount_per_worker

            # Cards in hand
            hand_count = len(player_board.hand_cards)
            hand_names = [card.name for card in player_board.hand_cards]

            # Technologies developed (buildings)
            buildings_info = []
            for building in player_board.get_all_buildings():
                workers = player_board.yellow_reserves['technology_workers'].get(building.name, 0)
                buildings_info.append(f"{building.name}({workers}w)")

            # Wonders
            wonders_info = []
            for wonder in player_board.wonders:
                step_info = wonder.get_step_info()
                wonders_info.append(f"{wonder.name}({step_info['current_step']}/{step_info['num_steps']})")

            # Actions available
            civil_available = player_board.get_civil_actions_available()
            military_available = player_board.get_military_actions_available()

            # Format debug log
            debug_msg = f"""
========== PLAYER {player_id} STATE AFTER {action_type.upper()} ({'SUCCESS' if success else 'FAILED'}) ==========
RESOURCES: Food={resources['food']}, Materials={resources['material']}, Science={resources['science']}, Culture={resources['culture']}, Happy={resources['happy']}, Strength={resources['strength']}
PRODUCTION: Food={production['food']}, Materials={production['material']}, Science={production['science']}, Culture={production['culture']}, Happy={production['happy']}, Strength={production['strength']}
HAND CARDS: {hand_count} cards {hand_names if hand_names else []}
BUILDINGS: {', '.join(buildings_info) if buildings_info else 'None'}
WONDERS: {', '.join(wonders_info) if wonders_info else 'None'}
GOVERNMENT: {player_board.government.name} (Civil:{civil_available}, Military:{military_available})
WORKERS: Available={player_board.yellow_reserves['available_workers']}
====================================================================================================="""

            logging.info(debug_msg)

        except Exception as e:
            logging.warning(f"Failed to log player state debug: {e}")

# Factory para crear acciones comunes
class ActionFactory:
    """Factory para crear acciones del juego de forma conveniente"""

    @staticmethod
    def create_take_card_action(player_id: int, card_position: int) -> GameAction:
        """Crea acción para tomar carta civil

        Args:
            player_id (int): ID del jugador
            card_position (int): Posición de la carta en el tablero

        Returns:
            GameAction: Acción de tomar carta
        """
        return GameAction(
            action_type='tomar_carta',
            parameters={'card_position': card_position},
            cost={'civil_actions': 1, 'military_actions': 0},
            player_id=player_id
        )

    @staticmethod
    def create_increase_population_action(player_id: int) -> GameAction:
        """Crea acción para aumentar población

        Args:
            player_id (int): ID del jugador

        Returns:
            GameAction: Acción de aumentar población
        """
        return GameAction(
            action_type='aumentar_población',
            parameters={},
            cost={'civil_actions': 1, 'military_actions': 0},
            player_id=player_id
        )

    @staticmethod
    def create_assign_worker_action(player_id: int, tech_name: str) -> GameAction:
        """Crea acción para asignar trabajador

        Args:
            player_id (int): ID del jugador
            tech_name (str): Nombre de la tecnología

        Returns:
            GameAction: Acción de asignar trabajador
        """
        return GameAction(
            action_type='asignar_trabajador',
            parameters={'tech_name': tech_name},
            cost={'civil_actions': 1, 'military_actions': 0},
            player_id=player_id
        )

    @staticmethod
    def create_assign_warrior_action(player_id: int, tech_name: str) -> GameAction:
        """Crea acción para asignar guerrero

        Args:
            player_id (int): ID del jugador
            tech_name (str): Nombre de la tecnología

        Returns:
            GameAction: Acción de asignar trabajador
        """
        return GameAction(
            action_type='asignar_guerrero',
            parameters={'tech_name': tech_name},
            cost={'civil_actions': 0, 'military_actions': 1},
            player_id=player_id
        )

    @staticmethod
    def create_build_building_action(player_id: int, card_name: str, building_type: str = 'building') -> GameAction:
        """Crea acción para construir edificio

        Args:
            player_id (int): ID del jugador
            card_name (str): Nombre de la carta/tecnología
            building_type (str): Tipo de construcción

        Returns:
            GameAction: Acción de construir edificio
        """
        return GameAction(
            action_type='construir_edificio',
            parameters={'card_name': card_name, 'building_type': building_type},
            cost={'civil_actions': 1, 'military_actions': 0},
            player_id=player_id
        )

    @staticmethod
    def create_end_turn_action(player_id: int) -> GameAction:
        """Crea acción para terminar turno

        Args:
            player_id (int): ID del jugador

        Returns:
            GameAction: Acción de terminar turno
        """
        return GameAction(
            action_type='terminar_turno',
            parameters={},
            cost={'civil_actions': 0, 'military_actions': 0},
            player_id=player_id
        )

# Utilidades para manejo de acciones
class ActionUtils:
    """Utilidades para trabajar con acciones del juego"""

    @staticmethod
    def filter_actions_by_type(actions: List[GameAction], action_type: str) -> List[GameAction]:
        """Filtra acciones por tipo

        Args:
            actions (List[GameAction]): Lista de acciones
            action_type (str): Tipo de acción a filtrar

        Returns:
            List[GameAction]: Acciones filtradas
        """
        return [action for action in actions if action.action_type == action_type]

    @staticmethod
    def calculate_total_cost(actions: List[GameAction]) -> Dict[str, int]:
        """Calcula el coste total de una lista de acciones

        Args:
            actions (List[GameAction]): Lista de acciones

        Returns:
            Dict[str, int]: Coste total por tipo de acción
        """
        total_cost = {'civil_actions': 0, 'military_actions': 0}

        for action in actions:
            for cost_type, cost_value in action.cost.items():
                total_cost[cost_type] = total_cost.get(cost_type, 0) + cost_value

        return total_cost

    @staticmethod
    def validate_action_sequence(actions: List[GameAction], game_state) -> Tuple[bool, str]:
        """Valida una secuencia de acciones

        Args:
            actions (List[GameAction]): Secuencia de acciones
            game_state: Estado del juego

        Returns:
            Tuple[bool, str]: (es_válida, mensaje_error)
        """
        validator = ActionValidator(game_state)

        for i, action in enumerate(actions):
            is_valid, error_msg = validator.validate_action(action.player_id, action)
            if not is_valid:
                return False, f"Acción {i+1} inválida: {error_msg}"

        return True, ""