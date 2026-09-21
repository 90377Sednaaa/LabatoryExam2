"""
Unit tests for CPU Scheduling and Banker's Algorithm simulation.
"""
import unittest

from bankers_algorithm import (
    calculate_need,
    is_safe_state,
    PRECONFIGURED_DATA,
)


class BankersAlgorithmTests(unittest.TestCase):
    """Test suite for Banker's Algorithm deadlock avoidance."""

    def test_calculate_need(self):
        allocation = [
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2],
        ]
        max_matrix = [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3],
        ]
        expected_need = [
            [7, 4, 3],
            [1, 2, 2],
            [6, 0, 0],
            [0, 1, 1],
            [4, 3, 1],
        ]
        need = calculate_need(allocation, max_matrix)
        self.assertEqual(need, expected_need)

    def test_preconfigured_safe_sequence(self):
        processes = PRECONFIGURED_DATA["processes"]
        allocation = PRECONFIGURED_DATA["allocation"]
        max_matrix = PRECONFIGURED_DATA["max"]
        available = PRECONFIGURED_DATA["available"]

        is_safe, safe_seq, need = is_safe_state(processes, allocation, max_matrix, available)
        self.assertTrue(is_safe)
        self.assertEqual(safe_seq, ["P1", "P3", "P4", "P0", "P2"])
        self.assertEqual(need, [
            [7, 4, 3],
            [1, 2, 2],
            [6, 0, 0],
            [0, 1, 1],
            [4, 3, 1],
        ])

    def test_unsafe_state(self):
        processes = ["P0", "P1", "P2"]
        allocation = [
            [1, 2],
            [2, 1],
            [2, 1],
        ]
        max_matrix = [
            [3, 3],
            [4, 3],
            [3, 4],
        ]
        # Need:
        # P0: [2, 1]
        # P1: [2, 2]
        # P2: [1, 3]
        # Available: [0, 0] -> No process can be satisfied
        available = [0, 0]

        is_safe, safe_seq, _ = is_safe_state(processes, allocation, max_matrix, available)
        self.assertFalse(is_safe)
        self.assertEqual(safe_seq, [])


if __name__ == "__main__":
    unittest.main()
