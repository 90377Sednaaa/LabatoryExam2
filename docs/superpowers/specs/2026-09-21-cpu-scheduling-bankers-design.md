# Design Specification: CPU Scheduling and Banker's Algorithm Simulation

## Overview
This project simulates fundamental Operating System resource management and process scheduling mechanisms:
1. **CPU Scheduling Algorithms**:
   - Non-Preemptive: First-Come, First-Served (FCFS) and Shortest Job First (SJF).
   - Preemptive: Shortest Remaining Time First (SRTF / Preemptive SJF) and Round Robin (RR).
   - Features: Gantt chart visualization, execution metrics per process (Completion Time, Turnaround Time, Waiting Time), and overall averages.
2. **Banker's Algorithm for Deadlock Avoidance**:
   - Safety algorithm checking whether the system is in a safe or unsafe state.
   - Computes and displays the Need Matrix.
   - Outputs the safe sequence of processes if one exists.
   - Dual-mode support: Pre-configured sample dataset (runs with no user inputs required, matching the reference output) and Custom user input matrix mode.
3. **Execution Modes**:
   - Unified interactive CLI (`main.py`).
   - Standalone execution for CPU scheduling (`cpu_scheduling.py`).
   - Standalone execution for Banker's Algorithm (`bankers_algorithm.py`).
   - Comprehensive documentation (`README.md`) and automated unit tests (`test_simulation.py`).

---

## 1. CPU Scheduling Module (`cpu_scheduling.py`)

### 1.1 Process Model
A `Process` data structure holds:
- `pid`: Process identifier string (e.g. `"P1"`, `"P2"`).
- `arrival_time`: Integer arrival time ($\ge 0$).
- `burst_time`: Integer original CPU burst time ($> 0$).
- `remaining_time`: Integer remaining burst time for preemptive scheduling.
- `completion_time`: Integer timestamp when execution finishes.
- `turnaround_time`: $CT - AT$.
- `waiting_time`: $TAT - BT$.
- `start_time`: First time the process gets CPU (optional / for response time).

### 1.2 Timeline & Gantt Chart Model
Each simulation generates a chronological list of timeline intervals:
- `(pid, start_time, end_time)` where `pid` is either the process name or `"IDLE"`.
- Adjacent intervals of the same PID are consolidated.
- ASCII Gantt Chart rendering:
  - Top & bottom borders: `+-------+-------+`
  - PID blocks: `|  P1   |  P2   |`
  - Timeline numbers: `0       4       7`

### 1.3 Scheduling Algorithms
1. **FCFS (First-Come, First-Served)**:
   - Sort available processes by arrival time.
   - Advance clock to process arrival time if CPU is idle.
   - Execute to completion ($CT = \text{current\_time} + BT$).
2. **SJF (Shortest Job First - Non-Preemptive)**:
   - At current time, inspect ready queue (processes with $AT \le \text{current\_time}$).
   - If ready queue is empty, fast-forward to next arrival time (IDLE block).
   - Select process with minimum $BT$ (tie-breaker: earlier $AT$, then $PID$).
   - Run to completion.
3. **SRTF (Shortest Remaining Time First - Preemptive SJF)**:
   - Track active processes. At each time tick, pick the arrived process with lowest `remaining_time > 0`.
   - If a newly arrived process has strictly smaller remaining time than the running process, preempt.
   - Consolidate consecutive 1-unit intervals of the same process into single Gantt chart blocks.
4. **Round Robin (RR)**:
   - Time quantum $q > 0$.
   - Maintain a FIFO ready queue.
   - Arriving processes enter the ready queue as they arrive.
   - When a process completes its slice or finishes, any newly arrived processes during that slice are enqueued before the preempted process is re-enqueued.
   - If queue is empty, advance time to next process arrival.

### 1.4 Metrics Calculation
For $n$ processes:
$$\text{Turnaround Time (TAT)} = \text{Completion Time (CT)} - \text{Arrival Time (AT)}$$
$$\text{Waiting Time (WT)} = \text{Turnaround Time (TAT)} - \text{Burst Time (BT)}$$
$$\text{Average TAT} = \frac{\sum_{i=1}^n \text{TAT}_i}{n}$$
$$\text{Average WT} = \frac{\sum_{i=1}^n \text{WT}_i}{n}$$

---

## 2. Banker's Algorithm Module (`bankers_algorithm.py`)

### 2.1 Reference / Pre-configured Dataset
Standard 5 processes ($P_0 - P_4$) and 3 resources ($A, B, C$):
- **Allocation Matrix**:
  - $P_0$: `[0, 1, 0]`
  - $P_1$: `[2, 0, 0]`
  - $P_2$: `[3, 0, 2]`
  - $P_3$: `[2, 1, 1]`
  - $P_4$: `[0, 0, 2]`
- **Maximum Matrix**:
  - $P_0$: `[7, 5, 3]`
  - $P_1$: `[3, 2, 2]`
  - $P_2$: `[9, 0, 2]`
  - $P_3$: `[2, 2, 2]`
  - $P_4$: `[4, 3, 3]`
- **Available Resources**: `[3, 3, 2]`

### 2.2 Algorithm Logic
1. **Need Matrix**:
   $$\text{Need}[i][j] = \text{Max}[i][j] - \text{Allocation}[i][j]$$
2. **Safety Check**:
   - `Work = list(Available)`
   - `Finish = [False] * num_processes`
   - `safe_sequence = []`
   - Loop up to $n$ times:
     - Find an unallocated process $i$ where $\forall j, \text{Need}[i][j] \le \text{Work}[j]$.
     - If found:
       - $\text{Work}[j] \mathrel{+}= \text{Allocation}[i][j]$
       - $\text{Finish}[i] = \text{True}$
       - Append $P_i$ to `safe_sequence`.
     - If no such process found in an iteration, break.
   - If all processes finished, state is **Safe**; otherwise **Unsafe**.

### 2.3 Custom Input Mode
When selected, prompts user for:
- Number of processes $n$ and number of resources $m$.
- Allocation matrix (row by row).
- Maximum matrix (row by row, validated: $\text{Max} \ge \text{Allocation}$).
- Available resource vector.

### 2.4 Output Formatting
Formatted to match the reference screenshot:
```text
Need Matrix:
P0: [7, 4, 3]
P1: [1, 2, 2]
P2: [6, 0, 0]
P3: [0, 1, 1]
P4: [4, 3, 1]

System is in a Safe State.
Safe Sequence: P1 -> P3 -> P4 -> P0 -> P2
```

---

## 3. Main Interface (`main.py`)
Interactive terminal menu allowing the user to:
1. Run FCFS scheduling
2. Run Non-Preemptive SJF scheduling
3. Run Preemptive SJF (SRTF) scheduling
4. Run Round Robin (RR) scheduling
5. Run Banker's Algorithm (Pre-configured sample output)
6. Run Banker's Algorithm (Custom user matrix input)
0. Exit

---

## 4. Verification and Testing Plan
- **Automated Unit Tests (`test_simulation.py`)**:
  - `test_fcfs()`: Known textbook sample with idle time and sequential arrivals.
  - `test_sjf()`: Correct shortest job selection and metrics.
  - `test_srtf()`: Preemption on shorter arrival, accurate turnaround and waiting calculations.
  - `test_round_robin()`: Queue rotation, accurate handling of arrivals coinciding with time quantum expirations.
  - `test_bankers_preconfigured()`: Verifies exact need matrix and safe sequence `['P1', 'P3', 'P4', 'P0', 'P2']`.
  - `test_bankers_unsafe()`: Verifies deadlock detection when allocation exhausts available resources without safe continuation.
- **Manual Verification**:
  - Running `python main.py` and verifying menu navigation, clean ASCII Gantt charts, tabular output, and exact match to the sample Banker's Algorithm output.
