import csv
import platform
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main():
    folder = Path(__file__).resolve().parent
    if not (folder / "summary.csv").exists() or not (folder / "fit.txt").exists():
        raise FileNotFoundError("Run benchmark.py and fit_gustafson.py first")
    with (folder / "summary.csv").open(newline="") as file:
        rows = list(csv.DictReader(file))
    p = np.array([int(r["p"]) for r in rows], dtype=float)
    speed = np.array([float(r["scaled_speedup"]) for r in rows])
    mean = np.array([float(r["mean_seconds"]) for r in rows])
    sem = np.array([float(r["standard_error_seconds"]) for r in rows])
    alpha = float((folder / "fit.txt").read_text().splitlines()[0].split("=")[1])
    error = speed * sem / mean
    plt.figure(figsize=(8, 5))
    plt.plot(p, p, label="Ideal")
    plt.plot(p, p - alpha * (p - 1), label="Gustafson fit")
    plt.plot(p, 1 / (alpha + (1 - alpha) / p), label="Amdahl model")
    plt.errorbar(p, speed, yerr=error, fmt="o", capsize=3, label="Measured")
    plt.xlabel("Processes")
    plt.ylabel("Scaled speedup")
    plt.title("Weak Scaling Comparison")
    plt.legend()
    plt.grid(alpha=0.2)
    plt.tight_layout()
    out = folder.parent / "plots" / "scaling_comparison.png"
    plt.savefig(out, dpi=250)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
