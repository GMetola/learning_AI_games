from datetime import datetime
from typing import List, Dict, Optional

class GameSession:
    def __init__(self, session_id: str, players: List[str], bot_types: List[str]):
        """Modelo para sesión de juego

        Args:
            session_id (str): ID único de la sesión
            players (List[str]): Lista de nombres de jugadores
            bot_types (List[str]): Tipos de bots (human, algorithmic, ai)
        """
        self.session_id = session_id
        self.players = players
        self.bot_types = bot_types
        self.start_time = datetime.now()
        self.end_time = None
        self.game_state = {}
        self.moves_history = []
        self.winner = None
        self.final_scores = {}

    def to_dict(self) -> Dict:
        """Convierte la sesión a diccionario para MongoDB"""
        return {
            'session_id': self.session_id,
            'players': self.players,
            'bot_types': self.bot_types,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'game_state': self.game_state,
            'moves_history': self.moves_history,
            'winner': self.winner,
            'final_scores': self.final_scores
        }

class TrainingData:
    def __init__(self, bot_id: str, game_session_id: str, move_data: Dict):
        """Modelo para datos de entrenamiento de IA

        Args:
            bot_id (str): ID del bot
            game_session_id (str): ID de la sesión de juego
            move_data (Dict): Datos del movimiento realizado
        """
        self.bot_id = bot_id
        self.game_session_id = game_session_id
        self.move_data = move_data
        self.game_state_before = {}
        self.game_state_after = {}
        self.reward = 0
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict:
        """Convierte los datos de entrenamiento a diccionario"""
        return {
            'bot_id': self.bot_id,
            'game_session_id': self.game_session_id,
            'move_data': self.move_data,
            'game_state_before': self.game_state_before,
            'game_state_after': self.game_state_after,
            'reward': self.reward,
            'timestamp': self.timestamp
        }

class BotPerformance:
    def __init__(self, bot_id: str, bot_type: str):
        """Modelo para rendimiento de bots

        Args:
            bot_id (str): ID del bot
            bot_type (str): Tipo de bot (algorithmic, ai)
        """
        self.bot_id = bot_id
        self.bot_type = bot_type
        self.games_played = 0
        self.games_won = 0
        self.average_score = 0.0
        self.win_rate = 0.0
        self.last_updated = datetime.now()

    def update_performance(self, won: bool, score: int):
        """Actualiza estadísticas de rendimiento"""
        self.games_played += 1
        if won:
            self.games_won += 1

        # Actualiza promedio de puntuación
        self.average_score = ((self.average_score * (self.games_played - 1)) + score) / self.games_played
        self.win_rate = self.games_won / self.games_played
        self.last_updated = datetime.now()

    def to_dict(self) -> Dict:
        """Convierte el rendimiento a diccionario"""
        return {
            'bot_id': self.bot_id,
            'bot_type': self.bot_type,
            'games_played': self.games_played,
            'games_won': self.games_won,
            'average_score': self.average_score,
            'win_rate': self.win_rate,
            'last_updated': self.last_updated
        }