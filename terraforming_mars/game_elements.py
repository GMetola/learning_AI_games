"""
    A general list of elements in the game. I will organize and subdivide later.
"""
RESOURCES = ['megacredits', 'steel', 'titanium', 'plants', 'energy', 'heat']
STANDARD_PJ = ['sell patent', 'power plant', 'asteroid', 'aquifier', 'greenery',' city']

class game_elem():
    def __init__(self, name, cost) -> None:
        self.name = name
        self.cost = cost

## RESOURCES


class Action():
    def __init__(self) -> None:
        pass
    pass

class Card(game_elem):
    def __init__(self, 
                name, cost,
                requirements={},
                consequences={}
                ) -> None:
        super().__init__(name, cost)
        self.playable = False
        self.requirements = requirements
        self.consequences = consequences


class Resource(game_elem):
    def __init__(self, name) -> None:
        self.name = name
        self.qty = 0
        self.terraformable = self.name in ['plant', 'heat']
        self.convertible = self.name in ['steel', 'titanium', 'energy']


class Player():
    def __init__(self) -> None:
        self.corporation = 'basic'
        self.vict_points = 0
        self.terr_points = 20
        self.resources = dict.fromkeys(RESOURCES, 0)
        self.res_production = dict.fromkeys(RESOURCES, 0)
        
        # turn
        self.turn_active = False
        self.actions_left = 2
        self.log = []
    pass


class Milestones_and_Awards():
    def __init__(self, name, cost) -> None:
        self.name = name
        self.cost = cost
        self.owner = None
        self.aspirant_ranking = []  # list of players by order
        self.activated = False


class StandardProject():
    def __init__(self) -> None:
        pass
    pass


class Awards():
    def __init__(self) -> None:
        pass
    pass


## MARS

class Mars():
    def __init__(self) -> None:
        pass
    pass


class TerraformElement():
    def __init__(self, name, max, min, step) -> None:
        self.name = name
        self.max = max
        self.min = min
        self.step = step

    pass


class Tile():
    def __init__(self) -> None:
        pass
    pass


## GAME PHASES

class SetupGame():
    def __init__(self) -> None:
        pass
    pass


class Turn():
    def __init__(self) -> None:
        pass
    pass


class EndGame():
    def __init__(self) -> None:
        pass
    pass

