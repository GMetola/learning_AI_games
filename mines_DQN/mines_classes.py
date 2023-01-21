"""
Classes needed for the basic game
"""
import numpy as np  # TODO: evolve numpy arrays to tensors
import pygame


class Dorf():
    """
    Class to create villages.
    """

    # ABSOLUTE VALUES
    resource_list = ["wood","clay","iron","wheat"]
    num_resources = len(resource_list)
    storage = 2000
    resources = np.ones((1,num_resources))
    BUILDING_AMOUNT = 0
    imp_costs =   np.array([[1, 100, 100, 100],
                            [100, 1, 100, 100],
                            [100, 100, 1, 100],
                            [100, 100, 100, 1]])
    imp_growths = np.array([100, 200, 400, 600])

    def __init__(self, starting_resources=800, starting_production = 10) -> None:
        self.production = [starting_production]*len(self.resource_list)
        self.starting_resources = starting_resources

        self.reset_dorf()

    def reset_dorf(self):
        """Sets all attributes to their initial value"""

        woodcutter = Improvement(0, 'Woodcutter', self.imp_costs[0], self.imp_growths)
        clay_pit = Improvement(1, 'Clay Pit', self.imp_costs[1], self.imp_growths)
        iron_mine = Improvement(2, 'Iron Mine', self.imp_costs[2], self.imp_growths)
        crop = Improvement(3, 'Crop', self.imp_costs[3], self.imp_growths)

        self.buildings = [woodcutter, clay_pit, iron_mine, crop]
        self.building_levels = np.array([woodcutter.level,
                                        clay_pit.level,
                                        iron_mine.level,
                                        crop.level])

        self.resources = (self.resources * 0) + self.starting_resources

    def reduce_storage(self, costs) -> None:
        """Update materials after purchase"""
        self.resources -= costs

    def harvest(self):
        """Increase materials after turn end"""
        self.resources += self.production

    def check_positive_storage(self):
        """Test storage is positive"""
        return (self.resources > -1).all()

    def print_storage(self):
        """Print current materials"""
        for name,value in zip(self.resource_list, self.resources):
            print(name, ": ", value)

    def print_buildings(self):
        """Buildings built in village"""
        levels = []
        for building in self.buildings:
            levels.append(building.level)
        print("\nBuilding levels: ", levels)

    def print_building_details(self):
        """Buildings built in village"""
        print("\nBuildings in Dorf: ")
        for building in self.buildings:
            building.print_detail_info()

    def check_purchasing_power(self, improvement_id):
        """Checks if the town has enough resources to buy the improvement"""
        improvement = self.buildings[improvement_id -1]  # indexation starts in 0
        resources = self.resources
        costs = improvement.cost
        # TODO: divide requirement per resource type
        if (resources > costs).all():
            able = True
        else:
            able = False
        return able

    def purchase_improvement(self, improvement_id) -> None:
        """Main function to buy an improvement"""
        if not self.check_purchasing_power(improvement_id):
            return
        improved_building = self.buildings[improvement_id -1]  # indexation starts in 0
        self.reduce_storage(improved_building.cost)
        improved_building.upgrade()
        print(f"{improved_building.name} upgraded to level {improved_building.level}!")


class Improvement():
    """Class to create buildings to improve the village"""
    level = int(1)

    def __init__(self, index, name, cost, growth) -> None:
        self.name = name
        self.impr_id = index
        self.base_cost = cost
        self.cost = cost
        self.growth = growth
        self.production = self.growth * self.level

    def upgrade(self):
        """Level building up"""
        self.level += 1
        self.cost = self.base_cost * self.level
        self.production = self.growth * self.level

    def print_basic_info(self):
        """Print building info"""
        print(f"{self.name} (level {self.level})")

    def print_detail_info(self):
        """Print building info"""
        print("Building info:")
        print(f"{self.name} (level {self.level}) - Production: {self.production}")
        next_level_prod = self.production/self.level*(self.level+1)
        print(f"Next level -- Cost: {self.cost} -- Production: {next_level_prod}\n")


class Game:
    """ Initialize PyGAME """

    def __init__(self) -> None:
        pygame.display.set_caption('Travian_DeepQNetwork')
        self.window_size = 600


if __name__ == '__main__':
    d = Dorf()

    d.print_buildings()

    d.print_buildings()

    d.print_buildings()
