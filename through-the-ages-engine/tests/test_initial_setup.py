#!/usr/bin/env python3
"""
Test para verificar la configuración inicial correcta del juego
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from game.board import PlayerBoard

def test_initial_setup():
    """Verifica que la configuración inicial sea correcta"""
    print("=== Test: Configuración Inicial ===")

    # INICIALIZACIÓN
    player_board = PlayerBoard(player_id=1)    # VERIFICACIÓN TRABAJADORES
    print(f"Trabajadores disponibles: {player_board.yellow_reserves['available_workers']}")

    # VERIFICACIÓN GRUPOS AMARILLOS
    total_in_groups = sum(group['tokens'] for group in player_board.yellow_reserves['groups'])
    print(f"Fichas en grupos amarillos: {total_in_groups}")

    print("Trabajadores asignados:")
    for tech, workers in player_board.yellow_reserves['technology_workers'].items():
        print(f"  {tech}: {workers} trabajadores")

    # VERIFICACIÓN TOTAL
    total_assigned = sum(player_board.yellow_reserves['technology_workers'].values())
    total_available = player_board.yellow_reserves['available_workers']
    total_tokens = total_assigned + total_available + total_in_groups

    print(f"\nTOTAL:")
    print(f"  Asignados: {total_assigned}")
    print(f"  Disponibles: {total_available}")
    print(f"  En grupos: {total_in_groups}")
    print(f"  Total fichas amarillas: {total_tokens}")

    # VERIFICACIÓN RECURSOS
    print(f"\nRECURSOS:")
    for resource, amount in player_board.resources.items():
        print(f"  {resource}: {amount}")    # VERIFICACIÓN TECNOLOGÍAS
    print(f"\nTECNOLOGÍAS:")
    # Show all buildings from the new card manager
    all_buildings = player_board.card_manager.get_all_buildings()
    for building in all_buildings:
        print(f"  {building.name}")

    # Also show government and leader if any
    if player_board.card_manager.get_government():
        print(f"  {player_board.card_manager.get_government().name} (Government)")
    if player_board.card_manager.get_leader():
        print(f"  {player_board.card_manager.get_leader().name} (Leader)")# VERIFICACIONES
    assert total_tokens == 24, f"Total de fichas amarillas debe ser 24, pero es {total_tokens}"
    assert total_assigned == 5, f"Trabajadores asignados deben ser 5, pero son {total_assigned}"
    assert total_available == 1, f"Trabajadores disponibles deben ser 1, pero son {total_available}"
    assert total_in_groups == 18, f"Fichas en grupos debe ser 18, pero son {total_in_groups}"

    print("\n✓ Configuración inicial correcta!")

    return True

def test_worker_assignment():
    """Verifica que la asignación de trabajadores funcione correctamente"""
    print("\n=== Test: Asignación de Trabajadores ===")

    player_board = PlayerBoard(player_id=1)

    # ESTADO INICIAL
    initial_available = player_board.yellow_reserves['available_workers']
    initial_agriculture = player_board.yellow_reserves['technology_workers']['Agriculture']

    print(f"Inicial - Disponibles: {initial_available}, Agriculture: {initial_agriculture}")

    # ASIGNAR TRABAJADOR A AGRICULTURA
    success = player_board.assign_worker_to_building('Agriculture')

    final_available = player_board.yellow_reserves['available_workers']
    final_agriculture = player_board.yellow_reserves['technology_workers']['Agriculture']

    print(f"Final - Disponibles: {final_available}, Agriculture: {final_agriculture}")

    # VERIFICACIONES
    assert success == True, "Debería poder asignar trabajador"
    assert final_available == initial_available - 1, "Trabajadores disponibles deben disminuir en 1"
    assert final_agriculture == initial_agriculture + 1, "Trabajadores en Agriculture deben aumentar en 1"

    print("✓ Asignación de trabajador correcta!")

    # INTENTAR ASIGNAR SIN TRABAJADORES DISPONIBLES
    player_board.yellow_reserves['available_workers'] = 0
    success = player_board.assign_worker_to_building('Bronze')

    assert success == False, "No debería poder asignar trabajador sin disponibles"
    print("✓ Validación sin trabajadores disponibles correcta!")

    return True

if __name__ == "__main__":
    try:
        test_initial_setup()
        test_worker_assignment()
        print("\n🎉 ¡Todos los tests pasaron!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
