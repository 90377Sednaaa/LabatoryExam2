"""
Unit tests for CPU Scheduling and Banker's Algorithm simulation.
"""
import unittest

from bankers_algorithm import (
    calculate_need,
    is_safe_state,
    PRECONFIGURED_DATA,
)
from cpu_scheduling import (
    Process,
    simulate_fcfs,
    simulate_sjf,
    simulate_srtf,
    simulate_round_robin,
    render_gantt_chart,
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


class CPUSchedulingTests(unittest.TestCase):
    """Test suite for CPU Scheduling algorithms and Gantt chart generation."""

    def test_fcfs_scheduling(self):
        procs = [
            Process("P1", arrival_time=0, burst_time=4),
            Process("P2", arrival_time=1, burst_time=3),
            Process("P3", arrival_time=2, burst_time=1),
        ]
        completed, timeline = simulate_fcfs(procs)
        proc_dict = {p.pid: p for p in completed}

        self.assertEqual(proc_dict["P1"].completion_time, 4)
        self.assertEqual(proc_dict["P1"].waiting_time, 0)
        self.assertEqual(proc_dict["P1"].turnaround_time, 4)

        self.assertEqual(proc_dict["P2"].completion_time, 7)
        self.assertEqual(proc_dict["P2"].waiting_time, 3)
        self.assertEqual(proc_dict["P2"].turnaround_time, 6)

        self.assertEqual(proc_dict["P3"].completion_time, 8)
        self.assertEqual(proc_dict["P3"].waiting_time, 5)
        self.assertEqual(proc_dict["P3"].turnaround_time, 6)

        self.assertEqual(timeline, [("P1", 0, 4), ("P2", 4, 7), ("P3", 7, 8)])

    def test_fcfs_with_idle_time(self):
        procs = [
            Process("P1", arrival_time=2, burst_time=3),
        ]
        completed, timeline = simulate_fcfs(procs)
        self.assertEqual(timeline, [("IDLE", 0, 2), ("P1", 2, 5)])
        self.assertEqual(completed[0].waiting_time, 0)
        self.assertEqual(completed[0].completion_time, 5)

    def test_sjf_non_preemptive(self):
        procs = [
            Process("P1", arrival_time=0, burst_time=7),
            Process("P2", arrival_time=2, burst_time=4),
            Process("P3", arrival_time=4, burst_time=1),
            Process("P4", arrival_time=5, burst_time=4),
        ]
        completed, timeline = simulate_sjf(procs)
        proc_dict = {p.pid: p for p in completed}

        self.assertEqual(proc_dict["P1"].completion_time, 7)
        self.assertEqual(proc_dict["P3"].completion_time, 8)
        self.assertEqual(proc_dict["P2"].completion_time, 12)
        self.assertEqual(proc_dict["P4"].completion_time, 16)

        self.assertEqual(timeline, [("P1", 0, 7), ("P3", 7, 8), ("P2", 8, 12), ("P4", 12, 16)])

    def test_srtf_preemptive(self):
        procs = [
            Process("P1", arrival_time=0, burst_time=8),
            Process("P2", arrival_time=1, burst_time=4),
            Process("P3", arrival_time=2, burst_time=9),
            Process("P4", arrival_time=3, burst_time=5),
        ]
        completed, timeline = simulate_srtf(procs)
        proc_dict = {p.pid: p for p in completed}

        self.assertEqual(proc_dict["P2"].completion_time, 5)
        self.assertEqual(proc_dict["P4"].completion_time, 10)
        self.assertEqual(proc_dict["P1"].completion_time, 17)
        self.assertEqual(proc_dict["P3"].completion_time, 26)

        self.assertEqual(proc_dict["P1"].waiting_time, 9)
        self.assertEqual(proc_dict["P2"].waiting_time, 0)
        self.assertEqual(proc_dict["P3"].waiting_time, 15)
        self.assertEqual(proc_dict["P4"].waiting_time, 2)

        self.assertEqual(timeline, [
            ("P1", 0, 1),
            ("P2", 1, 5),
            ("P4", 5, 10),
            ("P1", 10, 17),
            ("P3", 17, 26),
        ])

    def test_round_robin(self):
        procs = [
            Process("P1", arrival_time=0, burst_time=5),
            Process("P2", arrival_time=1, burst_time=3),
            Process("P3", arrival_time=2, burst_time=1),
        ]
        completed, timeline = simulate_round_robin(procs, quantum=2)
        proc_dict = {p.pid: p for p in completed}

        self.assertEqual(proc_dict["P3"].completion_time, 5)
        self.assertEqual(proc_dict["P2"].completion_time, 8)
        self.assertEqual(proc_dict["P1"].completion_time, 9)

        self.assertEqual(proc_dict["P1"].waiting_time, 4)
        self.assertEqual(proc_dict["P2"].waiting_time, 4)
        self.assertEqual(proc_dict["P3"].waiting_time, 2)

        self.assertEqual(timeline, [
            ("P1", 0, 2),
            ("P2", 2, 4),
            ("P3", 4, 5),
            ("P1", 5, 7),
            ("P2", 7, 8),
            ("P1", 8, 9),
        ])

    def test_render_gantt_chart(self):
        timeline = [("P1", 0, 4), ("P2", 4, 7), ("P3", 7, 8)]
        chart = render_gantt_chart(timeline)
        self.assertIn("P1", chart)
        self.assertIn("P2", chart)
        self.assertIn("P3", chart)
        self.assertIn("0", chart)
        self.assertIn("8", chart)


if __name__ == "__main__":
    unittest.main()
