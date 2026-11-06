import argparse
import csv
import multiprocessing as mp
import os
import platform
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


def worker(index, elements):
    x = np.linspace(0.0, 1.0, elements, dtype=np.float64)
    y = np.sqrt(x * x + index + 1.0) * np.cos(x / 3.0)
    return float(np.sum(y))


def run(p, elements):
    with mp.Pool(processes=p) as pool:
        return sum(pool.starmap(worker, [(i, elements) for i in range(p)]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--elements", type=int, default=2000000)
    parser.add_argument("--runs", type=int, default=5)
    args = parser.parse_args()
    if args.elements <= 0 or args.runs <= 0:
        raise ValueError("elements and runs must be positive")
    logical = os.cpu_count() or 2
    levels = sorted(set([1, 2, 4, 8, 16, logical]))
    levels = [p for p in levels if p <= logical]
    while len(levels) < 5:
        levels = sorted(set(levels + list(range(1, logical + 1))))
        break
    if len(levels) < 5:
        print("Warning: this computer has fewer than five processor levels")
    file = Path(__file__).resolve().parents[1] / "results.csv"
    with file.open("w", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(["timestamp_utc", "p", "run", "elements_per_worker", "total_elements", "seconds", "result", "cpu", "logical_cores"])
        for p in levels:
            for repetition in range(1, args.runs + 1):
                start = time.perf_counter()
                result = run(p, args.elements)
                seconds = time.perf_counter() - start
                writer.writerow([datetime.now(timezone.utc).isoformat(), p, repetition, args.elements, p * args.elements, f"{seconds:.8f}", f"{result:.9f}", platform.processor(), logical])
                output.flush()
                print(f"P={p} run={repetition} time={seconds:.4f}s")
    print(f"Saved {file}")


if __name__ == "__main__":
    mp.freeze_support()
    main()
