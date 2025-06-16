"""
Simulation Controller for automated bot vs bot games
"""

import logging
import time
from typing import List, Dict, Any, Optional
from game.game_state import GameState
from game.actions import ActionValidator, ActionExecutor, GameAction
from bots.base_bot import BaseBot, BotManager
from bots.algorithmic_bot import AlgorithmicBot


class SimulationController:
    """Controls automated simulations between bots"""

    def __init__(self):
        """Initialize the simulation controller"""
        self.bot_manager = BotManager()
        self.current_games = {}
        self.simulation_stats = {
            'games_played': 0,
            'total_turns': 0,
            'average_game_length': 0,
            'bot_performance': {}
        }

    def create_bot_vs_bot_game(self, bot1_type: str, bot2_type: str,
                              bot1_difficulty: str = "medium",
                              bot2_difficulty: str = "medium") -> str:
        """Create a new bot vs bot game

        Args:
            bot1_type (str): Type of first bot
            bot2_type (str): Type of second bot
            bot1_difficulty (str): Difficulty of first bot
            bot2_difficulty (str): Difficulty of second bot

        Returns:
            str: Game session ID
        """
        # Generate unique game ID
        game_id = f"sim_{int(time.time())}"

        # Create bots
        bot1 = self.bot_manager.create_bot_instance(
            bot1_type, f"{game_id}_bot1", f"Bot1_{bot1_type}", bot1_difficulty
        )
        bot2 = self.bot_manager.create_bot_instance(
            bot2_type, f"{game_id}_bot2", f"Bot2_{bot2_type}", bot2_difficulty
        )

        # Set player IDs
        if hasattr(bot1, 'set_player_id'):
            bot1.set_player_id(1)
        if hasattr(bot2, 'set_player_id'):
            bot2.set_player_id(2)

        # Initialize game state
        game_state = GameState()
        players = [bot1.name, bot2.name]
        bot_types = [bot1_type, bot2_type]
        game_state.initialize_game(players, bot_types)

        # Store game info
        self.current_games[game_id] = {
            'game_state': game_state,
            'bots': [bot1, bot2],
            'turn_count': 0,
            'start_time': time.time(),
            'winner': None,
            'game_log': []
        }

        logging.info(f"Created bot vs bot game {game_id}: {bot1.name} vs {bot2.name}")
        return game_id

    def simulate_single_game(self, bot1_type: str, bot2_type: str,
                           bot1_difficulty: str = "medium",
                           bot2_difficulty: str = "medium",
                           max_turns: int = 100,
                           verbose: bool = False) -> Dict[str, Any]:
        """Simulate a complete game between two bots

        Args:
            bot1_type (str): Type of first bot
            bot2_type (str): Type of second bot
            bot1_difficulty (str): Difficulty of first bot
            bot2_difficulty (str): Difficulty of second bot
            max_turns (int): Maximum turns before declaring draw
            verbose (bool): Whether to log detailed game progress

        Returns:
            Dict: Game results and statistics
        """
        game_id = self.create_bot_vs_bot_game(bot1_type, bot2_type, bot1_difficulty, bot2_difficulty)

        try:
            return self._run_game_simulation(game_id, max_turns, verbose)
        finally:
            # Clean up
            if game_id in self.current_games:
                del self.current_games[game_id]

    def _run_game_simulation(self, game_id: str, max_turns: int, verbose: bool) -> Dict[str, Any]:
        """Run the actual game simulation"""
        game_info = self.current_games[game_id]
        game_state = game_info['game_state']
        bots = game_info['bots']

        validator = ActionValidator(game_state)
        executor = ActionExecutor(game_state, bots)

        turn_count = 0
        game_log = []

        while not game_state.is_game_over() and turn_count < max_turns:
            current_player_idx = game_state.current_turn
            current_bot = bots[current_player_idx]

            if verbose:
                logging.info(f"Turn {turn_count + 1}: {current_bot.name} {current_bot.civil_actions_left} civil actions left")

            try:
                # Get available actions
                available_actions = validator.get_legal_actions(current_bot.player_id or current_player_idx + 1)

                if not available_actions:
                    logging.warning(f"No available actions for {current_bot.name}, ending turn")
                    game_state.next_turn()
                    continue

                # Bot makes decision
                selected_action_dict = current_bot.make_move(game_state, available_actions)

                # Convert dict to GameAction if needed
                if isinstance(selected_action_dict, dict):
                    # Find matching GameAction
                    selected_action = None
                    for action in available_actions:
                        if (action.action_type == selected_action_dict.get('type') and
                            action.parameters == selected_action_dict.get('parameters', {})):
                            selected_action = action
                            break

                    if not selected_action:
                        # Fallback: create end turn action
                        from game.actions import ActionFactory
                        selected_action = ActionFactory.create_end_turn_action(current_player_idx + 1)
                else:
                    selected_action = selected_action_dict                # Execute action
                result = executor.execute_action(selected_action, current_bot)

                # Log action
                action_log = {
                    'turn': turn_count + 1,
                    'player': current_bot.name,
                    'action': selected_action.action_type,
                    'success': result.get('success', False),
                    'details': result
                }
                game_log.append(action_log)

                if verbose:
                    logging.info(f"Action: {selected_action.action_type} - Success: {action_log['success']}")
                if selected_action.action_type == 'terminar_turno':
                    # Reset action counters for next turn
                    next_player_idx = game_state.current_turn
                    if next_player_idx < len(bots):
                        bots[next_player_idx].reset_actions_for_turn()
                    turn_count += 1
                elif not result.get('success', False):
                    # If action failed, still advance turn to prevent infinite loops
                    game_state.next_turn()
                    # Reset action counters for next player
                    next_player_idx = game_state.current_turn
                    if next_player_idx < len(bots):
                        bots[next_player_idx].reset_actions_for_turn()
                    turn_count += 1
            except Exception as e:
                logging.error(f"Error during {current_bot.name}'s turn: {e}")
                game_state.next_turn()
                # Reset action counters for next player
                next_player_idx = game_state.current_turn
                if next_player_idx < len(bots):
                    bots[next_player_idx].reset_actions_for_turn()
                turn_count += 1

        # Determine winner
        winner = self._determine_winner(game_state)

        # Update statistics
        self._update_simulation_stats(game_info, winner, turn_count)

        # Compile results
        results = {
            'game_id': game_id,
            'winner': winner,
            'turns': turn_count,
            'game_log': game_log,
            'final_scores': self._get_final_scores(game_state),
            'game_over_reason': 'max_turns' if turn_count >= max_turns else 'normal',
            'duration': time.time() - game_info['start_time']
        }

        if verbose:
            logging.info(f"Game {game_id} completed - Winner: {winner}, Turns: {turn_count}")

        return results

    def _determine_winner(self, game_state: GameState) -> Optional[str]:
        """Determine the winner based on final game state"""
        if not game_state.players:
            return None

        # Simple winner determination: highest culture score
        best_score = -1
        winner = None

        for player in game_state.players:
            culture_score = player.board.resources.get('culture', 0)
            if culture_score > best_score:
                best_score = culture_score
                winner = player.name

        return winner

    def _get_final_scores(self, game_state: GameState) -> Dict[str, int]:
        """Get final scores for all players"""
        scores = {}
        for player in game_state.players:
            scores[player.name] = player.board.resources.get('culture', 0)
        return scores

    def _update_simulation_stats(self, game_info: Dict, winner: str, turn_count: int):
        """Update overall simulation statistics"""
        self.simulation_stats['games_played'] += 1
        self.simulation_stats['total_turns'] += turn_count
        self.simulation_stats['average_game_length'] = (
            self.simulation_stats['total_turns'] / self.simulation_stats['games_played']
        )

        # Update bot performance
        for bot in game_info['bots']:
            bot_name = bot.name
            if bot_name not in self.simulation_stats['bot_performance']:
                self.simulation_stats['bot_performance'][bot_name] = {
                    'games_played': 0,
                    'games_won': 0,
                    'win_rate': 0.0
                }

            stats = self.simulation_stats['bot_performance'][bot_name]
            stats['games_played'] += 1

            if winner == bot_name:
                stats['games_won'] += 1

            stats['win_rate'] = stats['games_won'] / stats['games_played']

    def run_tournament(self, bot_configs: List[Dict],
                      games_per_matchup: int = 5,
                      verbose: bool = False) -> Dict[str, Any]:
        """Run a tournament with multiple bots

        Args:
            bot_configs (List[Dict]): List of bot configurations
            games_per_matchup (int): Number of games per bot pair
            verbose (bool): Whether to log detailed progress

        Returns:
            Dict: Tournament results
        """
        tournament_results = {
            'participants': bot_configs,
            'matchups': [],
            'leaderboard': [],
            'total_games': 0
        }

        # Run all matchups
        for i, bot1_config in enumerate(bot_configs):
            for j, bot2_config in enumerate(bot_configs):
                if i >= j:  # Avoid duplicate matchups and self-play
                    continue

                if verbose:
                    logging.info(f"Matchup: {bot1_config} vs {bot2_config}")

                matchup_results = {
                    'bot1': bot1_config,
                    'bot2': bot2_config,
                    'games': [],
                    'bot1_wins': 0,
                    'bot2_wins': 0,
                    'draws': 0
                }

                # Play multiple games
                for game_num in range(games_per_matchup):
                    result = self.simulate_single_game(
                        bot1_config['type'], bot2_config['type'],
                        bot1_config.get('difficulty', 'medium'),
                        bot2_config.get('difficulty', 'medium'),
                        verbose=False
                    )

                    matchup_results['games'].append(result)
                    tournament_results['total_games'] += 1

                    # Track wins
                    winner = result['winner']
                    if winner and bot1_config['type'] in winner:
                        matchup_results['bot1_wins'] += 1
                    elif winner and bot2_config['type'] in winner:
                        matchup_results['bot2_wins'] += 1
                    else:
                        matchup_results['draws'] += 1

                tournament_results['matchups'].append(matchup_results)

        # Calculate leaderboard
        tournament_results['leaderboard'] = self._calculate_leaderboard(tournament_results)

        if verbose:
            logging.info(f"Tournament completed: {tournament_results['total_games']} games played")

        return tournament_results

    def _calculate_leaderboard(self, tournament_results: Dict) -> List[Dict]:
        """Calculate tournament leaderboard"""
        bot_scores = {}

        for matchup in tournament_results['matchups']:
            bot1_type = matchup['bot1']['type']
            bot2_type = matchup['bot2']['type']

            # Initialize if not exists
            if bot1_type not in bot_scores:
                bot_scores[bot1_type] = {'wins': 0, 'games': 0, 'points': 0}
            if bot2_type not in bot_scores:
                bot_scores[bot2_type] = {'wins': 0, 'games': 0, 'points': 0}

            # Add games
            games_in_matchup = len(matchup['games'])
            bot_scores[bot1_type]['games'] += games_in_matchup
            bot_scores[bot2_type]['games'] += games_in_matchup

            # Add wins and points (3 for win, 1 for draw)
            bot_scores[bot1_type]['wins'] += matchup['bot1_wins']
            bot_scores[bot1_type]['points'] += matchup['bot1_wins'] * 3 + matchup['draws']

            bot_scores[bot2_type]['wins'] += matchup['bot2_wins']
            bot_scores[bot2_type]['points'] += matchup['bot2_wins'] * 3 + matchup['draws']

        # Create leaderboard
        leaderboard = []
        for bot_type, stats in bot_scores.items():
            leaderboard.append({
                'bot_type': bot_type,
                'points': stats['points'],
                'wins': stats['wins'],
                'games': stats['games'],
                'win_rate': stats['wins'] / stats['games'] if stats['games'] > 0 else 0
            })

        # Sort by points descending
        leaderboard.sort(key=lambda x: x['points'], reverse=True)

        return leaderboard

    def get_simulation_stats(self) -> Dict[str, Any]:
        """Get current simulation statistics"""
        return self.simulation_stats.copy()


def main():
    """Example usage of SimulationController"""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    controller = SimulationController()

    # Example 1: Single game simulation
    print("Running single game simulation...")
    result = controller.simulate_single_game("algorithmic", "algorithmic", "easy", "hard", verbose=True)
    print(f"Game result: {result['winner']} won in {result['turns']} turns")

    # Example 2: Small tournament
    print("\nRunning small tournament...")
    bot_configs = [
        {'type': 'algorithmic', 'difficulty': 'easy'},
        {'type': 'algorithmic', 'difficulty': 'medium'},
        {'type': 'algorithmic', 'difficulty': 'hard'}
    ]

    tournament_results = controller.run_tournament(bot_configs, games_per_matchup=3, verbose=True)

    print("\nTournament Leaderboard:")
    for i, entry in enumerate(tournament_results['leaderboard']):
        print(f"{i+1}. {entry['bot_type']} ({entry['points']} points, {entry['win_rate']:.2%} win rate)")


if __name__ == "__main__":
    main()
