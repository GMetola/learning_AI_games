from typing import Dict

class Player:
    def __init__(self, name):
        # Inicializa el jugador con un nombre y atributos básicos
        self.name = name
        self.player_id = None  # Se asignará desde el tablero
        self.board = None      # Referencia al tablero individual del jugador (PlayerBoard)

        # Recursos temporales (DEPRECATED - usar self.board.resources)
        self.resources = {
            'food': 0,
            'culture': 0,
            'science': 0,
            'strength': 0,
            'happy': 0,
            'military': 0
        }
        self.cards = []
        self.actions = []

    def set_board(self, player_board):
        """Asigna el tablero individual del jugador

        Args:
            player_board (PlayerBoard): Tablero individual del jugador
        """
        self.board = player_board
        # Sincroniza recursos iniciales con el tablero
        self.resources = self.board.resources.copy()

    def gain_resources(self, food=0, culture=0, science=0, strength=0, happy=0, military=0):
        """Aumenta los recursos del jugador

        NOTA: Se actualiza tanto el Player como el PlayerBoard
        """
        if self.board:
            # Actualiza el tablero individual (fuente de verdad)
            self.board.resources['food'] += food
            self.board.resources['culture'] += culture
            self.board.resources['science'] += science
            self.board.resources['strength'] += strength
            self.board.resources['happy'] += happy
            # Sincroniza recursos locales
            self.resources = self.board.resources.copy()
        else:
            # Fallback si no hay tablero asignado
            self.resources['food'] += food
            self.resources['culture'] += culture
            self.resources['science'] += science
            self.resources['strength'] += strength
            self.resources['happy'] += happy
            self.resources['military'] += military

    def play_card(self, card):
        # Juega una carta y la añade a la mano del jugador
        self.cards.append(card)
        # Aquí se pueden añadir más lógicas relacionadas con la carta

    def take_action(self, action):
        # Realiza una acción y la añade a la lista de acciones del jugador
        self.actions.append(action)
        # Aquí se pueden añadir más lógicas relacionadas con la acción

    def get_production_per_turn(self) -> Dict[str, int]:
        """Obtiene la producción por turno del jugador

        Returns:
            Dict[str, int]: Recursos producidos por turno
        """
        if self.board:
            return self.board.calculate_production()
        return {}

    def get_worker_assignments(self) -> Dict[str, int]:
        """Obtiene asignaciones de trabajadores

        Returns:
            Dict[str, int]: Trabajadores por tecnología
        """
        if self.board:
            return self.board.yellow_reserves['technology_workers']
        return {}

    def get_available_workers(self) -> int:
        """Obtiene número de trabajadores disponibles

        Returns:
            int: Trabajadores sin asignar
        """
        if self.board:
            return self.board.yellow_reserves['available_workers']
        return 0

    def check_happiness_status(self) -> Dict[str, any]:
        """Verifica estado de felicidad y posibles revueltas

        Returns:
            Dict: Estado de felicidad
        """
        if self.board:
            revolt = self.board.check_revolt_condition()
            happiness = self.board.indicators['happiness']
            unemployed = self.get_available_workers()

            return {
                'happiness_points': happiness,
                'unemployed_workers': unemployed,
                'revolt_risk': revolt,
                'status': 'REVUELTA' if revolt else 'ESTABLE'
            }
        return {'status': 'NO_DISPONIBLE'}

    def get_board_summary(self) -> Dict:
        """Obtiene resumen completo del tablero del jugador

        Returns:
            Dict: Resumen del estado del jugador
        """
        if self.board:
            summary = self.board.get_status_summary()
            summary['happiness_status'] = self.check_happiness_status()
            summary['available_workers'] = self.get_available_workers()
            return summary
        return {}

    def __str__(self):
        # Representación del jugador
        return f"Jugador: {self.name}, Recursos: {self.resources}, Cartas: {len(self.cards)}, Acciones: {len(self.actions)}"