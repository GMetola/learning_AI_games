import random
import logging
from typing import Dict, List
from bots.base_bot import BaseBot
from game.actions import GameAction

class AlgorithmicBot(BaseBot):
    def __init__(self, bot_id: str, name: str, difficulty: str = "medium"):
        """Bot algorítmico que sigue estrategias predefinidas

        Args:
            bot_id (str): ID único del bot
            name (str): Nombre del bot
            difficulty (str): Nivel de dificultad (easy, medium, hard)
        """
        super().__init__(bot_id, name, difficulty)
        self.strategy_weights = self._initialize_strategy_weights()
        self.player_id = None  # Will be set when the bot joins a game

    def set_player_id(self, player_id: int):
        """Set the player ID for this bot instance"""
        self.player_id = player_id

    def _initialize_strategy_weights(self) -> Dict[str, float]:
        """Inicializa pesos de estrategia según dificultad"""
        if self.difficulty == "easy":
            return {
                'population_priority': 0.3,
                'production_priority': 0.4,
                'military_priority': 0.1,
                'culture_priority': 0.2,
                'randomness': 0.3
            }
        elif self.difficulty == "medium":
            return {
                'population_priority': 0.25,
                'production_priority': 0.35,
                'military_priority': 0.2,
                'culture_priority': 0.2,
                'randomness': 0.15
            }
        else:  # hard
            return {
                'population_priority': 0.2,
                'production_priority': 0.3,
                'military_priority': 0.25,
                'culture_priority': 0.25,
                'randomness': 0.05
            }

    def make_move(self, game_state, available_actions: List) -> GameAction:
        """Selecciona un movimiento usando estrategias algorítmicas

        Args:
            game_state: Estado actual del juego (GameState object)
            available_actions: Lista de GameAction objects disponibles

        Returns:
            action (GameAction)
        """
        if not available_actions:
            logging.warning(f"Bot {self.name}: Sin acciones disponibles")
            return {'type': 'end_turn'}
        logging.info(f"Bot {self.name} analizando acciones disponibles: {len(available_actions)} acciones\n"
                     f"Tiene estos recursos: {game_state.players[self.player_id - 1].board.resource_manager.get_resource_summary()}")

        # Analyze player capabilities using new methods
        ordered_actions = self._prioritize_actions_based_on_capabilities(game_state)

        for action in ordered_actions:
            logging.info(f"Puntos: {action.estimated_points_gotten:.2f} -  Acción: {action.action_type} - Parámetros: {action.parameters}")

        return ordered_actions[0]

    def _evaluate_game_action(self, action: GameAction, game_state) -> float:
        """Evalúa una GameAction específica
        Un jugador debe llamar a _evaluate_game_action_with_capabilities para tener sus capacidades en cuenta

        Returns:
            float: Puntuación de la acción (0 a 1)
        """
        # Get current era for era-based strategy
        current_era = self._get_current_era(game_state)

        """
        Era-based Strategy Implementation:
        - Era A: Get a good leader and a good wonder
        - Era I: Focus on PRODUCTION. Balanced production in order: science, material, food.
                 Bonus for extra civil and military actions
        - Era II: BALANCING what couldn't be balanced in era I.
                  Special attention to population growth, happiness and food production.
                  Then production of science, material. Then civil and military actions
        - Era III: Focus on culture HARD, get good military cards, get good wonders.
        - All eras: Try to be first or second in military strength.
        """
        action_type = action.action_type
        score = 0.0

        # Get player state
        if self.player_id and self.player_id <= len(game_state.players):
            player = game_state.players[self.player_id - 1]
            player_board = player.board
        else:
            # Fallback: try to find player by name
            player = None
            for p in game_state.players:
                if p.name == self.name:
                    player = p
                    player_board = p.board
                    break
            if not player:
                return 0.0

        # Apply era-based modifiers to base scoring
        era_modifier = self._get_era_strategy_modifier(action_type, current_era, player_board)

        # EVALUACIÓN POR TIPO DE ACCIÓN (with era considerations)
        if action_type == 'aumentar_poblacion':
            score += self._evaluate_population_action(player_board) * era_modifier
        elif action_type == 'tomar_carta':
            score += self._evaluate_take_card_action(action, game_state) * era_modifier
        elif action_type == 'asignar_trabajador':
            score += self._evaluate_assign_worker_action(action, player_board) * era_modifier
        elif action_type == 'construir_edificio':
            score += self._evaluate_build_action(action, player_board) * era_modifier
        elif action_type == 'terminar_turno':
            score += self._evaluate_end_turn_action(player_board) * era_modifier

        return score

    def _get_current_era(self, game_state) -> str:
        """Get current game era/age

        Args:
            game_state: Game state object

        Returns:
            str: Current era ('A', 'I', 'II', 'III')
        """
        if hasattr(game_state, 'board') and hasattr(game_state.board, 'current_age'):
            return game_state.board.current_age
        logging.warning("Game state does not have current age, defaulting to 'A'")
        return 'A'

    def _get_era_strategy_modifier(self, action_type: str, era: str, player_board) -> float:
        """Get era-based strategy modifier for action scoring

        Args:
            action_type (str): Type of action
            era (str): Current era
            player_board: Player's board

        Returns:
            float: Modifier multiplier (typically 0.5 to 2.0)
        """
        base_modifier = 1.0

        if era == 'A':
            # Era A: Focus on leaders and wonders
            if action_type == 'tomar_carta':
                # Higher priority for leaders and wonders
                base_modifier = 1.3
            elif action_type == 'construir_edificio':
                # Basic buildings are important
                base_modifier = 1.2

        elif era == 'I':
            # Era I: Focus on PRODUCTION (science > material > food)
            if action_type == 'asignar_trabajador':
                # High priority for worker assignments to production
                base_modifier = 1.5
            elif action_type == 'construir_edificio':
                # Production buildings are crucial
                base_modifier = 1.4
            elif action_type == 'aumentar_poblacion':
                # Population growth is important
                base_modifier = 1.3

        elif era == 'II':
            # Era II: BALANCING - population growth, happiness, food production
            if action_type == 'aumentar_poblacion':
                # Very high priority for population growth
                base_modifier = 1.6
            elif action_type == 'construir_edificio':
                # Focus on happiness and food buildings
                base_modifier = 1.3
            elif action_type == 'asignar_trabajador':
                # Balance production
                base_modifier = 1.2

        elif era == 'III':
            # Era III: Focus on culture HARD, military cards, wonders
            if action_type == 'tomar_carta':
                # High priority for culture and military cards
                base_modifier = 1.4
            elif action_type == 'construir_edificio':
                # Wonders and culture buildings
                base_modifier = 1.3

        # Military strength is always important (all eras)
        if action_type in ['tomar_carta', 'construir_edificio']:
            # Boost military-related actions slightly
            # GABRIEL: revisa esto
            base_modifier *= 1.1

        return base_modifier

    def _evaluate_population_action(self, player_board) -> float:
        """Evalúa acción de aumentar población"""
        # Higher priority if we have few workers
        available_workers = player_board.yellow_reserves['available_workers']
        if available_workers < 3:
            return self.strategy_weights['population_priority'] * 100
        elif available_workers < 6:
            return self.strategy_weights['population_priority'] * 50
        else:
            return self.strategy_weights['population_priority'] * 10

    def _evaluate_take_card_action(self, action, game_state) -> float:
        """Evalúa acción de tomar carta"""
        card_position = action.parameters.get('card_position', 0)

        # Check if card exists
        if (card_position < len(game_state.board.visible_civil_cards) and
            game_state.board.visible_civil_cards[card_position]):

            card = game_state.board.visible_civil_cards[card_position]

            # Evaluate based on card type and production
            score = self.strategy_weights['production_priority'] * 30

            # Bonus for production cards
            if hasattr(card, 'production') and card.production:
                if 'food' in card.production:
                    score += 20
                if 'material' in card.production:
                    score += 15
                if 'science' in card.production:
                    score += 25
                if 'culture' in card.production:
                    score += self.strategy_weights['culture_priority'] * 30

            return score

        return 0

    def _evaluate_assign_worker_action(self, action, player_board) -> float:
        """Evalúa asignación de trabajador"""
        tech_name = action.parameters.get('tech_name', '')

        # Get building info
        if player_board.has_technology(tech_name):
            building = player_board.card_manager.get_building_by_name(tech_name)

            # Check current worker assignment
            current_workers = player_board.yellow_reserves['technology_workers'].get(tech_name, 0)

            # Prioritize assigning workers to unassigned technologies
            if current_workers == 0:
                return self.strategy_weights['production_priority'] * 40
            elif current_workers < 2:
                return self.strategy_weights['production_priority'] * 20
            else:
                return self.strategy_weights['production_priority'] * 5

        return 0

    def _evaluate_build_action(self, action, player_board) -> float:
        """Evalúa construcción de edificio"""
        card_name = action.parameters.get('card_name', '')

        # Basic building priority
        return self.strategy_weights['production_priority'] * 25

    def _evaluate_end_turn_action(self, player_board) -> float:
        """Evalúa terminar turno"""
        # Lower priority - only if no better options
        return 1.0

    def _evaluate_action(self, action: Dict, game_state: Dict) -> float:
        """Evalúa una acción específica (formato legacy)"""
        action_type = action.get('type', '')
        score = 0.0

        # EVALUACIONES BÁSICAS POR TIPO
        if action_type == 'increase_population':
            score += self.strategy_weights['population_priority'] * 50
        elif action_type == 'take_card':
            score += self.strategy_weights['production_priority'] * 40
        elif action_type == 'assign_worker':
            score += self.strategy_weights['production_priority'] * 30
        elif action_type == 'end_turn':
            score += 1.0
        else:
            # Unknown action type
            score += 10.0

        return score

    def evaluate_position(self, game_state: Dict) -> float:
        """Evalúa la posición actual del juego

        Args:
            game_state (Dict): Estado del juego

        Returns:
            float: Puntuación de la posición (-1 a 1)
        """
        try:
            # Find our player in the game state
            our_player = None
            if hasattr(game_state, 'players'):
                for player in game_state.players:
                    if player.name == self.name:
                        our_player = player
                        break

            if not our_player:
                return 0.0

            player_board = our_player.board
            score = 0.0

            # EVALUACIÓN DE RECURSOS
            resources = player_board.resources
            score += resources.get('food', 0) * 0.1
            score += resources.get('material', 0) * 0.1
            score += resources.get('science', 0) * 0.15
            score += resources.get('culture', 0) * 0.2

            # EVALUACIÓN DE POBLACIÓN
            available_workers = player_board.yellow_reserves['available_workers']
            score += available_workers * 5

            # EVALUACIÓN DE TECNOLOGÍAS
            tech_count = len(player_board.card_manager.get_all_buildings())
            # Also count other card types
            tech_count += len(player_board.card_manager.get_wonders())
            if player_board.card_manager.get_leader():
                tech_count += 1
            if player_board.card_manager.get_government():
                tech_count += 1
            score += tech_count * 10

            # Normalizar a rango [-1, 1]
            # Asumiendo que una puntuación buena está alrededor de 100
            normalized_score = min(1.0, max(-1.0, score / 100.0))

            return normalized_score

        except Exception as e:
            logging.warning(f"Error evaluating position for bot {self.name}: {e}")
            return 0.0

    def _get_player_from_game_state(self, game_state):
        """Utility method to find our player in the game state"""
        if hasattr(game_state, 'players'):
            for player in game_state.players:
                if player.name == self.name:
                    return player
        return None

    def _evaluate_production_action(self, action: Dict, game_state: Dict) -> float:
        """Evalúa acciones de producción"""
        base_score = self.strategy_weights['production_focus'] * 10

        # Prioriza granjas al inicio del juego
        current_turn = game_state.get('turn', 0)
        if action.get('type') == 'build_farm' and current_turn < 5:
            base_score *= 1.5

        return base_score

    def _evaluate_military_action(self, action: Dict, game_state: Dict) -> float:
        """Evalúa acciones militares"""
        return self.strategy_weights['military_focus'] * 8

    def _evaluate_culture_action(self, action: Dict, game_state: Dict) -> float:
        """Evalúa acciones culturales"""
        return self.strategy_weights['culture_focus'] * 6

    def _evaluate_wonder_action(self, action: Dict, game_state: Dict) -> float:
        """Evalúa construcción de maravillas"""
        return self.strategy_weights['wonder_focus'] * 12

    def evaluate_position(self, game_state: Dict) -> float:
        """Evalúa la posición actual del bot en el juego"""
        player_resources = game_state.get('current_player_resources', {})
        my_score = player_resources.get('culture', 0)

        # Evaluación simple basada en puntuación
        if my_score > 50:
            return 0.8
        elif my_score > 25:
            return 0.5
        else:
            return 0.2

    def _get_player_capabilities(self, game_state) -> dict:
        """Get what the player can do

        Args:
            game_state: Current game state

        Returns:
            dict: Analysis of player capabilities
        """
        player = game_state.players[self.player_id - 1]
        player_board = player.board

        # Get comprehensive action summary
        action_summary = player_board.get_available_actions_summary()

        # Check specific action capabilities
        population_check = player_board.can_increase_population_with_details()

        # Check worker assignment for production buildings
        available_production_jobs = {}
        for building in player_board.card_manager.get_production_buildings():
            available_production_jobs[building.name] = player_board.can_build_building(building)

        # Check worker assignment to urban buildings
        available_urban_jobs = {}
        for building in player_board.card_manager.get_urban_buildings():
            available_urban_jobs[building.name] = player_board.can_build_building(building)

        # Check research possibilities for cards in hand
        research_possibilities = {}
        hand_cards = player_board.card_manager.get_hand_cards()
        for card in hand_cards:
            # Estimate science cost (in a real game, this would come from card data)
            estimated_science_cost = getattr(card, 'science_cost', 1)
            research_possibilities[card.name] = player_board.can_research_technology(card.name, estimated_science_cost)

        # Check building possibilities for cards in hand
        building_possibilities = {}
        for card in hand_cards:
            if hasattr(card, 'build_cost'):  # Only buildings have build costs
                building_possibilities[card.name] = player_board.can_build_building(card.name)

        return {
            'action_summary': action_summary,
            'population_check': population_check,
            'available_production_jobs': available_production_jobs,
            'available_urban_jobs': available_urban_jobs,
            'research_possibilities': research_possibilities,
            'building_possibilities': building_possibilities
        }

    def _prioritize_actions_based_on_capabilities(self, game_state) -> List[str]:
        """Prioritize actions based on what the player can actually do

        Args:
            game_state: Current game state

        Returns:
            List[GameAction]: Ordered list of recommended action types
        """
        capabilities = self._get_player_capabilities(game_state)
        action_priorities = []

        # Population growth priority
        if capabilities['population_check']['can_increase']:
            action = GameAction(
                action_type='aumentar_poblacion',
                parameters={},
                number_of_actions_spent={'civil': 1, 'military': 0},
                player_id=self.player_id
            )
            action = self._evaluate_game_action_with_capabilities(action, game_state, capabilities)
            action_priorities.append(action)

        # Worker assignment priorities
        assignable_producers = [tech for tech, check in capabilities['available_production_jobs'].items() if check['can_build']]
        assignable_urbanite = [tech for tech, check in capabilities['available_urban_jobs'].items() if check['can_build']]
        assignable_workers = assignable_producers + assignable_urbanite
        if assignable_workers:
            # Prioritize production buildings
            for tech in assignable_workers:
                action = GameAction(
                    action_type='asignar_trabajador',
                    parameters={'tech_name': tech},
                    number_of_actions_spent={'civil': 1, 'military': 0},
                    player_id=self.player_id
                )
                action = self._evaluate_game_action_with_capabilities(action, game_state, capabilities)
                action_priorities.append(action)

        # Research priorities
        researchable_cards = [card for card, check in capabilities['research_possibilities'].items() if check['can_research']]
        if researchable_cards:
            for card in researchable_cards:
                action = GameAction(
                    action_type='desarrollar_tecnologia',
                    parameters={'card_name': card},
                    number_of_actions_spent={'civil': 1, 'military': 0},
                    player_id=self.player_id
                )
                action = self._evaluate_game_action_with_capabilities(action, game_state, capabilities)
                action_priorities.append(action)

        # Building priorities
        buildable_cards = [card for card, check in capabilities['building_possibilities'].items() if check['can_build']]
        if buildable_cards:
            for card in buildable_cards:
                action = GameAction(
                    action_type='construir_edificio',
                    parameters={'card_name': card},
                    number_of_actions_spent={'civil': 1, 'military': 0},
                    player_id=self.player_id
                )
                action = self._evaluate_game_action_with_capabilities(action, game_state, capabilities)
                action_priorities.append(action)

        # Sort by priority score (descending)
        action_priorities.sort(key=lambda x: x.estimated_points_gotten, reverse=True)

        return action_priorities

    def _evaluate_game_action_with_capabilities(self, action: GameAction, game_state, capabilities) -> float:
        """Evalúa una GameAction con conocimiento de las capacidades del jugador
        Args:
            action (GameAction): Acción a evaluar
            game_state: Estado actual del juego
            capabilities (dict): Análisis de capacidades del jugador
        Returns:
            action (GameAction): Acción evaluada con puntuación incluida

        """
        action_type = action.action_type
        score = 0.0

        # Base evaluation using existing method
        base_score = self._evaluate_game_action(action, game_state)
        score += base_score

        # Bonus scoring based on capability analysis
        if action_type == 'aumentar_poblacion':
            pop_check = capabilities['population_check']
            if pop_check['can_increase']:
                # Higher priority if we have excess food
                food_ratio = pop_check['current_food'] / max(pop_check['food_cost'], 1)
                if food_ratio > 2:
                    score += 0.3  # Bonus for having plenty of food
                score += 0.2  # Base bonus for viable population increase
            else:
                score -= 0.5  # Penalty for impossible action
        elif action_type == 'asignar_trabajador':
            tech_name = action.parameters.get('tech_name', '')
            if tech_name in capabilities['available_production_jobs']:
                worker_check = capabilities['available_production_jobs'][tech_name]
                if worker_check.get('can_build', False):
                    # Bonus for production buildings
                    if 'Farm' in tech_name or 'Mine' in tech_name:
                        score += 0.25
                    score += 0.15  # Base bonus for viable worker assignment
                else:
                    score -= 0.8  # Heavy penalty for impossible assignment
            elif tech_name in capabilities['available_urban_jobs']:
                worker_check = capabilities['available_urban_jobs'][tech_name]
                if worker_check.get('can_build', False):
                    # Bonus for production buildings
                    if 'Farm' in tech_name or 'Mine' in tech_name:
                        score += 0.25
                    score += 0.15  # Base bonus for viable worker assignment
                else:
                    score -= 0.8  # Heavy penalty for impossible assignment

        elif action_type == 'desarrollar_tecnologia':
            card_name = action.parameters.get('card_name', '')
            if card_name in capabilities['research_possibilities']:
                research_check = capabilities['research_possibilities'][card_name]
                if research_check['can_research']:
                    # Bonus based on science efficiency
                    if research_check['current_science'] > research_check.get('science_cost', 1) * 2:
                        score += 0.2  # Bonus for having plenty of science
                    score += 0.15  # Base bonus for viable research
                else:
                    score -= 0.7  # Penalty for impossible research

        elif action_type == 'construir_edificio':
            card_name = action.parameters.get('card_name', '')
            if card_name in capabilities['building_possibilities']:
                build_check = capabilities['building_possibilities'][card_name]
                if build_check['can_build']:
                    score += 0.2  # Bonus for viable building construction
                else:
                    score -= 0.6  # Penalty for impossible construction
        action.estimated_points_gotten = score
        return action