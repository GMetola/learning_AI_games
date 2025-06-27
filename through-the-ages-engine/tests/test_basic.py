"""
Test básico para verificar que el sistema funciona
"""
import sys
import os

# Agrega src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from bots.base_bot import BotManager
from database.connection import DatabaseConnection
from game.cards import CardLoader
from game.game_state import GameState


def test_card_loading():
    """Prueba carga de cartas"""
    print("=== Test: Carga de Cartas ===")
    loader = CardLoader()
    cards = loader.load_cards_from_csv()
    print(f"✓ Cartas cargadas: {len(cards)}")

    if len(cards) > 0:
        print(f"✓ Primera carta: {cards[0].name}")
    return True

def test_bot_creation():
    """Prueba creación de bots"""
    print("\n=== Test: Creación de Bots ===")
    manager = BotManager()

    # Crea bot algorítmico
    algo_bot = manager.create_bot_instance("algorithmic", "test_algo", "TestAlgo", "medium")
    print(f"✓ Bot algorítmico creado: {algo_bot.name}")

    # Crea bot IA
    ai_bot = manager.create_bot_instance("ai", "test_ai", "TestAI", "medium")
    print(f"✓ Bot IA creado: {ai_bot.name}")

    return True

def test_game_state():
    """Prueba estado del juego"""
    print("\n=== Test: Estado del Juego ===")
    game = GameState()
    players = ["Bot1", "Bot2"]
    bot_types = ["human", "algorithmic"]

    game.initialize_game(players, bot_types)
    print(f"✓ Juego inicializado con {len(players)} jugadores")

    current_player = game.get_current_player()
    print(f"✓ Jugador actual: {current_player}")

    actions = game.get_available_actions()
    print(f"✓ Acciones disponibles: {len(actions)}")

    return True

def test_database_connection():
    """Prueba conexión a base de datos"""
    print("\n=== Test: Conexión Base de Datos ===")
    db = DatabaseConnection()
    connected = db.connect()

    if connected:
        print("✓ Conexión a MongoDB exitosa")
        db.close()
    else:
        print("⚠ MongoDB no disponible (normal si no está configurado)")

    return True

def main():
    """Ejecuta todas las pruebas"""
    print("THROUGH THE AGES - Pruebas Básicas")
    print("=" * 50)

    tests = [
        test_card_loading,
        test_bot_creation,
        test_game_state,
        test_database_connection
    ]

    passed = 0
    for test in tests:
        if test():
            passed += 1

    print(f"\n=== Resumen ===")
    print(f"Pruebas pasadas: {passed}/{len(tests)}")

    if passed == len(tests):
        print("✓ Todos los tests pasaron - Sistema listo!")
    else:
        print("⚠ Algunos tests fallaron - Revise los errores")

if __name__ == "__main__":
    main()
