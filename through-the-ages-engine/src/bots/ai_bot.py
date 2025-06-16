import random
import numpy as np
import logging
from typing import Dict, List, Tuple
from .base_bot import BaseBot

class AIBot(BaseBot):
    def __init__(self, bot_id: str, name: str, difficulty: str = "medium"):
        """Bot de IA que aprende usando Q-Learning

        Args:
            bot_id (str): ID único del bot
            name (str): Nombre del bot
            difficulty (str): Nivel de dificultad
        """
        super().__init__(bot_id, name, difficulty)

        # Parámetros de Q-Learning
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.epsilon = 0.1  # Exploración vs explotación

        # Tabla Q - mapea estados a valores de acción
        self.q_table = {}

        # Historial para entrenamiento
        self.state_action_history = []
        self.last_state = None
        self.last_action = None

    def make_move(self, game_state: Dict, available_actions: List[Dict]) -> Dict:
        """Hace un movimiento usando Q-Learning

        Args:
            game_state (Dict): Estado actual del juego
            available_actions (List[Dict]): Acciones disponibles

        Returns:
            Dict: Movimiento seleccionado
        """
        if not available_actions:
            logging.warning(f"AI Bot {self.name}: Sin acciones disponibles")
            return {}

        # Convierte el estado del juego a una representación simple
        state_key = self._encode_game_state(game_state)

        # EPSILON-GREEDY
        # Decide entre exploración y explotación
        if random.random() < self.epsilon:
            # Exploración: acción aleatoria
            selected_action = random.choice(available_actions)
            logging.info(f"AI Bot {self.name} explorando - acción aleatoria")
        else:
            # Explotación: mejor acción conocida
            selected_action = self._get_best_action(state_key, available_actions)
            logging.info(f"AI Bot {self.name} explotando - mejor acción conocida")

        # Guarda estado y acción para aprendizaje
        self.last_state = state_key
        self.last_action = self._encode_action(selected_action)

        return selected_action

    def _encode_game_state(self, game_state: Dict) -> str:
        """Convierte estado del juego a clave string

        Args:
            game_state (Dict): Estado del juego

        Returns:
            str: Representación codificada del estado
        """
        player_resources = game_state.get('current_player_resources', {})

        # Simplifica el estado a características clave
        state_features = [
            min(player_resources.get('food', 0), 10),  # Limita valores para reducir espacio de estados
            min(player_resources.get('material', 0), 10),
            min(player_resources.get('culture', 0), 50),
            min(player_resources.get('strength', 0), 10),
            min(game_state.get('turn', 0), 20)
        ]

        return '_'.join(map(str, state_features))

    def _encode_action(self, action: Dict) -> str:
        """Codifica una acción como string

        Args:
            action (Dict): Acción del juego

        Returns:
            str: Representación codificada de la acción
        """
        action_type = action.get('type', 'unknown')
        target = action.get('target', '')
        return f"{action_type}_{target}"

    def _get_best_action(self, state_key: str, available_actions: List[Dict]) -> Dict:
        """Obtiene la mejor acción para un estado dado

        Args:
            state_key (str): Estado codificado
            available_actions (List[Dict]): Acciones disponibles

        Returns:
            Dict: Mejor acción
        """
        if state_key not in self.q_table:
            # Estado nuevo - inicializa con valores aleatorios pequeños
            self.q_table[state_key] = {}

        best_action = None
        best_value = float('-inf')

        for action in available_actions:
            action_key = self._encode_action(action)

            # Obtiene valor Q o inicializa con valor pequeño aleatorio
            q_value = self.q_table[state_key].get(action_key, random.uniform(-0.1, 0.1))

            if q_value > best_value:
                best_value = q_value
                best_action = action

        return best_action if best_action else random.choice(available_actions)

    def learn_from_reward(self, reward: float, new_game_state: Dict = None):
        """Actualiza Q-table basado en recompensa recibida

        Args:
            reward (float): Recompensa recibida
            new_game_state (Dict): Nuevo estado del juego (opcional)
        """
        if self.last_state is None or self.last_action is None:
            return

        # ACTUALIZACIÓN
        # Inicializa entrada en Q-table si no existe
        if self.last_state not in self.q_table:
            self.q_table[self.last_state] = {}

        current_q = self.q_table[self.last_state].get(self.last_action, 0.0)

        # Calcula valor futuro máximo
        future_value = 0.0
        if new_game_state:
            new_state_key = self._encode_game_state(new_game_state)
            if new_state_key in self.q_table:
                future_value = max(self.q_table[new_state_key].values()) if self.q_table[new_state_key] else 0.0

        # Actualización Q-Learning
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * future_value - current_q)
        self.q_table[self.last_state][self.last_action] = new_q

        logging.debug(f"AI Bot {self.name} actualizó Q-value: {current_q:.3f} -> {new_q:.3f}")

    def evaluate_position(self, game_state: Dict) -> float:
        """Evalúa la posición actual usando la Q-table"""
        state_key = self._encode_game_state(game_state)

        if state_key not in self.q_table or not self.q_table[state_key]:
            return 0.0

        # Promedio de valores Q para este estado
        avg_q_value = sum(self.q_table[state_key].values()) / len(self.q_table[state_key])

        # Normaliza a rango [-1, 1]
        return max(-1.0, min(1.0, avg_q_value))

    def save_model(self, filepath: str):
        """Guarda el modelo Q-table a archivo

        Args:
            filepath (str): Ruta donde guardar el modelo
        """
        import json
        try:
            with open(filepath, 'w') as f:
                json.dump(self.q_table, f, indent=2)
            logging.info(f"Modelo AI guardado en {filepath}")
        except Exception as e:
            logging.error(f"Error guardando modelo AI: {e}")

    def load_model(self, filepath: str):
        """Carga modelo Q-table desde archivo

        Args:
            filepath (str): Ruta del archivo del modelo
        """
        import json
        try:
            with open(filepath, 'r') as f:
                self.q_table = json.load(f)
            logging.info(f"Modelo AI cargado desde {filepath}")
        except FileNotFoundError:
            logging.info(f"No se encontró modelo AI en {filepath}, iniciando con tabla vacía")
        except Exception as e:
            logging.error(f"Error cargando modelo AI: {e}")

    def adjust_learning_parameters(self, games_played: int):
        """Ajusta parámetros de aprendizaje según experiencia

        Args:
            games_played (int): Número de juegos jugados
        """
        # Reduce exploración con el tiempo
        if games_played > 100:
            self.epsilon = max(0.05, self.epsilon * 0.995)

        # Reduce tasa de aprendizaje gradualmente
        if games_played > 50:
            self.learning_rate = max(0.01, self.learning_rate * 0.999)

        logging.debug(f"AI Bot {self.name}: epsilon={self.epsilon:.3f}, lr={self.learning_rate:.3f}")

    def get_q_table_stats(self) -> Dict:
        """Obtiene estadísticas de la Q-table"""
        if not self.q_table:
            return {'states': 0, 'actions': 0, 'avg_q_value': 0.0}

        total_actions = sum(len(actions) for actions in self.q_table.values())
        all_q_values = [q for actions in self.q_table.values() for q in actions.values()]
        avg_q_value = sum(all_q_values) / len(all_q_values) if all_q_values else 0.0

        return {
            'states': len(self.q_table),
            'actions': total_actions,
            'avg_q_value': avg_q_value
        }