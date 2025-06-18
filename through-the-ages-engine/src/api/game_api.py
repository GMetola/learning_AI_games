from flask import Flask, request, jsonify
import logging
import uuid
import random
from datetime import datetime
from typing import Dict, List
from ..game.game_state import GameState
from ..bots.base_bot import BotManager, BaseBot
from ..database.connection import DatabaseConnection
from ..database.models import GameSession, TrainingData

app = Flask(__name__)

# Inicializa componentes
bot_manager = BotManager()
db_connection = DatabaseConnection()
active_games = {}

@app.route('/health', methods=['GET'])
def health_check():
    """Verifica el estado de la API"""
    return jsonify({
        "status": "OK",
        "timestamp": datetime.now().isoformat(),
        "active_games": len(active_games)
    })

@app.route('/start_game', methods=['POST'])
def start_game():
    """Inicia una nueva partida

    Body JSON:
    {
        "players": ["bot1", "bot2", "human"],
        "bot_types": ["algorithmic", "ai", "human"],
        "difficulty": "medium"
    }
    """
    try:
        data = request.json
        players = data.get('players', [])
        bot_types = data.get('bot_types', [])
        difficulty = data.get('difficulty', 'medium')

        if len(players) != len(bot_types):
            return jsonify({"error": "Número de jugadores y tipos no coinciden"}), 400

        # Crea nueva sesión de juego
        session_id = str(uuid.uuid4())
        game_state = GameState()

        # INICIALIZACIÓN
        # Inicializa jugadores y bots
        for i, (player_name, bot_type) in enumerate(zip(players, bot_types)):
            if bot_type != "human":
                bot_id = f"{bot_type}_{i}_{session_id[:8]}"
                bot = bot_manager.create_bot_instance(bot_type, bot_id, player_name, difficulty)
                bot_manager.register_bot(bot)

        # Configura el estado del juego
        game_state.initialize_game(players, bot_types)
        active_games[session_id] = {
            'game_state': game_state,
            'players': players,
            'bot_types': bot_types,
            'start_time': datetime.now()
        }

        # Guarda sesión en base de datos
        session = GameSession(session_id, players, bot_types)
        if db_connection.connect():
            collection = db_connection.get_collection('game_sessions')
            collection.insert_one(session.to_dict())

        logging.info(f"Juego iniciado: {session_id} con jugadores {players}")

        return jsonify({
            "session_id": session_id,
            "players": players,
            "current_player": game_state.get_current_player(),
            "game_state": game_state.get_public_state()
        })

    except Exception as e:
        logging.error(f"Error iniciando juego: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/make_move', methods=['POST'])
def make_move():
    """Realiza un movimiento en el juego

    Body JSON:
    {
        "session_id": "uuid",
        "player_id": "player_name",
        "action": {"type": "build_farm", "target": "location"}
    }
    """
    try:
        data = request.json
        session_id = data.get('session_id')
        player_id = data.get('player_id')
        action = data.get('action')

        if session_id not in active_games:
            return jsonify({"error": "Sesión de juego no encontrada"}), 404

        game_info = active_games[session_id]
        game_state = game_info['game_state']

        # Verifica que sea el turno del jugador
        if game_state.get_current_player() != player_id:
            return jsonify({"error": "No es el turno de este jugador"}), 400

        # MOVIMIENTO
        # Ejecuta la acción
        result = game_state.execute_action(player_id, action)

        if result['success']:
            # Guarda datos de entrenamiento para bots IA
            player_index = game_info['players'].index(player_id)
            if game_info['bot_types'][player_index] == 'ai':
                # Calculate reward based on move outcome
                reward = _calculate_move_reward(result, game_state, player_id)

                training_data = TrainingData(
                    bot_id=f"ai_{player_index}_{session_id[:8]}",
                    game_session_id=session_id,
                    move_data=action,
                    reward=reward
                )

            # Avanza al siguiente jugador
            game_state.next_turn()

            return jsonify({
                "success": True,
                "game_state": game_state.get_public_state(),
                "next_player": game_state.get_current_player(),
                "game_over": game_state.is_game_over()
            })
        else:
            return jsonify(result), 400

    except Exception as e:
        logging.error(f"Error ejecutando movimiento: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/bot_move', methods=['POST'])
def bot_move():
    """Solicita movimiento de un bot

    Body JSON:
    {
        "session_id": "uuid",
        "bot_id": "bot_name"
    }
    """
    try:
        data = request.json
        session_id = data.get('session_id')
        bot_id = data.get('bot_id')

        if session_id not in active_games:
            return jsonify({"error": "Sesión no encontrada"}), 404

        game_info = active_games[session_id]
        game_state = game_info['game_state']

        # Obtiene el bot
        bot = bot_manager.get_bot(bot_id)
        if not bot:
            return jsonify({"error": "Bot no encontrado"}), 404

        # MOVIMIENTO BOT
        # Obtiene acciones disponibles y solicita movimiento al bot
        available_actions = game_state.get_available_actions()
        selected_action = bot.make_move(game_state.get_state(), available_actions)

        # Ejecuta el movimiento del bot
        result = game_state.execute_action(bot.name, selected_action)

        if result['success']:
            game_state.next_turn()

            return jsonify({
                "success": True,
                "action_taken": selected_action,
                "game_state": game_state.get_public_state(),
                "next_player": game_state.get_current_player()
            })
        else:
            return jsonify(result), 400

    except Exception as e:
        logging.error(f"Error en movimiento de bot: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_game_state/<session_id>', methods=['GET'])
def get_game_state(session_id):
    """Obtiene el estado actual del juego"""
    if session_id not in active_games:
        return jsonify({"error": "Sesión no encontrada"}), 404

    game_state = active_games[session_id]['game_state']
    return jsonify({
        "session_id": session_id,
        "game_state": game_state.get_public_state(),
        "current_player": game_state.get_current_player(),
        "available_actions": game_state.get_available_actions(),
        "game_over": game_state.is_game_over()
    })

@app.route('/train_ai', methods=['POST'])
def train_ai():
    """Ejecuta sesiones de entrenamiento para bots IA

    Body JSON:
    {
        "num_games": 100,
        "ai_bot_id": "ai_bot_1",
        "opponent_types": ["algorithmic", "algorithmic"]
    }
    """
    try:
        data = request.json
        num_games = data.get('num_games', 10)
        ai_bot_id = data.get('ai_bot_id')
        opponent_types = data.get('opponent_types', ['algorithmic'])

        training_results = []

        # ENTRENAMIENTO
        # Ejecuta múltiples juegos para entrenamiento
        for game_num in range(num_games):
            # Crea nueva sesión de entrenamiento
            training_session_id = f"training_{ai_bot_id}_{game_num}"

            players = [ai_bot_id] + [f"opp_{i}" for i in range(len(opponent_types))]
            bot_types = ['ai'] + opponent_types

            # Simula juego completo
            game_result = simulate_training_game(training_session_id, players, bot_types)
            training_results.append(game_result)

            # Actualiza bot IA con resultado
            ai_bot = bot_manager.get_bot(ai_bot_id)
            if ai_bot:
                ai_bot.adjust_learning_parameters(game_num + 1)

        return jsonify({
            "training_completed": True,
            "games_played": num_games,
            "results": training_results[-5:]  # Últimos 5 resultados
        })

    except Exception as e:
        logging.error(f"Error en entrenamiento: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/bot_stats', methods=['GET'])
def get_bot_stats():
    """Obtiene estadísticas de todos los bots"""
    return jsonify({
        "bot_stats": bot_manager.get_bot_stats(),
        "available_bots": bot_manager.get_available_bots()
    })

def simulate_training_game(session_id: str, players: List[str], bot_types: List[str]) -> Dict:
    """Simula un juego completo para entrenamiento

    Args:
        session_id (str): ID de la sesión de entrenamiento
        players (List[str]): Lista de jugadores
        bot_types (List[str]): Tipos de cada jugador

    Returns:
        Dict: Resultado del juego
    """
    # Implementación simplificada de simulación de juego
    # En la implementación real, esto ejecutaría un juego completo
    winner = players[0]  # Placeholder
    scores = {player: 50 + random.randint(-20, 20) for player in players}

    return {
        "session_id": session_id,
        "winner": winner,
        "scores": scores,
        "turns_played": 15
    }

def _calculate_move_reward(result: Dict, game_state: GameState, player_id: str) -> float:
    """Calculate reward for AI training based on move outcome

    Args:
        result (Dict): Result of the executed action
        game_state (GameState): Current game state
        player_id (str): Player who made the move

    Returns:
        float: Reward value (-1.0 to 1.0)
    """
    reward = 0.0

    # Base reward for successful actions
    if result.get('success', False):
        reward += 0.1
    else:
        reward -= 0.3

    # Find player in game state
    player = None
    for p in game_state.players:
        if p.name == player_id:
            player = p
            break

    if not player:
        return reward

    # Reward based on resource gains
    if 'player_id' in result:
        player_board = player.board
        resources = player_board.resources

        # Reward for having balanced resources
        total_resources = sum(resources.values())
        if total_resources > 0:
            # Bonus for resource diversity
            non_zero_resources = sum(1 for v in resources.values() if v > 0)
            diversity_bonus = non_zero_resources / len(resources) * 0.1
            reward += diversity_bonus

        # Reward for production buildings
        production_count = len(player_board.production_buildings)
        reward += production_count * 0.05

        # Reward for population growth
        available_workers = player_board.yellow_reserves.get('available_workers', 0)
        if available_workers > 3:
            reward += 0.1

        # Penalty for corruption
        corruption = player_board.get_corruption_penalty()
        reward -= corruption * 0.02

    # Reward for game progression
    if hasattr(game_state, 'turn_number'):
        # Later game actions should be more carefully evaluated
        turn_factor = min(game_state.turn_number / 50.0, 1.0)
        reward *= (1.0 + turn_factor * 0.5)

    # Clamp reward between -1.0 and 1.0
    return max(-1.0, min(1.0, reward))

if __name__ == '__main__':
    # Configura logging
    logging.basicConfig(level=logging.INFO)

    # Conecta a base de datos
    if db_connection.connect():
        logging.info("Conectado a MongoDB exitosamente")

    app.run(debug=True, host='0.0.0.0', port=5000)
