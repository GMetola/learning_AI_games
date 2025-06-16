class BotInterface:
    def __init__(self, bot_name):
        self.bot_name = bot_name

    def make_move(self, game_state):
        """
        Método para que el bot realice un movimiento basado en el estado del juego.
        :param game_state: El estado actual del juego.
        :return: Acción que el bot desea realizar.
        """
        raise NotImplementedError("Este método debe ser implementado por los bots específicos.")

    def receive_feedback(self, feedback):
        """
        Método para recibir retroalimentación sobre la acción realizada.
        :param feedback: Retroalimentación sobre el movimiento realizado.
        """
        pass

    def get_bot_name(self):
        """
        Método para obtener el nombre del bot.
        :return: Nombre del bot.
        """
        return self.bot_name