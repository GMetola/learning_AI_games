"""
MAIN execution for Travian IA project
"""

import logging
import numpy as np

import turn_functions
import travian_classes


dorf = travian_classes.Dorf()

class Turn():
    """
    Class to create each of the game turns
    """
    action = 0
    options = []

    def __init__(self, turn_number, points) -> None:
        self.turn_number = turn_number
        self.points = points

    def start_turn(self):
        """Checks possible actions for player"""
        logging.info("Start of turn %s", str(self.turn_number))
        self.options, _ = self.possible_actions()

    def player_action(self, turn_selection):
        """Execute selected action"""
        if turn_selection != 'pass':
            try:
                turn_functions.purchase_improvement(dorf, turn_selection)
            except Exception:
                logging.error("That building was not available.", exc_info=True)

    def end_turn(self):
        """
        Runs triggered endturn actions
        Calculates points gained
        """
        dorf.harvest()
        self.points = self.calculate_points()
        self.turn_number += 1

    def calculate_points(self):
        """Calculates points obtained in a turn"""
        self.points = np.sum(dorf.resources)/1000
        print("Points of turn", self.turn_number, ":", self.points)
        return self.points

    def possible_actions(self):
        """Checks available actions for current player on current turn"""
        possible_actions = []
        action_names = []
        for building in dorf.buildings:
            able = turn_functions.purchasing_power_check(dorf, building)
            if able:
                possible_actions.append(building.impr_id)
                action_names.append(building.name)
        return possible_actions, action_names

    def print_action_options(self):
        """Printer"""
        _, option_names = self.possible_actions()
        for option in option_names:
            print(option)


class Game():
    """
    Uppermost class, contains the game itself
    """
    points = 0
    max_points = 0
    player = None

    def __init__(self) -> None:
        self.turns = 10
        self.player = Player()

    def start_game(self):
        """
        Main function, which will call midgame and endgame.
        """
        logging.info("GAME STARTED !!")
        self.midgame()
        self.endgame()

    def midgame(self):
        """
        Loops the game the number of turns specified
        """
        for turn_number in range(self.turns):
            current_turn = Turn(turn_number, self.points)
            current_turn.start_turn()
            options, _ = current_turn.possible_actions()
            selected = self.player.call(options)
            current_turn.player_action(selected)
            current_turn.end_turn()

            self.points = current_turn.points

            if self.points > self.max_points:
                self.max_points = self.points

    def endgame(self):
        """
        Counts points, declares winner and closes game
        """
        print("Number of turns: ", self.turns)
        print("Final score:", self.points)
        dorf.print_buildings()
        dorf.print_storage()


class Player():
    """
    Creates players who only have random choice selection
    """
    def __init__(self, name="dummie") -> None:
        pass

    def call(self, options):
        """Selects an option among the ones offered."""
        if len(options) is 0:
            choice = 'pass'
        else:
            choice = np.random.choice(options)
            logging.info("I want to build option %s", str(choice))
        return choice

if __name__ == '__main__':
    partida = Game()
    partida.start_game()
