# CPU Scheduling and Banker's Algorithm Simulation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete Python simulation for preemptive (Round Robin, SRTF) and non-preemptive (FCFS, SJF) CPU scheduling algorithms with Gantt chart generation and average turnaround/waiting time calculations, alongside Banker's Algorithm for deadlock avoidance (supporting instant reference sample output matching the provided specification and custom user matrix input).

**Architecture:** 
- `bankers_algorithm.py`: Core logic for Need Matrix calculation and safety state determination with dual modes (pre-configured instant run & custom user matrix input).
- `cpu_scheduling.py`: Process models, simulation engines (FCFS, SJF, SRTF, RR), ASCII Gantt chart generator, and metrics calculation.
- `main.py`: Interactive CLI dashboard uniting all simulation features.
- `test_simulation.py`: Standard library `unittest` suite covering all scheduling and safety conditions.
- `README.md`: Complete documentation on how to run, OS concepts, and sample outputs.

**Tech Stack:** Python 3 (standard library only: `typing`, `dataclasses`, `collections`, `unittest`).

## Global Constraints
- Target platform: Windows / Cross-platform standard Python 3.
- No external pip dependencies required.
- Clear, readable ASCII Gantt chart output with timestamps.
- Exact match for sample Banker's Algorithm output:
  `Need Matrix: P0: [7, 4, 3], P1: [1, 2, 2], P2: [6, 0, 0], P3: [0, 1, 1], P4: [4, 3, 1]`
  `System is in a Safe State.`
  `Safe Sequence: P1 -> P3 -> P4 -> P0 -> P2`
- Code must be thoroughly commented explaining OS concepts.

---

### Task 1: Banker's Algorithm Module

**Files:**
- Create: `bankers_algorithm.py`
- Test: `test_simulation.py`

**Interfaces:**
- Produces:
  - `calculate_need(allocation: list[list[int]], max_matrix: list[list[int]]) -> list[list[int]]`
  - `is_safe_state(processes: list[str], allocation: list[list[int]], max_matrix: list[list[int]], available: list[int]) -> tuple[bool, list[str], list[list[int]]]`
  - `print_bankers_output(processes: list[str], need_matrix: list[list[int]], is_safe: bool, safe_sequence: list[str]) -> None`
  - `run_preconfigured_bankers() -> None`
  - `run_custom_bankers() -> None`

- [ ] **Step 1: Write test case for Banker's Algorithm**
Add tests in `test_simulation.py` for safe state with the reference sample matrix and an unsafe deadlock state.

- [ ] **Step 2: Run test to verify failure**
Run: `python -m unittest test_simulation.py`
Expected: Failure (module not yet implemented).

- [ ] **Step 3: Implement `bankers_algorithm.py`**
Implement matrix calculation, safety algorithm, preconfigured dataset matching the reference output, custom input handler, and standalone execution block `if __name__ == "__main__":`.

- [ ] **Step 4: Run test to verify it passes**
Run: `python -m unittest test_simulation.BankersAlgorithmTests`
Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add bankers_algorithm.py test_simulation.py; git commit -m "feat: implement Banker's Algorithm with dual preconfigured and custom modes"
```

---

### Task 2: CPU Scheduling Core & Algorithms

**Files:**
- Create: `cpu_scheduling.py`
- Test: `test_simulation.py`

**Interfaces:**
- Produces:
  - `Process(pid: str, arrival_time: int, burst_time: int, remaining_time: int, completion_time: int, turnaround_time: int, waiting_time: int, start_time: int)`
  - `simulate_fcfs(processes: list[Process]) -> tuple[list[Process], list[tuple[str, int, int]]]`
  - `simulate_sjf(processes: list[Process]) -> tuple[list[Process], list[tuple[str, int, int]]]`
  - `simulate_srtf(processes: list[Process]) -> tuple[list[Process], list[tuple[str, int, int]]]`
  - `simulate_round_robin(processes: list[Process], quantum: int) -> tuple[list[Process], list[tuple[str, int, int]]]`
  - `render_gantt_chart(timeline: list[tuple[str, int, int]]) -> str`
  - `print_schedule_results(processes: list[Process], timeline: list[tuple[str, int, int]], algorithm_name: str) -> None`

- [ ] **Step 1: Write unit tests for FCFS, SJF, SRTF, and Round Robin**
Add test methods in `test_simulation.py` verifying completion time, turnaround time, waiting time, and average metrics on standard test cases.

- [ ] **Step 2: Run tests to verify failure**
Run: `python -m unittest test_simulation.py`
Expected: Failure (cpu_scheduling module not yet implemented).

- [ ] **Step 3: Implement `cpu_scheduling.py`**
Implement the `Process` dataclass, FCFS, SJF, SRTF, Round Robin simulation engines, ASCII Gantt chart formatter, results table generator, and interactive user prompt function when run standalone.

- [ ] **Step 4: Run tests to verify they pass**
Run: `python -m unittest test_simulation.CPUSchedulingTests`
Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add cpu_scheduling.py test_simulation.py; git commit -m "feat: implement CPU scheduling algorithms and Gantt chart visualization"
```

---

### Task 3: Interactive CLI Runner (`main.py`)

**Files:**
- Create: `main.py`

**Interfaces:**
- Consumes:
  - `bankers_algorithm.run_preconfigured_bankers`, `bankers_algorithm.run_custom_bankers`
  - `cpu_scheduling.run_interactive_scheduling`

- [ ] **Step 1: Implement `main.py`**
Build the user-friendly terminal menu providing options for each CPU scheduling algorithm, pre-configured Banker's output, custom Banker's input, and exit. Include graceful input handling and loop until user chooses to exit.

- [ ] **Step 2: Test `main.py` execution non-interactively and interactively**
Run `python -c "import main; print('main imported successfully')"` and verify menu logic.

- [ ] **Step 3: Commit**
```bash
git add main.py; git commit -m "feat: add main interactive menu CLI"
```

---

### Task 4: Documentation (`README.md`)

**Files:**
- Create: `README.md`

- [ ] **Step 1: Write comprehensive `README.md`**
Document requirements, project structure, instructions to run both standalone modules and `main.py`, explanation of scheduling and Banker's algorithms, and sample outputs (including screenshot reference output).

- [ ] **Step 2: Commit**
```bash
git add README.md; git commit -m "docs: add comprehensive README with instructions and sample outputs"
```

---

### Task 5: Final Full Verification

- [ ] **Step 1: Run complete automated test suite**
Run: `python -m unittest discover -s . -p "test_*.py" -v`
Expected: 100% tests passing.

- [ ] **Step 2: Execute sample runs**
Run pre-configured Banker's Algorithm and verify output matches the user-provided screenshot.
Run CPU scheduling algorithms with sample inputs to verify Gantt chart and table rendering.
