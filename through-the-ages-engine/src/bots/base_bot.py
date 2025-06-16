from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import logging

class BaseBot(ABC):
    def __init__(self, bot_id: str, name: str, difficulty: str = "medium"):
        """Clase base para todos los bots

        Args:
            bot_id (str): Identificador único del bot
            name (str): Nombre del bot
            difficulty (str): Nivel de dificultad (easy, medium, hard)
        """
        self.bot_id = bot_id
        self.name = name
        self.difficulty = difficulty
        self.games_played = 0
        self.games_won = 0
        self.player_id = None

        # CONTADORES DE ACCIONES POR TURNO
        self.civil_actions_left = 4  # Máximo 4 acciones civiles por turno
        self.military_actions_left = 2  # Máximo 2 acciones militares por turno

    @abstractmethod
    def make_move(self, game_state: Dict, available_actions: List[Dict]) -> Dict:
        """Hace un movimiento basado en el estado del juego

        Args:
            game_state (Dict): Estado actual del juego
            available_actions (List[Dict]): Acciones disponibles

        Returns:
            Dict: Movimiento seleccionado
        """
        pass

    @abstractmethod
    def evaluate_position(self, game_state: Dict) -> float:
        """Evalúa la posición actual del juego

        Args:
            game_state (Dict): Estado del juego

        Returns:
            float: Puntuación de la posición (-1 a 1)
        """
        pass

    def update_performance(self, won: bool, score: int):
        """Actualiza estadísticas de rendimiento

        Args:
            won (bool): Si ganó el juego
            score (int): Puntuación obtenida
        """
        self.games_played += 1
        if won:
            self.games_won += 1

    def set_player_id(self, player_id: int):
        """Establece el ID del jugador

        Args:
            player_id (int): ID del jugador
        """
        self.player_id = player_id

    def consume_civil_action(self, count: int = 1):
        """Consume acciones civiles

        Args:
            count (int): Número de acciones civiles a consumir
        """
        self.civil_actions_left = max(0, self.civil_actions_left - count)

    def consume_military_action(self, count: int = 1):
        """Consume acciones militares

        Args:
            count (int): Número de acciones militares a consumir
        """
        self.military_actions_left = max(0, self.military_actions_left - count)

    def reset_actions_for_turn(self):
        """Resetea contadores de acciones para nuevo turno"""
        self.civil_actions_left = 4
        self.military_actions_left = 2

        win_rate = self.games_won / self.games_played if self.games_played > 0 else 0
        logging.info(f"Bot {self.name}: {self.games_won}/{self.games_played} ganados ({win_rate:.2%})")

    def get_stats(self) -> Dict:
        """Obtiene estadísticas del bot"""
        return {
            'bot_id': self.bot_id,
            'name': self.name,
            'difficulty': self.difficulty,
            'games_played': self.games_played,
            'games_won': self.games_won,
            'win_rate': self.games_won / self.games_played if self.games_played > 0 else 0
        }

    def reset_stats(self):
        """Reinicia estadísticas del bot"""
        self.games_played = 0
        self.games_won = 0

    def __str__(self):
        return f"Bot {self.name} ({self.difficulty})"

class BotManager:
    def __init__(self):
        """Gestor de bots para el juego"""
        self.registered_bots = {}
        self.active_bots = {}

    def register_bot(self, bot: BaseBot):
        """Registra un bot en el sistema

        Args:
            bot (BaseBot): Bot a registrar
        """
        self.registered_bots[bot.bot_id] = bot
        logging.info(f"Bot registrado: {bot.name} (ID: {bot.bot_id})")

    def get_bot(self, bot_id: str) -> Optional[BaseBot]:
        """Obtiene un bot por su ID

        Args:
            bot_id (str): ID del bot

        Returns:
            BaseBot: Bot encontrado o None
        """
        return self.registered_bots.get(bot_id)

    def create_bot_instance(self, bot_type: str, bot_id: str, name: str, difficulty: str = "medium") -> BaseBot:
        """Crea una nueva instancia de bot

        Args:
            bot_type (str): Tipo de bot (algorithmic, ai, human)
            bot_id (str): ID único del bot
            name (str): Nombre del bot
            difficulty (str): Nivel de dificultad

        Returns:
            BaseBot: Nueva instancia de bot
        """
        if bot_type == "algorithmic":
            from .algorithmic_bot import AlgorithmicBot
            return AlgorithmicBot(bot_id, name, difficulty)
        elif bot_type == "ai":
            from .ai_bot import AIBot
            return AIBot(bot_id, name, difficulty)
        else:
            raise ValueError(f"Tipo de bot no soportado: {bot_type}")

    def get_available_bots(self) -> List[str]:
        """Lista todos los bots disponibles"""
        return list(self.registered_bots.keys())

    def get_bot_stats(self) -> List[Dict]:
        """Obtiene estadísticas de todos los bots"""
        return [bot.get_stats() for bot in self.registered_bots.values()]