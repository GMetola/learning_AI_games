import json
import logging
from typing import Dict, List
from ..game.game_state import GameState
from ..bots.base_bot import BotManager
from ..game.cards import CardLoader

class ConsoleUI:
    def __init__(self):
        """Interfaz de consola para Through the Ages"""
        self.game_state = None
        self.bot_manager = BotManager()
        self.card_loader = CardLoader()

    def display_welcome(self):
        """Muestra mensaje de bienvenida"""
        print("=" * 50)
        print("    THROUGH THE AGES - Motor de Juego")
        print("=" * 50)
        print("1. Jugar contra bots")
        print("2. Entrenar bot IA")
        print("3. Ver estadísticas de bots")
        print("4. Salir")
        print("-" * 50)

    def start_interactive_session(self):
        """Inicia sesión interactiva"""
        while True:
            self.display_welcome()
            choice = input("Seleccione una opción (1-4): ").strip()

            if choice == "1":
                self.start_human_vs_bots_game()
            elif choice == "2":
                self.train_ai_bot()
            elif choice == "3":
                self.show_bot_statistics()
            elif choice == "4":
                print("¡Gracias por jugar!")
                break
            else:
                print("Opción inválida. Intente de nuevo.")

    def start_human_vs_bots_game(self):
        """Inicia juego humano vs bots"""
        print("\n--- Configuración de Juego ---")

        # CONFIGURACIÓN
        # Solicita número de jugadores
        while True:
            try:
                num_players = int(input("Número de jugadores (2-4): "))
                if 2 <= num_players <= 4:
                    break
                else:
                    print("Número debe estar entre 2 y 4")
            except ValueError:
                print("Ingrese un número válido")

        # Configura jugadores
        players = ["Humano"]
        bot_types = ["human"]

        for i in range(1, num_players):
            print(f"\nBot {i}:")
            print("1. Algorítmico (Fácil)")
            print("2. Algorítmico (Medio)")
            print("3. Algorítmico (Difícil)")
            print("4. IA (En entrenamiento)")

            while True:
                bot_choice = input("Tipo de bot: ").strip()
                if bot_choice == "1":
                    bot_name = f"AlgoBot_{i}_Easy"
                    bot = self.bot_manager.create_bot_instance("algorithmic", f"bot_{i}", bot_name, "easy")
                    break
                elif bot_choice == "2":
                    bot_name = f"AlgoBot_{i}_Medium"
                    bot = self.bot_manager.create_bot_instance("algorithmic", f"bot_{i}", bot_name, "medium")
                    break
                elif bot_choice == "3":
                    bot_name = f"AlgoBot_{i}_Hard"
                    bot = self.bot_manager.create_bot_instance("algorithmic", f"bot_{i}", bot_name, "hard")
                    break
                elif bot_choice == "4":
                    bot_name = f"AIBot_{i}"
                    bot = self.bot_manager.create_bot_instance("ai", f"ai_bot_{i}", bot_name, "medium")
                    break
                else:
                    print("Opción inválida")

            self.bot_manager.register_bot(bot)
            players.append(bot_name)
            bot_types.append(bot.name.split("_")[0].lower())

        # Inicia juego
        self.game_state = GameState()
        self.game_state.initialize_game(players, bot_types)

        print(f"\n¡Juego iniciado con {num_players} jugadores!")
        self.play_game_loop()

    def play_game_loop(self):
        """Bucle principal del juego"""
        turn_count = 0

        while not self.game_state.is_game_over() and turn_count < 100:
            current_player = self.game_state.get_current_player()
            self.display_game_state()

            # TURNO
            # Verifica si es humano o bot
            if current_player == "Humano":
                self.handle_human_turn()
            else:
                self.handle_bot_turn(current_player)

            self.game_state.next_turn()
            turn_count += 1

            input("\nPresione Enter para continuar...")

        self.display_final_results()

    def display_game_state(self):
        """Muestra el estado actual del juego"""
        print("\n" + "=" * 60)
        print(f"TURNO {self.game_state.turn_number} - Jugador: {self.game_state.get_current_player()}")
        print("=" * 60)

        # Muestra información de todos los jugadores
        for i, player in enumerate(self.game_state.players):
            marker = ">>> " if i == self.game_state.current_turn else "    "
            print(f"{marker}{player.name}:")
            print(f"        Comida: {player.resources.get('food', 0)}")
            print(f"        Recursos: {player.resources.get('material', 0)}")
            print(f"        Cultura: {player.resources.get('culture', 0)}")
            print(f"        Fuerza: {player.resources.get('strength', 0)}")
            print(f"        Ciencia: {player.resources.get('science', 0)}")
            print(f"        Cartas: {len(player.cards)}")
            print()

    def handle_human_turn(self):
        """Maneja el turno del jugador humano"""
        available_actions = self.game_state.get_available_actions()

        print("Acciones disponibles:")
        for i, action in enumerate(available_actions):
            action_desc = self.format_action_description(action)
            print(f"{i + 1}. {action_desc}")

        # SELECCIÓN
        # Solicita selección al jugador
        while True:
            try:
                choice = int(input("Seleccione acción (número): ")) - 1
                if 0 <= choice < len(available_actions):
                    selected_action = available_actions[choice]
                    break
                else:
                    print("Número inválido")
            except ValueError:
                print("Ingrese un número válido")

        # Ejecuta la acción
        result = self.game_state.execute_action("Humano", selected_action)
        if result['success']:
            print(f"✓ {result['message']}")
        else:
            print(f"✗ {result['error']}")

    def handle_bot_turn(self, bot_name: str):
        """Maneja el turno de un bot"""
        # Busca el bot por nombre
        bot = None
        for registered_bot in self.bot_manager.registered_bots.values():
            if registered_bot.name == bot_name:
                bot = registered_bot
                break

        if not bot:
            print(f"Bot {bot_name} no encontrado!")
            return

        # MOVIMIENTO BOT
        # Obtiene acciones disponibles y solicita movimiento
        available_actions = self.game_state.get_available_actions()
        game_state_dict = self.game_state.get_state()

        selected_action = bot.make_move(game_state_dict, available_actions)

        print(f"{bot_name} está pensando...")
        action_desc = self.format_action_description(selected_action)
        print(f"{bot_name} eligió: {action_desc}")

        # Ejecuta la acción del bot
        result = self.game_state.execute_action(bot_name, selected_action)
        if result['success']:
            print(f"✓ {result['message']}")
        else:
            print(f"✗ {result['error']}")

    def format_action_description(self, action: Dict) -> str:
        """Formatea la descripción de una acción"""
        action_type = action.get('type', 'unknown')
        cost = action.get('cost', 0)

        descriptions = {
            'build_farm': f"Construir Granja (Coste: {cost} recursos)",
            'build_mine': f"Construir Mina (Coste: {cost} recursos)",
            'research_tech': f"Investigar Tecnología (Coste: {cost} ciencia)",
            'end_turn': "Terminar Turno"
        }

        return descriptions.get(action_type, f"Acción desconocida: {action_type}")

    def display_final_results(self):
        """Muestra resultados finales del juego"""
        print("\n" + "=" * 50)
        print("           RESULTADOS FINALES")
        print("=" * 50)

        # Ordena jugadores por puntuación
        sorted_players = sorted(
            self.game_state.players,
            key=lambda p: p.resources.get('culture', 0),
            reverse=True
        )

        for i, player in enumerate(sorted_players):
            position = i + 1
            score = player.resources.get('culture', 0)
            print(f"{position}. {player.name}: {score} puntos de cultura")

        winner = sorted_players[0]
        print(f"\n🏆 ¡{winner.name} es el ganador!")

    def train_ai_bot(self):
        """Entrena un bot de IA"""
        print("\n--- Entrenamiento de Bot IA ---")

        # Crea bot IA para entrenamiento
        ai_bot = self.bot_manager.create_bot_instance("ai", "training_ai", "TrainingAI", "medium")
        self.bot_manager.register_bot(ai_bot)

        # Solicita parámetros de entrenamiento
        try:
            num_games = int(input("Número de juegos de entrenamiento (1-1000): "))
            num_games = max(1, min(1000, num_games))
        except ValueError:
            num_games = 10

        print(f"\nEntrenando bot IA con {num_games} juegos...")

        # ENTRENAMIENTO
        # Simula múltiples juegos para entrenamiento
        wins = 0
        for game_num in range(num_games):
            if game_num % 10 == 0:
                print(f"Progreso: {game_num}/{num_games}")

            # Simula juego simple
            game_won = self.simulate_training_game(ai_bot)
            if game_won:
                wins += 1

            ai_bot.adjust_learning_parameters(game_num + 1)

        win_rate = wins / num_games
        print(f"\nEntrenamiento completado:")
        print(f"Juegos ganados: {wins}/{num_games} ({win_rate:.1%})")
        print(f"Estados aprendidos: {len(ai_bot.q_table)}")

    def simulate_training_game(self, ai_bot) -> bool:
        """Simula un juego de entrenamiento

        Args:
            ai_bot: Bot de IA a entrenar

        Returns:
            bool: True si el bot IA ganó
        """
        # Simulación simplificada de un juego
        # En implementación real, esto sería un juego completo

        dummy_state = {
            'turn': 1,
            'current_player_resources': {'food': 2, 'material': 2, 'culture': 0, 'science': 1},
            'opponents_resources': [{'culture': 5}]
        }

        dummy_actions = [
            {'type': 'build_farm', 'cost': 2},
            {'type': 'build_mine', 'cost': 2},
            {'type': 'end_turn', 'cost': 0}
        ]

        # Bot hace un movimiento
        action = ai_bot.make_move(dummy_state, dummy_actions)

        # Simula recompensa aleatoria
        import random
        reward = random.uniform(-1.0, 1.0)
        ai_bot.learn_from_reward(reward)

        return reward > 0

    def show_bot_statistics(self):
        """Muestra estadísticas de todos los bots"""
        print("\n--- Estadísticas de Bots ---")

        stats = self.bot_manager.get_bot_stats()

        if not stats:
            print("No hay bots registrados.")
            return

        for bot_stat in stats:
            print(f"\nBot: {bot_stat['name']}")
            print(f"  Tipo: {bot_stat.get('difficulty', 'unknown')}")
            print(f"  Juegos jugados: {bot_stat['games_played']}")
            print(f"  Juegos ganados: {bot_stat['games_won']}")
            print(f"  Tasa de victoria: {bot_stat['win_rate']:.1%}")

if __name__ == "__main__":
    # Configura logging básico
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    # Inicia interfaz de consola
    ui = ConsoleUI()
    ui.start_interactive_session()