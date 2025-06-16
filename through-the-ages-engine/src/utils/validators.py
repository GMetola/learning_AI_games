def validate_card_data(card_data):
    # Validar que los datos de la carta no estén vacíos
    if not card_data.get('Card Name'):
        raise ValueError("El nombre de la carta no puede estar vacío.")

    # Validar que el coste tecnológico y de construcción sean números no negativos
    if card_data.get('Tech cost') < 0:
        raise ValueError("El coste tecnológico no puede ser negativo.")

    if card_data.get('Build cost') < 0:
        raise ValueError("El coste de construcción no puede ser negativo.")

def validate_player_action(action):
    # Validar que la acción del jugador sea válida
    valid_actions = ['build', 'produce', 'gain', 'discard']
    if action not in valid_actions:
        raise ValueError(f"La acción '{action}' no es válida. Acciones válidas: {valid_actions}")

def validate_game_state(game_state):
    # Validar que el estado del juego tenga los atributos necesarios
    required_attributes = ['current_turn', 'players', 'board']
    for attr in required_attributes:
        if attr not in game_state:
            raise ValueError(f"El estado del juego debe contener '{attr}'.")