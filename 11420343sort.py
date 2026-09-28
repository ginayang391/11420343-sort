#!/usr/bin/env python3
#11420343楊詠晴
"""
Interactive Sorting Algorithm Tool
===================================

A command-line application implementing three classic sorting algorithms
(Bubble Sort, Selection Sort, Insertion Sort) with flexible data input
(manual entry or CSV import), configurable sort direction, and a
continuous interactive loop.

Includes an execution-time comparison mode so the three algorithms can be
benchmarked against each other on the same dataset.

Uses only the Python standard library (csv, os, sys, time).
"""

from __future__ import annotations

import csv
import os
import sys
import time
from typing import List, Optional, Union

Number = Union[int, float]


# ---------------------------------------------------------------------------
# Sorting Algorithms
# ---------------------------------------------------------------------------

def bubble_sort(
    arr: List[Number], reverse: bool = False, track_steps: bool = False
):
    """Sort a list using Bubble Sort.

    Returns the sorted list, or (sorted_list, steps) when track_steps=True,
    where `steps` is a list of list-snapshots taken after each swap.
    """
    result = arr.copy()
    steps: Optional[List[List[Number]]] = [] if track_steps else None
    n = len(result)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            should_swap = (
                result[j] > result[j + 1]
                if not reverse
                else result[j] < result[j + 1]
            )
            if should_swap:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
                if track_steps:
                    steps.append(result.copy())
        if not swapped:
            break
    return (result, steps) if track_steps else result


def selection_sort(
    arr: List[Number], reverse: bool = False, track_steps: bool = False
):
    """Sort a list using Selection Sort.

    Returns the sorted list, or (sorted_list, steps) when track_steps=True,
    where `steps` is a list of list-snapshots taken after each swap.
    """
    result = arr.copy()
    steps: Optional[List[List[Number]]] = [] if track_steps else None
    n = len(result)
    for i in range(n):
        target_idx = i
        for j in range(i + 1, n):
            is_better = (
                result[j] < result[target_idx]
                if not reverse
                else result[j] > result[target_idx]
            )
            if is_better:
                target_idx = j
        if target_idx != i:
            result[i], result[target_idx] = result[target_idx], result[i]
            if track_steps:
                steps.append(result.copy())
    return (result, steps) if track_steps else result


def insertion_sort(
    arr: List[Number], reverse: bool = False, track_steps: bool = False
):
    """Sort a list using Insertion Sort.

    Returns the sorted list, or (sorted_list, steps) when track_steps=True,
    where `steps` is a list of list-snapshots taken after each element is
    inserted into its correct position.
    """
    result = arr.copy()
    steps: Optional[List[List[Number]]] = [] if track_steps else None
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and (
            (result[j] > key) if not reverse else (result[j] < key)
        ):
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
        if track_steps:
            steps.append(result.copy())
    return (result, steps) if track_steps else result


SORT_ALGORITHMS = {
    "1": ("Bubble Sort", bubble_sort),
    "2": ("Selection Sort", selection_sort),
    "3": ("Insertion Sort", insertion_sort),
}


# ---------------------------------------------------------------------------
# Input Handling
# ---------------------------------------------------------------------------

def parse_numbers(raw_text: str) -> List[Number]:
    """Parse a string of numbers separated by spaces, commas, or newlines.

    Non-numeric tokens are skipped with a warning.
    """
    tokens = []
    for line in raw_text.splitlines():
        for chunk in line.replace(",", " ").split():
            tokens.append(chunk)

    numbers: List[Number] = []
    for token in tokens:
        value = _to_number(token)
        if value is None:
            print(f"[Warning] Skipping non-numeric value: '{token}'")
            continue
        numbers.append(value)
    return numbers


def _to_number(token: str):
    """Convert a string token to int or float. Returns None if invalid."""
    token = token.strip()
    if not token:
        return None
    try:
        as_int = int(token)
        return as_int
    except ValueError:
        pass
    try:
        return float(token)
    except ValueError:
        return None


def read_manual_input() -> List[Number]:
    """Prompt the user for manually-entered numbers.

    Supports space-, comma-, or newline-separated values. The user
    finishes entry by submitting an empty line.
    """
    print("\nEnter numbers separated by spaces or commas.")
    print("You may enter multiple lines; submit an empty line to finish.\n")

    lines = []
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        if line.strip() == "":
            break
        lines.append(line)

    numbers = parse_numbers("\n".join(lines))
    print(f"\n[Success] {len(numbers)} number(s) entered.")
    return numbers


def read_csv_input() -> List[Number]:
    """Prompt for a CSV path and extract all numeric values from it.

    Handles single-row, single-column, or grid formats. Non-numeric
    cells are skipped with a warning.
    """
    path = input("\nEnter CSV file path: ").strip().strip('"').strip("'")

    if not path:
        print("[Error] No file path provided.")
        return []

    if not os.path.isfile(path):
        print(f"[Error] File not found: '{path}'")
        return []

    numbers: List[Number] = []
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            for row in reader:
                for cell in row:
                    value = _to_number(cell)
                    if value is None:
                        if cell.strip() != "":
                            print(f"[Warning] Skipping non-numeric cell: '{cell}'")
                        continue
                    numbers.append(value)
    except (OSError, csv.Error) as exc:
        print(f"[Error] Unable to read CSV file: {exc}")
        return []

    if numbers:
        preview = numbers if len(numbers) <= 10 else numbers[:10] + ["..."]
        print(f"[Success] Loaded {len(numbers)} number(s) from '{path}': {preview}")
    else:
        print(f"[Warning] No numeric values found in '{path}'.")

    return numbers


# ---------------------------------------------------------------------------
# CLI Handler
# ---------------------------------------------------------------------------

def print_header() -> None:
    print("=" * 50)
    print("           SORTING ALGORITHM SUITE")
    print("=" * 50)


def choose_input_method() -> List[Number]:
    while True:
        print("\nSelect Input Method:")
        print("  1. Manual console input (space/comma-separated)")
        print("  2. Load from .csv file")
        print("  3. Exit program")
        choice = input("> ").strip()

        if choice == "1":
            return read_manual_input()
        elif choice == "2":
            return read_csv_input()
        elif choice == "3":
            print("\nGoodbye!")
            sys.exit(0)
        else:
            print("[Warning] Invalid choice. Please enter 1, 2, or 3.")


COMPARE_ALL_CHOICE = "4"


def choose_algorithm() -> tuple[str, Optional[callable]]:
    """Prompt for a sorting algorithm.

    Returns (name, func) for a single algorithm, or ("Compare All Three",
    None) as a sentinel meaning "benchmark all three algorithms".
    """
    while True:
        print("\nSelect Sorting Algorithm:")
        print("  1. Bubble Sort")
        print("  2. Selection Sort")
        print("  3. Insertion Sort")
        print("  4. Compare All Three (execution time)")
        choice = input("> ").strip()
        if choice in SORT_ALGORITHMS:
            return SORT_ALGORITHMS[choice]
        if choice == COMPARE_ALL_CHOICE:
            return "Compare All Three", None
        print("[Warning] Invalid choice. Please enter 1, 2, 3, or 4.")


def choose_order() -> tuple[str, bool]:
    while True:
        print("\nSelect Order:")
        print("  1. Increasing (Small to Large)")
        print("  2. Decreasing (Large to Small)")
        choice = input("> ").strip()
        if choice == "1":
            return "Increasing", False
        elif choice == "2":
            return "Decreasing", True
        print("[Warning] Invalid choice. Please enter 1 or 2.")


def choose_yes_no(prompt: str) -> bool:
    """Prompt for a y/n answer and return True for yes, False for no."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False
        print("[Warning] Please enter 'y' or 'n'.")


MAX_CONSOLE_STEPS = 30


def display_steps(steps: List[List[Number]], algo_name: str) -> None:
    """Print the step-by-step transformation of the list during sorting.

    If there are too many steps to usefully print (large datasets can
    produce thousands of swaps), the full log is saved to a text file in
    the current folder instead, with a short preview shown on screen.
    """
    print(f"\n{'=' * 50}")
    print(f"Sorting Process ({algo_name}) - {len(steps)} step(s)")
    print("=" * 50)

    if not steps:
        print("[Info] No swaps/moves were needed (data may already be sorted).")
        print("=" * 50)
        return

    if len(steps) <= MAX_CONSOLE_STEPS:
        for idx, state in enumerate(steps, start=1):
            print(f"Step {idx:>4}: {state}")
    else:
        filename = f"{algo_name.replace(' ', '_').lower()}_steps.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                for idx, state in enumerate(steps, start=1):
                    f.write(f"Step {idx}: {state}\n")
            print(
                f"[Info] {len(steps)} steps is too many to print here, so the "
                f"full process was saved to '{filename}' in the current folder."
            )
        except OSError as exc:
            print(f"[Warning] Could not save step log to file: {exc}")

        preview_n = 5
        print(f"\nPreview (first {preview_n} steps):")
        for idx, state in enumerate(steps[:preview_n], start=1):
            print(f"Step {idx:>4}: {state}")
        print("...")
        print(f"Preview (last {preview_n} steps):")
        start_idx = len(steps) - preview_n + 1
        for idx, state in enumerate(steps[-preview_n:], start=start_idx):
            print(f"Step {idx:>4}: {state}")

    print("=" * 50)


def time_sort(func, numbers: List[Number], reverse: bool, repeats: int = 5):
    """Run a sort function `repeats` times and return (result, avg_seconds).

    Averaging over several runs smooths out timing noise, which matters
    most for small datasets that sort almost instantly.
    """
    best_result = None
    total_elapsed = 0.0
    for _ in range(repeats):
        start = time.perf_counter()
        best_result = func(numbers, reverse)
        total_elapsed += time.perf_counter() - start
    return best_result, total_elapsed / repeats


def run_comparison(numbers: List[Number], order_name: str, reverse: bool) -> None:
    """Run all three algorithms on the same data and compare timing."""
    benchmarks = []
    for _, (name, func) in SORT_ALGORITHMS.items():
        sorted_result, avg_seconds = time_sort(func, numbers, reverse)
        benchmarks.append((name, avg_seconds, sorted_result))

    benchmarks.sort(key=lambda item: item[1])
    reference_result = benchmarks[0][2]
    all_agree = all(result == reference_result for _, _, result in benchmarks)

    print("\n" + "-" * 50)
    print(f"Original Count: {len(numbers)}")
    print(f"Direction: {order_name}")
    print(f"Original: {numbers}")
    print("-" * 50)
    print(f"{'Rank':<5}{'Algorithm':<18}{'Avg Time (ms)':<16}")
    for rank, (name, avg_seconds, _) in enumerate(benchmarks, start=1):
        print(f"{rank:<5}{name:<18}{avg_seconds * 1000:<16.4f}")
    print("-" * 50)
    print(f"Fastest: {benchmarks[0][0]}  |  Slowest: {benchmarks[-1][0]}")
    print(f"Results match across all algorithms: {all_agree}")
    print(f"Sorted Result: {reference_result}")
    print("-" * 50)


def run_sort_session(numbers: List[Number]) -> None:
    """Run a single sort configuration + display the results."""
    if not numbers:
        print("\n[Warning] No data available to sort. Please provide input first.")
        return

    algo_name, algo_func = choose_algorithm()
    order_name, reverse = choose_order()

    if algo_func is None:
        run_comparison(numbers, order_name, reverse)
        return

    show_process = choose_yes_no(
        "\nShow the step-by-step sorting process? (y/n): "
    )

    if show_process:
        sorted_result, steps = algo_func(numbers, reverse, track_steps=True)
    else:
        sorted_result, avg_seconds = time_sort(algo_func, numbers, reverse)

    print("\n" + "-" * 50)
    print(f"Original Count: {len(numbers)}")
    print(f"Algorithm: {algo_name}")
    print(f"Direction: {order_name}")
    print(f"Original: {numbers}")
    print(f"Result:   {sorted_result}")
    if not show_process:
        print(f"Avg Execution Time: {avg_seconds * 1000:.4f} ms (averaged over 5 runs)")
    print("-" * 50)

    if show_process:
        display_steps(steps, algo_name)


def main() -> None:
    current_data: List[Number] = []

    while True:
        print_header()

        if current_data:
            print(f"\n[Info] Current dataset in memory: {len(current_data)} number(s).")
            print("  1. Use existing data")
            print("  2. Load new data")
            print("  3. Exit program")
            choice = input("> ").strip()
            if choice == "1":
                pass  # keep current_data
            elif choice == "2":
                current_data = choose_input_method()
            elif choice == "3":
                print("\nGoodbye!")
                sys.exit(0)
            else:
                print("[Warning] Invalid choice.")
                continue
        else:
            current_data = choose_input_method()

        run_sort_session(current_data)

        while True:
            again = input("\nTest another dataset or algorithm? (y/n): ").strip().lower()
            if again in ("y", "yes"):
                break
            elif again in ("n", "no"):
                print("\nGoodbye!")
                sys.exit(0)
            else:
                print("[Warning] Please enter 'y' or 'n'.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
        sys.exit(0)
