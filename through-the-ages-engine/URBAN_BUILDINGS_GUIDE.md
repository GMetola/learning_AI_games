# Urban Building Creation and Management Guide

## Overview

Urban buildings in the Through the Ages engine are special building cards that provide culture, happiness, and sometimes science production. They inherit from the `Building` class, which provides worker management functionality.

## Class Hierarchy

```
Card (base)
└── CivilCard
    └── Technology
        └── Building
            └── UrbanBuilding
```

## Urban Building Attributes

An `UrbanBuilding` object has these key attributes:

- **name**: Building name (e.g., "Theater", "Library")
- **building_type**: Type category ("Theater", "Arena", "Library", "Temple", "Lab")
- **age**: Game age ("I", "II", "III")
- **tech_cost**: Science cost to research the technology
- **build_cost**: Material cost to build the building
- **production**: Dict of resources produced per turn (e.g., `{'culture': 2, 'happy': 1}`)
- **gain**: Dict of one-time resources gained when built (e.g., `{'science': 2}`)
- **workers**: List of worker tokens assigned to this building
- **max_workers**: Maximum number of workers (typically 2)

## How to Create Urban Buildings

### Method 1: Load from CSV Data (Recommended)

```python
from game.card_loader import CardLoader

loader = CardLoader()

# Get a specific urban building by name
theater_card = loader.get_card_by_name("Drama")
if theater_card:
    print(f"Loaded: {theater_card}")
    print(f"Production: {theater_card.production}")

# Get all urban buildings
all_urban_buildings = loader.get_urban_buildings()
print(f"Found {len(all_urban_buildings)} urban buildings")
```

### Method 2: Create Manually

```python
from game.card_classes import UrbanBuilding

custom_library = UrbanBuilding(
    name="Advanced Library",
    building_type="Library",
    age="II",
    tech_cost=5,
    build_cost=7,
    production={'science': 2, 'culture': 2},
    gain={'science': 3},  # One-time bonus when built
    card_text="An advanced library with better research facilities"
)
```

## How to Add Urban Buildings to Player Board

The enhanced `add_urban_building` method supports multiple input types and includes validation:

### Method 1: Add Card Object

```python
# Assuming you have a player_board and a building card
player_board.add_urban_building(theater_card)
```

### Method 2: Add by Name (String)

```python
# The method will automatically load the card from CSV
player_board.add_urban_building("Printing Press")
```

### Method 3: Add Custom Building

```python
custom_theater = UrbanBuilding(
    name="Custom Theater",
    building_type="Theater",
    age="I",
    tech_cost=4,
    build_cost=5,
    production={'culture': 2, 'happy': 1}
)

player_board.add_urban_building(custom_theater)
```

## Error Handling

The `add_urban_building` method includes comprehensive error checking:

```python
try:
    player_board.add_urban_building("Nonexistent Building")
except ValueError as e:
    print(f"Error: {e}")  # "Card 'Nonexistent Building' not found"

try:
    player_board.add_urban_building("Agriculture")  # This is a production building
except ValueError as e:
    print(f"Error: {e}")  # "Card 'Agriculture' is not an UrbanBuilding"

try:
    player_board.add_urban_building("Drama")  # Add same building twice
    player_board.add_urban_building("Drama")
except ValueError as e:
    print(f"Error: {e}")  # "Urban building 'Drama' already exists on this board"
```

## Available Urban Building Types

The game includes these urban building categories:

1. **Temples**: Provide culture and happiness (Religion, Theology, Organized Religion)
2. **Labs**: Provide science (Alchemy, Scientific Method, Computers)
3. **Arenas**: Provide strength and happiness (Bread and Circuses, Team Sports, Professional Sports)
4. **Libraries**: Provide culture and science (Printing Press, Journalism, Multimedia)
5. **Theaters**: Provide culture and happiness (Drama, Opera, Movies)

## Working with Workers

Urban buildings can have workers assigned to them:

```python
building.assign_worker("worker_1")

# Get worker count
worker_count = building.get_worker_count()

# Remove a worker
building.remove_worker("worker_1")
```

## Integration with Game System

Urban buildings are tracked in the new modular system:

1. **player_board.card_manager.urban_buildings**: List of UrbanBuilding objects
2. **player_board.card_manager.has_technology(name)**: Check if player has a specific card/technology
3. **player_board.yellow_reserves['technology_workers']**: Worker assignments

## Example: Complete Urban Building Setup

```python
from game.card_loader import CardLoader
from game.card_classes import UrbanBuilding
from game.board import GameBoard
from game.player import Player

# Setup game board and player
game_board = GameBoard(1)
player = Player("TestPlayer")
player.player_id = 1
player_board = game_board.player_boards[1]
player.set_board(player_board)

# Load and add urban buildings
loader = CardLoader()

# Add existing buildings
player_board.add_urban_building("Drama")
player_board.add_urban_building("Printing Press")

# Add custom building
custom_arena = UrbanBuilding(
    name="Grand Arena",
    building_type="Arena",
    age="II",
    tech_cost=6,
    build_cost=8,
    production={'strength': 2, 'happy': 3},
    card_text="A magnificent arena for grand spectacles"
)
player_board.add_urban_building(custom_arena)

# Show results
print(f"Urban buildings: {len(player_board.urban_buildings)}")
for building in player_board.urban_buildings:
    workers = player_board.yellow_reserves['technology_workers'].get(building.name, 0)
    print(f"  {building.name} ({building.building_type}) - {workers} workers")
    print(f"    Production: {building.production}")
```

This system provides a robust and flexible way to create and manage urban buildings in the Through the Ages engine!
