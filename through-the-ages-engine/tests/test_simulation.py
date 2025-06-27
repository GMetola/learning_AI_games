#!/usr/bin/env python3
"""
Quick test of the simulation controller
"""

import sys
import os
import logging
import traceback

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from simulation.controller import SimulationController


def test_simulation():
    """Test basic simulation functionality"""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    print("Creating simulation controller...")
    controller = SimulationController()

    print("Running a simple bot vs bot game...")
    result = controller.simulate_single_game(
        "algorithmic", "algorithmic",
        "easy", "medium",
        max_turns=5,
        verbose=True
    )

    print(f"\n=== GAME RESULTS ===")
    print(f"Winner: {result['winner']}")
    print(f"Turns: {result['turns']}")
    print(f"Game Over Reason: {result['game_over_reason']}")
    print(f"Final Scores: {result['final_scores']}")
    print(f"Duration: {result['duration']:.2f} seconds")

    print(f"\n=== ACTION LOG (last 5 actions) ===")
    for action in result['game_log'][-5:]:
        print(f"Turn {action['turn']}: {action['player']} -> {action['action']} (Success: {action['success']})")

    return True

if __name__ == "__main__":
    success = test_simulation()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")
