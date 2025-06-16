"""
Punto de entrada principal para Through the Ages Engine
"""
import sys
import os
import logging

# Agrega el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Función principal"""
    print("Through the Ages - Motor de Juego")
    print("1. Interfaz de Consola")
    print("2. Servidor API")
    print("3. Cargar y probar cartas")
    print("4. Salir")

    choice = input("Seleccione opción (1-4): ").strip()

    if choice == "1":
        start_console_interface()
    elif choice == "2":
        start_api_server()
    elif choice == "3":
        test_card_loading()
    elif choice == "4":
        print("¡Hasta luego!")
    else:
        print("Opción inválida")

def start_console_interface():
    """Inicia la interfaz de consola"""
    try:
        from src.ui.console_ui import ConsoleUI
        ui = ConsoleUI()
        ui.start_interactive_session()
    except ImportError as e:
        print(f"Error importando módulos: {e}")
        print("Asegúrese de que todas las dependencias estén instaladas")

def start_api_server():
    """Inicia el servidor API"""
    try:
        print("Iniciando servidor API en puerto 5000...")
        from src.api.game_api import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError as e:
        print(f"Error importando módulos: {e}")
        print("Instale las dependencias con: pip install -r requirements.txt")

def test_card_loading():
    """Prueba la carga de cartas desde CSV"""
    try:
        from src.game.cards import CardLoader

        print("Cargando cartas desde CSV...")
        loader = CardLoader()
        cards = loader.load_cards_from_csv()

        print(f"Cartas cargadas: {len(cards)}")

        if cards:
            print("\nPrimeras 5 cartas:")
            for i, card in enumerate(cards[:5]):
                print(f"{i+1}. {card.name} ({card.category}, Era {card.age})")
                print(f"   Coste tech: {card.tech_cost}, Coste construcción: {card.build_cost}")

        # Muestra estadísticas por categoría
        categories = {}
        for card in cards:
            cat = card.category
            categories[cat] = categories.get(cat, 0) + 1

        print(f"\nCartas por categoría:")
        for category, count in categories.items():
            print(f"  {category}: {count}")

    except Exception as e:
        print(f"Error cargando cartas: {e}")

if __name__ == "__main__":    # Configura logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    main()
