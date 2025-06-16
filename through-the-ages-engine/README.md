# Through the Ages Engine

This project is a simplified version of the board game "Through the Ages," designed to allow both algorithmic and AI bots to play against each other. The architecture supports future graphical user interfaces and human player interaction.

## Project Structure

- **src/**: Contains the main source code for the game.
  - **game/**: Logic for the game mechanics.
    - `__init__.py`: Initializes the game module.
    - `board.py`: Game board logic.
    - `player.py`: Player class and management.
    - `cards.py`: Card mechanics and interactions.
    - `actions.py`: Player actions management.
    - `game_state.py`: Overall game state management.
  - **bots/**: Implementations of different bot types.
    - `__init__.py`: Initializes the bots module.
    - `base_bot.py`: Base class for bots.
    - `algorithmic_bot.py`: Algorithmic bot implementation.
    - `ai_bot.py`: AI bot implementation.
  - **api/**: Interfaces for game interaction.
    - `__init__.py`: Initializes the API module.
    - `game_api.py`: Game interaction interface.
    - `bot_interface.py`: Bot communication interface.
  - **database/**: Database management.
    - `__init__.py`: Initializes the database module.
    - `models.py`: Data models for game data.
    - `connection.py`: Database connection management.
  - **ui/**: User interface components.
    - `__init__.py`: Initializes the UI module.
    - `console_ui.py`: Console-based UI for human players.
    - `web_ui.py`: Web-based UI for future graphical interaction.
  - **utils/**: Utility functions and loaders.
    - `__init__.py`: Initializes the utilities module.
    - `card_loader.py`: Loads card data from CSV files.
    - `validators.py`: Validation functions for game data.

- **data/**: Contains game data files.
  - `cards.csv`: Card definitions and attributes.
  - `config.json`: Configuration settings for the game.

- **tests/**: Unit tests for the project.
  - `test_game.py`: Tests for game logic.
  - `test_bots.py`: Tests for bot implementations.
  - `test_api.py`: Tests for API functionality.

- **requirements.txt**: Lists project dependencies.

- **setup.py**: Packaging and dependency management.

## Getting Started

1. **Installation**: Clone the repository and install the required dependencies listed in `requirements.txt`.
2. **Running the Game**: Use the console UI or the web UI to start a game. You can choose to play against bots or other human players.
3. **Extending the Project**: You can add new bot strategies, modify game rules, or enhance the UI as needed.

## Future Work

- Develop a graphical user interface for better user experience.
- Implement more advanced AI strategies for bots.
- Expand the game mechanics and card interactions.

## License

This project is licensed under the MIT License. See the LICENSE file for details.