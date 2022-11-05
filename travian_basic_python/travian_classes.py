"""
Classes needed for the basic game
"""
import numpy as np  # TODO: evolve numpy arrays to tensors

BUILDING_AMOUNT = 0

class Dorf():
    """
    Class to create villages.
    """
    resource_list = ["wood","clay","iron","wheat"]
    storage = 2000
    resources = np.ones((1,len(resource_list)))
    BUILDING_AMOUNT = 0
    def __init__(self, starting_resources=800, starting_production = 10) -> None:
        self.production = [starting_production]*len(self.resource_list)


        # Improvements
        imp_costs =   np.array([[1, 100, 100, 100],
                                [100, 1, 100, 100],
                                [100, 100, 1, 100],
                                [100, 100, 100, 1]])
        woodcutter = Improvement('Woodcutter', imp_costs[0], 100)
        clay_pit = Improvement('Clay Pit', imp_costs[1], 200)
        iron_mine = Improvement('Iron Mine', imp_costs[2], 400)
        crop = Improvement('Crop', imp_costs[3], 600)

        self.buildings = [woodcutter, clay_pit, iron_mine, crop]
        self.building_levels = np.array([woodcutter.level,
                                        clay_pit.level,
                                        iron_mine.level,
                                        crop.level])

        self.resources *= starting_resources

    def reduce_storage(self, costs) -> None:
        """Update materials after purchase"""
        self.resources -= costs

    def harvest(self):
        """Increase materials after turn end"""
        self.resources += self.production

    def positive_storage_check(self):
        """Test storage is positive"""
        return (self.resources > -1).all()

    def print_storage(self):
        """Print current materials"""
        for name,value in zip(self.resource_list, self.resources):
            print(name, ": ", value)

    def print_buildings(self):
        """Buildings built in village"""
        print("\nBuildings in Dorf: ")
        for building in self.buildings:
            building.print_info()


class Improvement():
    """Class to create buildings to improve the village"""
    level = 1

    def __init__(self, name, cost, growth) -> None:
        global BUILDING_AMOUNT
        self.name = name
        self.impr_id = BUILDING_AMOUNT + 1
        BUILDING_AMOUNT += 1
        self.base_cost = cost
        self.cost = cost
        self.growth = growth
        self.production = self.growth * self.level

    def upgrade(self):
        """Level building up"""
        self.level += 1
        self.cost = self.base_cost * self.level
        self.production = self.growth * self.level

    def print_info(self):
        """Print building info"""
        print("Building info:")
        print(f"{self.name} (level {self.level}) - Production: {self.production}")
        next_level_prod = self.production/self.level*(self.level+1)
        print(f"Next level -- Cost: {self.cost} -- Production: {next_level_prod}\n")



if __name__ == '__main__':
    d = Dorf()

    d.print_buildings()

    d.print_buildings()

    d.print_buildings()
