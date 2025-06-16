from typing import Dict, List, Optional, Tuple, Any
import logging
from .cards import Card

# Import the new modular PlayerBoard
from .player_board_new import PlayerBoard


class GameBoard:
    """Tablero principal del juego que gestiona elementos compartidos"""

    def __init__(self, num_players: int):
        """Inicializa el tablero principal del juego

        Args:
            num_players (int): Número de jugadores en la partida
        """
        self.num_players = num_players

        # TABLEROS INDIVIDUALES DE JUGADORES - Now using modular PlayerBoard
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

        logging.info(f"GameBoard initialized for {num_players} players with modular PlayerBoards")

    def get_player_board(self, player_id: int) -> Optional[PlayerBoard]:
        """Obtiene el tablero de un jugador específico

        Args:
            player_id (int): ID del jugador

        Returns:
            Optional[PlayerBoard]: Tablero del jugador o None si no existe
        """
        return self.player_boards.get(player_id)

    def advance_age(self):
        """Avanza a la siguiente edad del juego"""
        if self.current_age == "A":
            self.current_age = "I"
        elif self.current_age == "I":
            self.current_age = "II"
        elif self.current_age == "II":
            self.current_age = "III"

    def get_available_civil_cards(self) -> List[Card]:
        """Obtiene las cartas civiles disponibles en el tablero

        Returns:
            List[Card]: Lista de cartas civiles disponibles
        """
        return [card for card in self.visible_civil_cards if card is not None]

    def get_available_military_cards(self) -> List[Card]:
        """Obtiene las cartas militares disponibles en el tablero

        Returns:
            List[Card]: Lista de cartas militares disponibles
        """
        return [card for card in self.visible_military_cards if card is not None]

    def setup_initial_civil_row(self):
        """Configura la fila inicial de cartas civiles"""
        # Esta función será implementada cuando se integre el sistema de cartas
        pass

    def get_available_civil_actions(self, player_id: int) -> List[Dict[str, Any]]:
        """Get available civil actions for a player using the modular system

        Args:
            player_id (int): Player ID

        Returns:
            List[Dict[str, Any]]: Available actions
        """
        player_board = self.get_player_board(player_id)
        if not player_board:
            return []

        return player_board.get_available_civil_actions(player_id)
