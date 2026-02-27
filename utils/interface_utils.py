import time
from typing import Callable, Any


def start_mission_control() -> int:
    """
    Displays the agency's command center menu and captures the agent's choice.

    Returns:
        int: The selected operation mode (0-3).
    """
    print("=" * 54)
    print("🏠  WELCOME TO THE IMMO-ELIZA INTELLIGENCE AGENCY  🏠")
    print("=" * 54)
    print("Agent, select your operational module:")
    print("  [1] 🏎️  Turbo-Crawler  : Discover hidden property URLs")
    print("  [2] 🕷️  Super-Scraper  : Extract details from listings")
    print("  [3] 🧹  Master-Cleaner : Sanitize the raw data (CSV)")
    print("  [0] 🚪  Exit Agency    : Terminate current session")
    print("-" * 54)

    while True:
        try:
            # Capture input and strip whitespace to prevent accidental errors
            choice = input("👉 Enter module number (1, 2, 3 or 0): ").strip()

            # Attempt conversion to integer
            choice_int = int(choice)

            # Validate that the choice exists in our protocol
            if choice_int in [0, 1, 2, 3]:
                return choice_int

            print(f"🚫 Error 404: Module '{choice_int}' not found. Use 0, 1, 2, or 3.")

        except ValueError:
            # Handle non-numeric inputs gracefully
            print("⚠️ Unauthorized input! Use numerical coordinates (0-3) only.")


def execute_mission(task_name: str, task_function: Callable, *args: Any) -> int:
    """
    Orchestrates the execution of a specific mission with dynamic arguments.

    Args:
        task_name (str): The identifier for the mission (e.g., 'CRAWLING').
        task_function (Callable): The technical logic to be executed.
        *args: Variable length argument list for the task_function.

    Returns:
        int: The total count of items successfully retrieved or processed.
    """
    print(f"\n{'—' * 30} {task_name} MISSION {'—' * 30}")

    # High-precision timer to measure mission efficiency
    start_time = time.perf_counter()

    # Execute the function with the passed arguments
    # The * and ** unpack the arguments into the function call
    result_count = task_function(*args)

    # Calculate total duration in minutes
    duration = (time.perf_counter() - start_time) / 60

    print(f"{'—' * 78}")
    print(f"⏱️  Duration: {duration:.1f} minutes")
    if result_count and result_count > 0:
        print(f"📊 Total items processed: {result_count}")
    print(f"{'—' * 78}\n")

    return result_count
