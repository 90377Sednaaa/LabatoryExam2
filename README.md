# Operating Systems Simulation: CPU Scheduling & Banker's Algorithm

**Laboratory Exam 2**  
A modular, fully commented Python simulation demonstrating core Operating System process management and deadlock avoidance concepts.

---

## 📋 Features

### 1. CPU Scheduling Algorithms
Simulates both non-preemptive and preemptive CPU scheduling algorithms:
- **First-Come, First-Served (FCFS)** `[Non-Preemptive]`
- **Shortest Job First (SJF)** `[Non-Preemptive]`
- **Shortest Remaining Time First (SRTF / Preemptive SJF)** `[Preemptive]`
- **Round Robin (RR)** `[Preemptive]` (with configurable Time Quantum)

**Outputs Provided:**
- Chronological ASCII **Gantt Chart** detailing process execution and any CPU `IDLE` time.
- Detailed metrics table: **Arrival Time (AT)**, **Burst Time (BT)**, **Completion Time (CT)**, **Turnaround Time (TAT)**, and **Waiting Time (WT)**.
- **Average Turnaround Time** and **Average Waiting Time**.

### 2. Banker's Algorithm (Deadlock Avoidance)
Implements Dijkstra's Banker's Algorithm to test system safety and compute safe execution sequences:
- **Pre-configured Mode (Default)**: Instantly runs with the laboratory exam reference dataset (5 processes $P_0-P_4$ and 3 resources $A, B, C$) with **no user inputs required**, matching the sample output screenshot.
- **Custom Input Mode**: Allows users to input their own number of processes, resources, Allocation matrix, Max matrix, and Available vector.
- **Outputs Provided**:
  - Computed **Need Matrix** ($\text{Need} = \text{Max} - \text{Allocation}$)
  - System Safety State (`Safe State` or `Unsafe State`)
  - **Safe Sequence** of processes (e.g., `P1 -> P3 -> P4 -> P0 -> P2`)

---

## 🛠️ Requirements & Prerequisites

- **Python 3.8+** (Standard Library only; no `pip` installations or third-party packages required).
- Compatible with Windows (Command Prompt / PowerShell), macOS, and Linux terminals.

---

## 🚀 How to Run the Programs

You can run the simulation using either the unified interactive dashboard or as individual standalone modules:

### Option A: Unified Interactive Menu (`main.py`)
Run the master controller:
```bash
python main.py
```
This opens an interactive menu:
```text
================================================================
   OPERATING SYSTEMS SIMULATION - LABORATORY EXAM 2    
   CPU Scheduling & Banker's Algorithm Deadlock Avoidance
================================================================

[CPU Scheduling Algorithms]
  1. First-Come, First-Served (FCFS)         [Non-Preemptive]
  2. Shortest Job First (SJF)                [Non-Preemptive]
  3. Shortest Remaining Time First (SRTF)    [Preemptive SJF]
  4. Round Robin (RR)                        [Preemptive]

[Deadlock Avoidance - Banker's Algorithm]
  5. Banker's Algorithm (Pre-configured Sample Output)
  6. Banker's Algorithm (Custom User Matrix Input)

[System]
  0. Exit Program
----------------------------------------------------------------
Enter your choice [0-6]:
```

---

### Option B: Standalone Banker's Algorithm (`bankers_algorithm.py`)
Run directly:
```bash
python bankers_algorithm.py
```
- Select `1` (or press **Enter**) to instantly output the pre-configured sample output without entering any numbers.
- Select `2` to enter your own custom matrices.

---

### Option C: Standalone CPU Scheduling (`cpu_scheduling.py`)
Run directly:
```bash
python cpu_scheduling.py
```
Select any scheduling algorithm (`1` through `4`), enter the number of processes, and enter their Arrival and Burst times.

---

## 📊 Sample Outputs

### Banker's Algorithm Sample Output
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

### CPU Scheduling Sample Output (Round Robin, Quantum = 2)
```text
=================================================================
  CPU Scheduling Results: Round Robin
=================================================================

Gantt Chart:
+-------+-------+-------+-------+-------+-------+
|   P1  |   P2  |   P3  |   P1  |   P2  |   P1  |
+-------+-------+-------+-------+-------+-------+
0       2       4       5       7       8       9

Process Execution Details:
----------------------------------------------------------------------------------------
Process   | Arrival Time | Burst Time | Completion Time | Turnaround Time | Waiting Time
----------------------------------------------------------------------------------------
P1        | 0            | 5          | 9               | 9               | 4           
P2        | 1            | 3          | 8               | 7               | 4           
P3        | 2            | 1          | 5               | 3               | 2           
----------------------------------------------------------------------------------------

Average Turnaround Time : 6.33
Average Waiting Time    : 3.33
=================================================================
```

---

## 📂 Project Structure

```text
LabatoryExam2/
├── main.py                      # Interactive CLI launcher uniting all simulations
├── cpu_scheduling.py            # Process model, FCFS, SJF, SRTF, RR & Gantt renderer
├── bankers_algorithm.py         # Need matrix computation & Banker's safety algorithm
├── Sample_Input_and_Output.docx # Word document with program execution screenshots
├── screenshots/                 # High-resolution execution screenshots
└── README.md                    # Project documentation and run guide
```
