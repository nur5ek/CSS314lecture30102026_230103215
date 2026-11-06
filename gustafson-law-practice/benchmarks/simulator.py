import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--alpha", type=float, default=0.04)
    parser.add_argument("--max-p", type=int, default=65536)
    args = parser.parse_args()
    if not 0.001 <= args.alpha <= 0.20 or not 1 <= args.max_p <= 65536:
        raise ValueError("alpha must be 0.001..0.20 and max-p must be 1..65536")
    folder = Path(__file__).resolve().parent
    rows = []
    for p in range(1, args.max_p + 1):
        amdahl = 1.0 / (args.alpha + (1 - args.alpha) / p)
        gustafson = p - args.alpha * (p - 1)
        rows.append((p, args.alpha, amdahl, gustafson))
    with (folder / "simulator_results.csv").open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["p", "alpha", "amdahl", "gustafson"])
        writer.writerows(rows)
    sampled = [row for row in rows if row[0] == 1 or row[0] & (row[0] - 1) == 0]
    plt.plot([r[0] for r in sampled], [r[2] for r in sampled], label="Amdahl")
    plt.plot([r[0] for r in sampled], [r[3] for r in sampled], label="Gustafson")
    plt.xscale("log", base=2)
    plt.xlabel("Processors")
    plt.ylabel("Speedup")
    plt.legend()
    plt.tight_layout()
    plt.savefig(folder.parent / "plots" / "simulator_comparison.png", dpi=200)
    print("Saved simulator_results.csv and simulator_comparison.png")


if __name__ == "__main__":
    main()
