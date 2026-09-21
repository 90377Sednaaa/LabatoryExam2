"""
Operating Systems Simulation - Main Entrypoint
Laboratory Exam 2

This interactive program allows users to simulate:
- CPU Scheduling Algorithms:
    * Non-preemptive: First-Come, First-Served (FCFS), Shortest Job First (SJF)
    * Preemptive: Shortest Remaining Time First (SRTF), Round Robin (RR)
- Deadlock Avoidance:
    * Banker's Algorithm (Pre-configured sample & Custom matrix input)
"""

import sys
from cpu_scheduling import run_interactive_scheduling
from bankers_algorithm import run_preconfigured_bankers, run_custom_bankers


def print_banner() -> None:
    """Displays the application title banner."""
    print("=" * 64)
    print("   OPERATING SYSTEMS SIMULATION - LABORATORY EXAM 2    ")
    print("   CPU Scheduling & Banker's Algorithm Deadlock Avoidance")
    print("=" * 64)


def print_menu() -> None:
    """Displays the available simulation choices."""
    print("\n[CPU Scheduling Algorithms]")
    print("  1. First-Come, First-Served (FCFS)         [Non-Preemptive]")
    print("  2. Shortest Job First (SJF)                [Non-Preemptive]")
    print("  3. Shortest Remaining Time First (SRTF)    [Preemptive SJF]")
    print("  4. Round Robin (RR)                        [Preemptive]")
    print("\n[Deadlock Avoidance - Banker's Algorithm]")
    print("  5. Banker's Algorithm (Pre-configured Sample Output)")
    print("  6. Banker's Algorithm (Custom User Matrix Input)")
    print("\n[System]")
    print("  0. Exit Program")
    print("-" * 64)


def get_input(prompt: str = "") -> str:
    """Reads input and strips whitespace and potential UTF-8 BOM on Windows."""
    return input(prompt).strip().replace("\ufeff", "")


def main() -> None:
    """Main application loop."""
    print_banner()
    
    while True:
        print_menu()
        choice = get_input("Enter your choice [0-6]: ")
        
        if choice == "0":
            print("\nThank you for using the OS Simulator. Goodbye!\n")
            sys.exit(0)
        elif choice in {"1", "2", "3", "4"}:
            run_interactive_scheduling(choice)
        elif choice == "5":
            run_preconfigured_bankers()
        elif choice == "6":
            run_custom_bankers()
        else:
            print("\n[!] Invalid choice. Please select a valid number from 0 to 6.")
            
        input("\nPress Enter to return to the main menu...")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nOperation cancelled or end of input. Exiting...\n")
        sys.exit(0)
