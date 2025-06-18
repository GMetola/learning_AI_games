#!/usr/bin/env python3
"""
Utilidades para pruebas del juego Through the Ages
Funciones auxiliares para configurar estados de prueba
"""

def set_max_happiness(player_board):
    """Establece la felicidad al máximo para evitar revueltas durante las pruebas

    Args:
        player_board (PlayerBoard): Tablero del jugador a modificar
    """
    # CONFIGURACIÓN FELICIDAD MÁXIMA
    # Establece felicidad suficiente para evitar revueltas
    max_workers = player_board.yellow_reserves['total_tokens']
    player_board.resources["happy"] = max_workers + 5  # Margen extra de seguridad

    print(f"🔧 TEST UTILITY: Felicidad establecida a {player_board.resources['happy']} para evitar revueltas")

def prevent_revolt_for_testing(player_board):
    """Previene revueltas durante las pruebas ajustando felicidad

    Args:
        player_board (PlayerBoard): Tablero del jugador
    """
    available_workers = player_board.yellow_reserves['available_workers']
    current_happiness = player_board.resources["happy"]

    if available_workers > current_happiness:
        # AJUSTE TEMPORAL
        # Aumenta felicidad para superar trabajadores disponibles
        player_board.resources["happy"] = available_workers + 2
        print(f"🔧 TEST UTILITY: Felicidad ajustada de {current_happiness} a {player_board.resources['happy']}")
        print(f"   Trabajadores disponibles: {available_workers}, Nueva felicidad: {player_board.resources['happy']}")
    else:
        print(f"✓ No se necesita ajuste: Trabajadores {available_workers} <= Felicidad {current_happiness}")

def reset_happiness_to_default(player_board):
    """Restablece la felicidad a valores por defecto del juego

    Args:
        player_board (PlayerBoard): Tablero del jugador
    """
    player_board.resources["happy"] = 1  # Valor inicial del juego
    print(f"🔄 TEST UTILITY: Felicidad restablecida a valor por defecto: 1")

def setup_production_test_state(player_board):
    """Configura estado óptimo para probar producción sin revueltas

    Args:
        player_board (PlayerBoard): Tablero del jugador
    """
    # CONFIGURACIÓN ESTADO PRODUCCIÓN
    # Asigna trabajadores a todas las tecnologías iniciales
    initial_technologies = ['Agriculture', 'Bronze', 'Filosofía', 'Religión']

    print("🔧 TEST UTILITY: Configurando estado para pruebas de producción...")    # Asigna un trabajador a cada tecnología
    for tech in initial_technologies:
        if (player_board.yellow_reserves['available_workers'] > 0 and
            player_board.has_technology(tech)):
            player_board.assign_worker_to_building(tech)
            print(f"   ✓ Trabajador asignado a {tech}")

    # PREVENCIÓN REVUELTAS
    # Ajusta felicidad si es necesario
    prevent_revolt_for_testing(player_board)

    print(f"   Estado final: {player_board.yellow_reserves['available_workers']} trabajadores disponibles")
    print(f"   Felicidad: {player_board.resources['happy']}")
    print(f"   Asignaciones: {player_board.yellow_reserves['technology_workers']}")

def verify_no_revolt(player_board):
    """Verifica que no hay condiciones de revuelta

    Args:
        player_board (PlayerBoard): Tablero del jugador

    Returns:
        bool: True si no hay revuelta, False si hay revuelta
    """
    revolt_condition = player_board.check_revolt_condition()
    available_workers = player_board.yellow_reserves['available_workers']
    happiness = player_board.resources["happy"]

    if revolt_condition:
        print(f"⚠️  REVUELTA DETECTADA: {available_workers} trabajadores > {happiness} felicidad")
        return False
    else:
        print(f"✓ Sin revuelta: {available_workers} trabajadores <= {happiness} felicidad")
        return True
