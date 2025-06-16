#!/usr/bin/env python3
"""
Test para verificar el nuevo sistema de grupos para reservas amarillas y azules
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from game.board import PlayerBoard

def test_yellow_reserves_groups():
    """Verifica que las reservas amarillas funcionen con el sistema de grupos"""
    print("=== Test: Sistema de Grupos Amarillos ===")

    # INICIALIZACIÓN
    player_board = PlayerBoard(player_id=1)

    # ESTADO INICIAL
    print("Estado inicial de grupos amarillos:")
    for i, group in enumerate(player_board.yellow_reserves['groups']):
        print(f"  Grupo {i+1}: {group['tokens']} fichas, ocupado: {group['occupied']}, consumo: {group['consumo']}, coste: {group['coste_nuevo']}")

    # VERIFICAR COSTO INICIAL
    initial_cost = player_board.get_population_cost()
    print(f"\nCoste inicial de población: {initial_cost}")

    # VERIFICAR CONSUMO INICIAL
    initial_consumption = player_board.get_food_consumption()
    print(f"Consumo inicial de comida: {initial_consumption}")

    # SIMULAR VACIADO DE GRUPOS
    print("\n--- Simulando vaciado de grupos ---")

    # Vaciar primer grupo (2 fichas)
    for i in range(2):
        success = player_board._take_yellow_token_from_group()
        print(f"Tomar ficha {i+1} del primer grupo: {success}")

    # Verificar que el primer grupo ahora está desocupado
    first_group = player_board.yellow_reserves['groups'][0]
    print(f"Primer grupo después de vaciado: {first_group['tokens']} fichas, ocupado: {first_group['occupied']}")

    # Verificar nuevos costes y consumo
    new_cost = player_board.get_population_cost()
    new_consumption = player_board.get_food_consumption()
    print(f"Nuevo coste de población: {new_cost}")
    print(f"Nuevo consumo de comida: {new_consumption}")

    # VERIFICACIONES
    assert first_group['occupied'] == False, "Primer grupo debería estar desocupado"
    assert first_group['tokens'] == 0, "Primer grupo debería tener 0 fichas"
    assert new_cost != initial_cost, "El coste debería haber cambiado"
    assert new_consumption != initial_consumption, "El consumo debería haber cambiado"

    print("✓ Sistema de grupos amarillos funciona correctamente!")
    return True

def test_blue_reserves_groups():
    """Verifica que las reservas azules funcionen con el sistema de grupos"""
    print("\n=== Test: Sistema de Grupos Azules ===")

    # INICIALIZACIÓN
    player_board = PlayerBoard(player_id=1)

    # ESTADO INICIAL
    print("Estado inicial de grupos azules:")
    for i, group in enumerate(player_board.blue_reserves['groups']):
        print(f"  Grupo {i+1}: {group['tokens']} fichas, ocupado: {group['occupied']}, corrupción: {group['corruption']}")

    # VERIFICAR CORRUPCIÓN INICIAL
    initial_corruption = player_board.get_corruption_penalty()
    print(f"\nCorrupción inicial: {initial_corruption}")

    # SIMULAR TOMA DE FICHAS AZULES
    print("\n--- Simulando toma de fichas azules ---")

    # Tomar 6 fichas del primer grupo
    for i in range(6):
        success = player_board._take_blue_token_from_group()
        print(f"Tomar ficha azul {i+1}: {success}")

    # Verificar que el primer grupo ahora está desocupado
    first_blue_group = player_board.blue_reserves['groups'][0]
    print(f"Primer grupo azul después de vaciado: {first_blue_group['tokens']} fichas, ocupado: {first_blue_group['occupied']}")

    # Verificar nueva corrupción
    new_corruption = player_board.get_corruption_penalty()
    print(f"Nueva corrupción: {new_corruption}")

    # VERIFICACIONES
    assert first_blue_group['occupied'] == False, "Primer grupo azul debería estar desocupado"
    assert first_blue_group['tokens'] == 0, "Primer grupo azul debería tener 0 fichas"
    assert new_corruption != initial_corruption, "La corrupción debería haber cambiado"

    print("✓ Sistema de grupos azules funciona correctamente!")
    return True

def test_turn_completion():
    """Verifica que la finalización de turno funcione correctamente"""
    print("\n=== Test: Finalización de Turno ===")

    # INICIALIZACIÓN
    player_board = PlayerBoard(player_id=1)

    # AÑADIR ALGUNAS MEJORAS DEL TURNO
    player_board.add_technology_researched("Nueva Tecnología")
    player_board.update_cards_in_hand(3)
    player_board.add_civil_action_bonus(1)

    # COMPLETAR TURNO
    turn_summary = player_board.complete_turn()

    print("Resumen del turno:")
    for key, value in turn_summary.items():
        print(f"  {key}: {value}")

    # VERIFICACIONES
    assert 'production' in turn_summary, "Debería incluir producción"
    assert 'technologies_researched' in turn_summary, "Debería incluir tecnologías investigadas"
    assert turn_summary['cards_in_hand'] == 3, "Debería tener 3 cartas en mano"

    # Verificar que las mejoras se resetearon
    assert len(player_board.turn_improvements['technologies_researched']) == 0, "Tecnologías investigadas deberían resetearse"

    print("✓ Finalización de turno funciona correctamente!")
    return True

if __name__ == "__main__":
    try:
        test_yellow_reserves_groups()
        test_blue_reserves_groups()
        test_turn_completion()
        print("\n🎉 ¡Todos los tests del sistema de grupos pasaron!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
