"""
Banker's Algorithm for Deadlock Avoidance
Laboratory Exam 2 - Operating Systems Simulation

This module implements Dijkstra's Banker's Algorithm.
It tests whether allocating resources to processes leaves the system in a safe state,
ensuring that deadlocks can never occur by finding a safe execution sequence.
"""

from typing import List, Tuple, Dict, Any, Optional

# Pre-configured dataset from standard OS textbook / laboratory exam specification:
# 5 processes (P0 to P4) and 3 resource types (A, B, C)
PRECONFIGURED_DATA: Dict[str, Any] = {
    "processes": ["P0", "P1", "P2", "P3", "P4"],
    "allocation": [
        [0, 1, 0],  # P0
        [2, 0, 0],  # P1
        [3, 0, 2],  # P2
        [2, 1, 1],  # P3
        [0, 0, 2],  # P4
    ],
    "max": [
        [7, 5, 3],  # P0
        [3, 2, 2],  # P1
        [9, 0, 2],  # P2
        [2, 2, 2],  # P3
        [4, 3, 3],  # P4
    ],
    "available": [3, 3, 2],  # Available instances of resource types [A, B, C]
}


def calculate_need(
    allocation: List[List[int]],
    max_matrix: List[List[int]]
) -> List[List[int]]:
    """
    Computes the Need Matrix for all processes.
    
    Formula:
        Need[i][j] = Max[i][j] - Allocation[i][j]
        
    where:
        - Max[i][j] represents the maximum demand of process i for resource j.
        - Allocation[i][j] represents instances of resource j currently allocated to process i.
        - Need[i][j] represents remaining instances needed by process i to finish.
    """
    num_processes = len(allocation)
    num_resources = len(allocation[0])
    
    need = []
    for i in range(num_processes):
        row = []
        for j in range(num_resources):
            row.append(max_matrix[i][j] - allocation[i][j])
        need.append(row)
    return need


def is_safe_state(
    processes: List[str],
    allocation: List[List[int]],
    max_matrix: List[List[int]],
    available: List[int]
) -> Tuple[bool, List[str], List[List[int]]]:
    """
    Safety Algorithm of Banker's Algorithm.
    
    Determines whether the system is in a safe state.
    
    Returns:
        (is_safe, safe_sequence, need_matrix)
        - is_safe: True if a safe sequence exists, False otherwise.
        - safe_sequence: Ordered list of process names in safe execution order.
        - need_matrix: The computed remaining resource requirements.
    """
    num_processes = len(processes)
    num_resources = len(available)
    
    # Step 1: Calculate Need Matrix
    need = calculate_need(allocation, max_matrix)
    
    # Step 2: Initialize Work and Finish vectors
    # Work vector represents currently available resources as processes complete.
    work = list(available)
    # Finish[i] tracks whether process i has safely completed execution.
    finish = [False] * num_processes
    
    safe_sequence: List[str] = []
    
    # Step 3: Find unallocated processes using circular scanning
    # Standard textbook Banker's algorithm continues scanning cyclically from the current process
    current_idx = 0
    checks_without_progress = 0
    
    while len(safe_sequence) < num_processes and checks_without_progress < num_processes:
        i = current_idx
        if not finish[i]:
            can_allocate = True
            for j in range(num_resources):
                if need[i][j] > work[j]:
                    can_allocate = False
                    break
            
            if can_allocate:
                for j in range(num_resources):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_sequence.append(processes[i])
                checks_without_progress = 0
            else:
                checks_without_progress += 1
        else:
            checks_without_progress += 1
            
        current_idx = (current_idx + 1) % num_processes
            
    # System is in safe state if and only if all processes could safely finish
    is_safe = (len(safe_sequence) == num_processes)
    return is_safe, safe_sequence if is_safe else [], need


def print_bankers_output(
    processes: List[str],
    need_matrix: List[List[int]],
    is_safe: bool,
    safe_sequence: List[str]
) -> None:
    """
    Prints the output matching the laboratory reference format:
    
    Need Matrix:
    P0: [7, 4, 3]
    ...
    System is in a Safe State.
    Safe Sequence: P1 -> P3 -> P4 -> P0 -> P2
    """
    print("\nNeed Matrix:")
    for proc, row in zip(processes, need_matrix):
        print(f"{proc}: {row}")
    
    print()
    if is_safe:
        print("System is in a Safe State.")
        print("Safe Sequence: " + " -> ".join(safe_sequence))
    else:
        print("System is in an Unsafe State (Deadlock may occur).")
        print("No safe sequence exists.")
    print()


def run_preconfigured_bankers() -> None:
    """
    Runs Banker's Algorithm instantly using the pre-configured dataset.
    No user input is required, producing the exact reference output.
    """
    processes = PRECONFIGURED_DATA["processes"]
    allocation = PRECONFIGURED_DATA["allocation"]
    max_matrix = PRECONFIGURED_DATA["max"]
    available = PRECONFIGURED_DATA["available"]
    
    print("\n--- Running Banker's Algorithm (Pre-configured Data) ---")
    is_safe, safe_seq, need = is_safe_state(processes, allocation, max_matrix, available)
    print_bankers_output(processes, need, is_safe, safe_seq)


import re


def parse_integer_list(raw: str, expected_count: int) -> Optional[List[int]]:
    """
    Parses a user input line into a list of non-negative integers.
    Supports:
    - Space-separated: '3 3 3'
    - Comma-separated or bracketed: '3, 3, 3', '[3, 3, 3]'
    - Compact single digits: '333' (when length matches expected_count)
    """
    cleaned = raw.strip().replace("\ufeff", "")
    # Extract all integer tokens
    tokens = re.findall(r"-?\d+", cleaned)
    if len(tokens) == expected_count:
        vals = [int(t) for t in tokens]
        if all(v >= 0 for v in vals):
            return vals
            
    # Fallback for single-digit inputs without spaces (e.g. '333' for 3 resources)
    if len(cleaned) == expected_count and cleaned.isdigit():
        return [int(c) for c in cleaned]
        
    return None


def run_custom_bankers() -> None:
    """
    Interactively prompts the user to input custom matrices for Banker's Algorithm.
    """
    print("\n--- Banker's Algorithm (Custom Input) ---")
    try:
        p_str = input("Enter number of processes: ").strip().replace("\ufeff", "")
        r_str = input("Enter number of resource types: ").strip().replace("\ufeff", "")
        num_p = int(p_str)
        num_r = int(r_str)
        
        if num_p <= 0 or num_r <= 0:
            print("Number of processes and resources must be positive integers.")
            return
            
        processes = [f"P{i}" for i in range(num_p)]
        
        print(f"\nEnter Allocation Matrix ({num_p} rows, {num_r} integers each, e.g. '0 1 0' or '010'):")
        allocation = []
        for i in range(num_p):
            while True:
                line = input(f"Allocation for {processes[i]}: ")
                vals = parse_integer_list(line, num_r)
                if vals is not None:
                    allocation.append(vals)
                    break
                print(f"Error: Please enter {num_r} non-negative integers (e.g., '0 1 0', '0, 1, 0', or '010').")
                
        print(f"\nEnter Maximum Matrix ({num_p} rows, {num_r} integers each, e.g. '7 5 3' or '753'):")
        max_matrix = []
        for i in range(num_p):
            while True:
                line = input(f"Maximum for {processes[i]}: ")
                vals = parse_integer_list(line, num_r)
                if vals is not None:
                    # Validate Max >= Allocation
                    if all(vals[j] >= allocation[i][j] for j in range(num_r)):
                        max_matrix.append(vals)
                        break
                    else:
                        print("Error: Max demand must be greater than or equal to current Allocation.")
                else:
                    print(f"Error: Please enter {num_r} non-negative integers (e.g., '7 5 3', '7, 5, 3', or '753').")
                    
        print(f"\nEnter Available Resources ({num_r} integers, e.g. '3 3 2' or '332'):")
        while True:
            line = input("Available: ")
            vals = parse_integer_list(line, num_r)
            if vals is not None:
                available = vals
                break
            print(f"Error: Please enter {num_r} non-negative integers (e.g., '3 3 2', '3, 3, 2', or '332').")
            
        is_safe, safe_seq, need = is_safe_state(processes, allocation, max_matrix, available)
        print_bankers_output(processes, need, is_safe, safe_seq)
        
    except ValueError:
        print("Invalid input! Please enter valid integers.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    try:
        print("==================================================")
        print("         Banker's Algorithm Simulation            ")
        print("==================================================")
        print("1. Pre-configured Data (Instant output from example)")
        print("2. Custom User Input")
        choice = input("Select mode [1/2] (Default 1): ").strip()
        
        if choice == "2":
            run_custom_bankers()
        else:
            run_preconfigured_bankers()
    except (KeyboardInterrupt, EOFError):
        print("\n\nOperation cancelled. Exiting...\n")
