"""
Turn functions to make the game run.
"""
import logging

def purchasing_power_check(dorf, improvement):
    """Checks if the town has enough resources to buy the improvement"""
    resources = dorf.resources
    costs = improvement.cost
    # TODO: divide requirement per resource type
    if (resources > costs).all():
        able = True
    else:
        able = False
    return able

def purchase_improvement(dorf, improvement_id) -> None:
    """Main function to buy an improvement"""
    improved_building = dorf.buildings[improvement_id -1]  # indexation starts in 0
    if not purchasing_power_check(dorf, improved_building):
        return
    dorf.reduce_storage(improved_building.cost)
    improved_building.upgrade()
    print(f"{improved_building.name} upgraded to level {improved_building.level}!")


def consistency_check(dorf):
    assert dorf.positive_storage_check()
