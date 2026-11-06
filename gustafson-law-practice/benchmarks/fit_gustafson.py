import csv
from pathlib import Path

import numpy as np


def main():
    folder = Path(__file__).resolve().parent
    path = folder / "results.csv"
    if not path.exists():
        raise FileNotFoundError("Run weak_scale_bench/benchmark.py first")
    grouped = {}
    with path.open(newline="") as file:
        for row in csv.DictReader(file):
            grouped.setdefault(int(row["p"]), []).append(float(row["seconds"]))
    if len(grouped) < 5 or any(len(v) < 5 for v in grouped.values()):
        raise ValueError("Need at least five processor levels and five runs each")
    stats = {p: (float(np.mean(v)), float(np.std(v, ddof=1))) for p, v in grouped.items()}
    t1 = stats[1][0]
    rows = []
    for p in sorted(stats):
        mean, std = stats[p]
        scaled = p * t1 / mean
        rows.append((p, mean, std, scaled, std / np.sqrt(len(grouped[p]))))
    x = np.array([p - 1 for p, _, _, _, _ in rows], dtype=float)
    y = np.array([p - scaled for p, _, _, scaled, _ in rows], dtype=float)
    alpha = float(np.dot(x, y) / np.dot(x, x))
    with (folder / "summary.csv").open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["p", "mean_seconds", "std_seconds", "scaled_speedup", "standard_error_seconds"])
        writer.writerows(rows)
    (folder / "fit.txt").write_text(f"Fitted alpha = {alpha:.8f}\nMeasured scaled speedup = P * mean_T1 / mean_TP\n", encoding="utf8")
    print(f"Fitted alpha: {alpha:.6f}")
    print("Saved summary.csv and fit.txt")


if __name__ == "__main__":
    main()
