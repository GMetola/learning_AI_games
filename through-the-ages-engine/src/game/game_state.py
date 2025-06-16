from typing import Dict, List
import logging
from .board import PlayerBoard, GameBoard

class GameState:
    def __init__(self):
        # Inicializa el estado del juego
        self.players = []
        self.current_turn = 0
        self.turn_number = 1
        self.game_over = False
        self.board = None  # Se inicializará con el número de jugadores

    def add_player(self, player):
        # Agrega un jugador al juego
        self.players.append(player)

    def initialize_game(self, players: List[str], bot_types: List[str]):
        """Inicializa el juego con jugadores y tipos de bot

        Args:
            players (List[str]): Lista de nombres de jugadores
            bot_types (List[str]): Tipos de bot para cada jugador
        """
        from .player import Player

        self.players = []
        self.bot_types = bot_types
        num_players = len(players)

        # INICIALIZACIÓN TABLERO
        # Crea el tablero principal con el número correcto de jugadores
        self.board = GameBoard(num_players)

        for i, (player_name, bot_type) in enumerate(zip(players, bot_types)):
            player = Player(player_name)
            player.bot_type = bot_type
            player.player_id = i + 1  # IDs de jugador de 1 a 4

            # Vincula el tablero individual del jugador (PlayerBoard)
            player_board = self.board.player_boards[player.player_id]
            player.set_board(player_board)
            self.players.append(player)

        self.current_turn = 0
        self.game_over = False
        self.turn_number = 1

        # Carga cartas iniciales si están disponibles
        self._setup_initial_cards()

    def _setup_initial_cards(self):
        """Configura cartas iniciales en el tablero"""
        try:
            from .cards import CardLoader
            loader = CardLoader()
            cards = loader.load_cards_from_csv()

            if cards:
                self.board.setup_initial_civil_row()
                logging.info("Cartas iniciales configuradas en el tablero")
        except Exception as e:
            logging.warning(f"No se pudieron cargar cartas iniciales: {e}")

    def get_current_player(self) -> str:
        """Obtiene el nombre del jugador actual"""
        if self.players:
            return self.players[self.current_turn].name
        return ""

    def get_state(self) -> Dict:
        """Obtiene el estado completo del juego"""
        current_player = self.players[self.current_turn] if self.players else None

        return {
            'turn': self.turn_number,
            'current_player': current_player.name if current_player else "",
            'current_player_resources': current_player.resources if current_player else {},
            'opponents_resources': [p.resources for p in self.players if p != current_player],
            'game_over': self.game_over,
            'players_info': [
                {
                    'name': p.name,
                    'resources': p.resources,
                    'cards': len(p.cards),
                    'bot_type': getattr(p, 'bot_type', 'human')
                } for p in self.players
            ]
        }

    def get_public_state(self) -> Dict:
        """Obtiene estado público del juego (sin información privada)"""
        return {
            'turn': self.turn_number,
            'current_player': self.get_current_player(),
            'players': [
                {
                    'name': p.name,
                    'score': p.resources.get('culture', 0),
                    'strength': p.resources.get('strength', 0),
                    'cards_count': len(p.cards)
                } for p in self.players
            ],
            'game_over': self.game_over
        }

    def get_available_actions(self) -> List[Dict]:
        """Obtiene acciones disponibles para el jugador actual usando el tablero"""
        current_player = self.players[self.current_turn] if self.players else None
        if not current_player or not self.board:
            return []

        # Obtiene acciones del tablero principal
        board_actions = self.board.get_available_civil_actions(current_player.player_id)

        # Agrega acciones básicas siempre disponibles
        basic_actions = [{"type": "end_turn", "cost": 0}]

        return board_actions + basic_actions

    def execute_action(self, player_name: str, action: Dict) -> Dict:
        """Ejecuta una acción del jugador usando el tablero

        Args:
            player_name (str): Nombre del jugador
            action (Dict): Acción a ejecutar

        Returns:
            Dict: Resultado de la acción
        """
        player = None
        for p in self.players:
            if p.name == player_name:
                player = p
                break

        if not player:
            return {"success": False, "error": "Jugador no encontrado"}

        # VALIDACIÓN
        if self.get_current_player() != player_name:
            return {"success": False, "error": "No es el turno de este jugador"}

        action_type = action.get('type', '')

        # EJECUCIÓN DE ACCIONES
        if action_type == 'take_card':
            return self._execute_take_card(player, action)
        elif action_type == 'increase_population':
            return self._execute_increase_population(player, action)
        elif action_type == 'assign_worker':
            return self._execute_assign_worker(player, action)
        elif action_type == 'end_turn':
            return {"success": True, "message": "Turno terminado"}
        else:
            return {"success": False, "error": f"Tipo de acción no reconocido: {action_type}"}

    def _execute_take_card(self, player, action: Dict) -> Dict:
        """Ejecuta tomar carta civil del tablero"""
        card_position = action.get('card_position', -1)
        cost = action.get('cost', {})

        if card_position < 0 or card_position >= len(self.board.visible_civil_cards):
            return {"success": False, "error": "Posición de carta inválida"}

        # Verifica costes
        science_cost = cost.get('science', 0)
        if player.board.resources['science'] < science_cost:
            return {"success": False, "error": "Ciencia insuficiente"}

        # Ejecuta la acción
        card = self.board.visible_civil_cards[card_position]
        player.board.resources['science'] -= science_cost
        player.board.actions['civil'] -= 1

        # Agrega carta a tecnologías del jugador
        if card:
            player.board.current_technologies[card.name] = {
                'type': card.get_type(),
                'category': card.category,
                'age': card.age,
                'production': card.production,
                'workers': 0
            }

            # Remueve carta del tablero
            self.board.visible_civil_cards[card_position] = None

        return {"success": True, "message": f"Carta {card.name} adquirida"}

    def _execute_increase_population(self, player, action: Dict) -> Dict:
        """Ejecuta aumento de población"""
        cost = action.get('cost', {})
        food_cost = cost.get('food', 0)

        if player.board.resources['food'] < food_cost:
            return {"success": False, "error": "Comida insuficiente"}

        # Ejecuta la acción
        player.board.resources['food'] -= food_cost
        player.board.actions['civil'] -= 1
        player.board.tokens['yellow'] += 1

        # Actualiza grupo de población en reserva amarilla
        next_group = self.board._get_next_population_group(player.player_id)
        if next_group:
            next_group['positions_filled'] += 1

        return {"success": True, "message": "Población aumentada"}

    def _execute_assign_worker(self, player, action: Dict) -> Dict:
        """Ejecuta asignación de trabajador a tecnología"""
        tech_name = action.get('technology', '')

        if tech_name not in player.board.current_technologies:
            return {"success": False, "error": "Tecnología no disponible"}

        if player.board.tokens['yellow'] <= sum(player.board.worker_assignments.values()):
            return {"success": False, "error": "No hay trabajadores disponibles"}

        # Asigna trabajador
        player.board.worker_assignments[tech_name] += 1

        return {"success": True, "message": f"Trabajador asignado a {tech_name}"}

    def is_game_over(self) -> bool:
        """Verifica si el juego ha terminado"""
        # Condición simple: juego termina después de 20 turnos
        return self.turn_number > 20 or self.game_over

    def next_turn(self):
        """Avanza al siguiente turno"""
        # COMPLETAR TURNO DEL JUGADOR ACTUAL
        current_player = self.players[self.current_turn]
        turn_summary = current_player.board.complete_turn()

        # Guardar resumen del turno para estadísticas
        if not hasattr(self, 'turn_summaries'):
            self.turn_summaries = []
        self.turn_summaries.append(turn_summary)

        # AVANZAR AL SIGUIENTE JUGADOR
        self.current_turn = (self.current_turn + 1) % len(self.players)

        # Si volvemos al primer jugador, incrementa número de turno
        if self.current_turn == 0:
            self.turn_number += 1
            logging.info(f"Iniciando turno {self.turn_number}")

    def _production_phase(self):
        """Fase de producción de recursos (obsoleta - ahora se hace en PlayerBoard.complete_turn)"""
        # Esta función ya no se usa, la producción se maneja individualmente
        pass

    def check_game_over(self):
        # Verifica si el juego ha terminado
        if len(self.players) < 2:
            self.game_over = True

    def reset_game(self):
        # Reinicia el estado del juego
        self.players = []
        self.current_turn = 0
        self.game_over = False