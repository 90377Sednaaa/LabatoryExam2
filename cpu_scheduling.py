"""
CPU Scheduling Algorithms Simulation
Laboratory Exam 2 - Operating Systems Simulation

This module simulates non-preemptive and preemptive CPU scheduling algorithms:
1. First-Come, First-Served (FCFS) [Non-preemptive]
2. Shortest Job First (SJF) [Non-preemptive]
3. Shortest Remaining Time First (SRTF / Preemptive SJF) [Preemptive]
4. Round Robin (RR) [Preemptive]

It outputs:
- Chronological ASCII Gantt Chart
- Detailed per-process statistics (Completion, Turnaround, Waiting times)
- Average Turnaround Time and Average Waiting Time
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
from collections import deque
import copy


@dataclass
class Process:
    """
    Data model representing a process in the CPU scheduling simulator.
    
    Attributes:
        pid: Unique process identifier (e.g. "P1", "P2").
        arrival_time: Time at which the process arrives in the ready queue (>= 0).
        burst_time: Total CPU execution time required by the process (> 0).
        remaining_time: CPU burst time remaining to be executed (used in preemptive algorithms).
        completion_time: Time at which the process finishes execution (CT).
        turnaround_time: Total elapsed time from arrival to completion (TAT = CT - AT).
        waiting_time: Total time spent waiting in ready queue (WT = TAT - BT).
        start_time: Time at which the process first gets CPU access.
    """
    pid: str
    arrival_time: int
    burst_time: int
    remaining_time: int = 0
    completion_time: int = 0
    turnaround_time: int = 0
    waiting_time: int = 0
    start_time: Optional[int] = None

    def __post_init__(self):
        if self.remaining_time == 0:
            self.remaining_time = self.burst_time


def consolidate_timeline(timeline: List[Tuple[str, int, int]]) -> List[Tuple[str, int, int]]:
    """
    Merges contiguous execution intervals of the same process/IDLE block.
    
    Example:
        [('P1', 0, 1), ('P1', 1, 2)] -> [('P1', 0, 2)]
    """
    if not timeline:
        return []
    consolidated: List[Tuple[str, int, int]] = []
    for pid, start, end in timeline:
        if start == end:
            continue
        if consolidated and consolidated[-1][0] == pid and consolidated[-1][2] == start:
            prev_pid, prev_start, _ = consolidated[-1]
            consolidated[-1] = (prev_pid, prev_start, end)
        else:
            consolidated.append((pid, start, end))
    return consolidated


def simulate_fcfs(
    processes: List[Process]
) -> Tuple[List[Process], List[Tuple[str, int, int]]]:
    """
    Simulates First-Come, First-Served (FCFS) Scheduling [Non-Preemptive].
    
    Processes are executed in the exact order of their arrival.
    If multiple processes arrive simultaneously, process ID breaks the tie.
    """
    # Clone processes to avoid mutating original list
    procs = [copy.deepcopy(p) for p in processes]
    # Sort primarily by arrival time, secondarily by PID
    procs.sort(key=lambda p: (p.arrival_time, p.pid))
    
    current_time = 0
    timeline: List[Tuple[str, int, int]] = []
    
    for p in procs:
        # If CPU is idle before this process arrives, record IDLE time
        if current_time < p.arrival_time:
            timeline.append(("IDLE", current_time, p.arrival_time))
            current_time = p.arrival_time
            
        p.start_time = current_time
        start = current_time
        current_time += p.burst_time
        p.completion_time = current_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time
        timeline.append((p.pid, start, current_time))
        
    return procs, consolidate_timeline(timeline)


def simulate_sjf(
    processes: List[Process]
) -> Tuple[List[Process], List[Tuple[str, int, int]]]:
    """
    Simulates Shortest Job First (SJF) Scheduling [Non-Preemptive].
    
    At each scheduling point, the arrived process with the shortest CPU burst time
    is selected and runs to completion without interruption.
    """
    procs = [copy.deepcopy(p) for p in processes]
    completed: List[Process] = []
    timeline: List[Tuple[str, int, int]] = []
    current_time = 0
    
    while len(completed) < len(procs):
        # Identify all processes that have arrived and have not yet finished
        available = [p for p in procs if p.arrival_time <= current_time and p not in completed]
        
        if not available:
            # CPU is idle: advance current_time to the next earliest arrival
            uncompleted = [p for p in procs if p not in completed]
            next_arrival = min(p.arrival_time for p in uncompleted)
            timeline.append(("IDLE", current_time, next_arrival))
            current_time = next_arrival
            continue
            
        # Select process with shortest burst time (tie-breakers: earlier arrival, then PID)
        chosen = min(available, key=lambda p: (p.burst_time, p.arrival_time, p.pid))
        
        chosen.start_time = current_time
        start = current_time
        current_time += chosen.burst_time
        chosen.completion_time = current_time
        chosen.turnaround_time = chosen.completion_time - chosen.arrival_time
        chosen.waiting_time = chosen.turnaround_time - chosen.burst_time
        
        timeline.append((chosen.pid, start, current_time))
        completed.append(chosen)
        
    return completed, consolidate_timeline(timeline)


def simulate_srtf(
    processes: List[Process]
) -> Tuple[List[Process], List[Tuple[str, int, int]]]:
    """
    Simulates Shortest Remaining Time First (SRTF) [Preemptive SJF].
    
    At any time, the process with the smallest remaining burst time is allocated the CPU.
    If a newly arrived process has a shorter remaining burst time than the currently running
    process, the running process is preempted.
    """
    procs = [copy.deepcopy(p) for p in processes]
    completed: List[Process] = []
    timeline: List[Tuple[str, int, int]] = []
    current_time = 0
    
    while len(completed) < len(procs):
        # Eligible processes: arrived and remaining time > 0
        available = [p for p in procs if p.arrival_time <= current_time and p.remaining_time > 0]
        
        if not available:
            # CPU is idle: jump to next arrival
            uncompleted = [p for p in procs if p.remaining_time > 0]
            next_arrival = min(p.arrival_time for p in uncompleted)
            timeline.append(("IDLE", current_time, next_arrival))
            current_time = next_arrival
            continue
            
        # Pick process with smallest remaining time
        chosen = min(available, key=lambda p: (p.remaining_time, p.arrival_time, p.pid))
        
        if chosen.start_time is None:
            chosen.start_time = current_time
            
        # Determine how long chosen can run before the next event
        # The next event is either chosen finishing or a new process arriving
        future_arrivals = [p.arrival_time for p in procs if p.arrival_time > current_time and p.remaining_time > 0]
        next_arrival = min(future_arrivals) if future_arrivals else None
        
        if next_arrival is not None:
            time_slice = min(chosen.remaining_time, next_arrival - current_time)
        else:
            time_slice = chosen.remaining_time
            
        start = current_time
        current_time += time_slice
        chosen.remaining_time -= time_slice
        timeline.append((chosen.pid, start, current_time))
        
        if chosen.remaining_time == 0:
            chosen.completion_time = current_time
            chosen.turnaround_time = chosen.completion_time - chosen.arrival_time
            chosen.waiting_time = chosen.turnaround_time - chosen.burst_time
            completed.append(chosen)
            
    return completed, consolidate_timeline(timeline)


def simulate_round_robin(
    processes: List[Process],
    quantum: int
) -> Tuple[List[Process], List[Tuple[str, int, int]]]:
    """
    Simulates Round Robin (RR) Scheduling [Preemptive].
    
    Processes are given CPU time in cyclic slices of at most `quantum` duration.
    A FIFO ready queue is maintained.
    New arrivals during a time slice are enqueued before the preempted process.
    """
    if quantum <= 0:
        raise ValueError("Time quantum must be greater than 0.")
        
    procs = [copy.deepcopy(p) for p in processes]
    # Sort processes by arrival time initially
    procs.sort(key=lambda p: (p.arrival_time, p.pid))
    
    ready_queue: deque[Process] = deque()
    completed: List[Process] = []
    timeline: List[Tuple[str, int, int]] = []
    
    current_time = 0
    arrived_indices = set()
    
    # Enqueue processes that arrive at or before time 0
    for i, p in enumerate(procs):
        if p.arrival_time <= current_time:
            ready_queue.append(p)
            arrived_indices.add(i)
            
    while len(completed) < len(procs):
        if not ready_queue:
            # CPU is idle: jump to next process arrival
            unvisited = [p for i, p in enumerate(procs) if i not in arrived_indices]
            next_arrival = min(p.arrival_time for p in unvisited)
            timeline.append(("IDLE", current_time, next_arrival))
            current_time = next_arrival
            
            # Add processes arriving at this new current_time
            for i, p in enumerate(procs):
                if i not in arrived_indices and p.arrival_time <= current_time:
                    ready_queue.append(p)
                    arrived_indices.add(i)
            continue
            
        current_proc = ready_queue.popleft()
        if current_proc.start_time is None:
            current_proc.start_time = current_time
            
        slice_time = min(current_proc.remaining_time, quantum)
        start = current_time
        current_time += slice_time
        current_proc.remaining_time -= slice_time
        timeline.append((current_proc.pid, start, current_time))
        
        # Check for newly arrived processes during (start, current_time]
        for i, p in enumerate(procs):
            if i not in arrived_indices and p.arrival_time <= current_time:
                ready_queue.append(p)
                arrived_indices.add(i)
                
        # If current process still has remaining work, put it back into queue
        if current_proc.remaining_time > 0:
            ready_queue.append(current_proc)
        else:
            current_proc.completion_time = current_time
            current_proc.turnaround_time = current_proc.completion_time - current_proc.arrival_time
            current_proc.waiting_time = current_proc.turnaround_time - current_proc.burst_time
            completed.append(current_proc)
            
    return completed, consolidate_timeline(timeline)


def render_gantt_chart(timeline: List[Tuple[str, int, int]]) -> str:
    """
    Renders an ASCII representation of the execution timeline (Gantt Chart).
    
    Example:
    +-------+-------+-------+
    |  P1   |  P2   |  P3   |
    +-------+-------+-------+
    0       4       7       8
    """
    if not timeline:
        return "Empty timeline."
        
    top_border = "+"
    middle_bar = "|"
    time_line = str(timeline[0][1])
    
    for pid, start, end in timeline:
        cell_width = max(len(pid) + 4, 7)
        top_border += "-" * cell_width + "+"
        middle_bar += pid.center(cell_width) + "|"
        
        end_str = str(end)
        target_pos = len(top_border) - 1
        spaces_needed = max(1, target_pos - len(time_line))
        time_line += " " * spaces_needed + end_str
        
    lines = [
        top_border,
        middle_bar,
        top_border,
        time_line,
    ]
    return "\n".join(lines)


def print_schedule_results(
    processes: List[Process],
    timeline: List[Tuple[str, int, int]],
    algorithm_name: str
) -> None:
    """
    Formats and prints the Gantt Chart, detailed process table, and averages.
    """
    # Sort processes by PID for clear table presentation
    sorted_procs = sorted(processes, key=lambda p: (len(p.pid), p.pid))
    
    total_tat = sum(p.turnaround_time for p in sorted_procs)
    total_wt = sum(p.waiting_time for p in sorted_procs)
    n = len(sorted_procs)
    avg_tat = total_tat / n if n > 0 else 0.0
    avg_wt = total_wt / n if n > 0 else 0.0
    
    print("\n" + "=" * 65)
    print(f"  CPU Scheduling Results: {algorithm_name}")
    print("=" * 65)
    
    print("\nGantt Chart:")
    print(render_gantt_chart(timeline))
    
    print("\nProcess Execution Details:")
    header = f"{'Process':<9} | {'Arrival Time':<12} | {'Burst Time':<10} | {'Completion Time':<15} | {'Turnaround Time':<15} | {'Waiting Time':<12}"
    divider = "-" * len(header)
    print(divider)
    print(header)
    print(divider)
    
    for p in sorted_procs:
        print(f"{p.pid:<9} | {p.arrival_time:<12} | {p.burst_time:<10} | {p.completion_time:<15} | {p.turnaround_time:<15} | {p.waiting_time:<12}")
    print(divider)
    
    print(f"\nAverage Turnaround Time : {avg_tat:.2f}")
    print(f"Average Waiting Time    : {avg_wt:.2f}")
    print("=" * 65 + "\n")


def prompt_for_processes() -> List[Process]:
    """
    Helper function to interactively collect process inputs from the console.
    """
    while True:
        try:
            n_str = input("Enter number of processes: ").strip()
            num_processes = int(n_str)
            if num_processes <= 0:
                print("Error: Number of processes must be at least 1.")
                continue
            break
        except ValueError:
            print("Error: Please enter a valid integer.")
            
    processes: List[Process] = []
    print("\nEnter details for each process:")
    for i in range(1, num_processes + 1):
        pid = f"P{i}"
        while True:
            try:
                print(f"\n--- Process {pid} ---")
                at_input = input(f"Arrival Time for {pid}: ").strip()
                at = int(at_input)
                if at < 0:
                    print("Error: Arrival time cannot be negative.")
                    continue
                    
                bt_input = input(f"Burst Time for {pid}: ").strip()
                bt = int(bt_input)
                if bt <= 0:
                    print("Error: Burst time must be greater than 0.")
                    continue
                    
                processes.append(Process(pid=pid, arrival_time=at, burst_time=bt))
                break
            except ValueError:
                print("Error: Please enter valid integers for Arrival and Burst times.")
                
    return processes


def run_interactive_scheduling(algorithm_code: str) -> None:
    """
    Runs an interactive scheduling session for the specified algorithm.
    """
    algo_names = {
        "1": "First-Come, First-Served (FCFS) [Non-Preemptive]",
        "2": "Shortest Job First (SJF) [Non-Preemptive]",
        "3": "Shortest Remaining Time First (SRTF) [Preemptive SJF]",
        "4": "Round Robin (RR) [Preemptive]",
    }
    
    name = algo_names.get(algorithm_code, "CPU Scheduling")
    print(f"\n>>> Selected Algorithm: {name} <<<")
    
    procs = prompt_for_processes()
    if not procs:
        return
        
    if algorithm_code == "1":
        completed, timeline = simulate_fcfs(procs)
    elif algorithm_code == "2":
        completed, timeline = simulate_sjf(procs)
    elif algorithm_code == "3":
        completed, timeline = simulate_srtf(procs)
    elif algorithm_code == "4":
        while True:
            try:
                q_input = input("\nEnter Time Quantum for Round Robin: ").strip()
                quantum = int(q_input)
                if quantum <= 0:
                    print("Error: Time Quantum must be greater than 0.")
                    continue
                break
            except ValueError:
                print("Error: Please enter a valid integer for Time Quantum.")
        completed, timeline = simulate_round_robin(procs, quantum)
    else:
        print("Unknown algorithm code.")
        return
        
    print_schedule_results(completed, timeline, name)


if __name__ == "__main__":
    try:
        print("==================================================")
        print("         CPU Scheduling Simulator                 ")
        print("==================================================")
        print("1. First-Come, First-Served (FCFS) [Non-Preemptive]")
        print("2. Shortest Job First (SJF) [Non-Preemptive]")
        print("3. Shortest Remaining Time First (SRTF) [Preemptive SJF]")
        print("4. Round Robin (RR) [Preemptive]")
        print("0. Exit")
        
        choice = input("\nSelect algorithm [1-4, 0]: ").strip()
        if choice in {"1", "2", "3", "4"}:
            run_interactive_scheduling(choice)
        else:
            print("Exiting CPU Scheduling Simulator.")
    except (KeyboardInterrupt, EOFError):
        print("\n\nOperation cancelled. Exiting...\n")
