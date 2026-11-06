# Gustafson's Law and Weak Scaling

Parallel and Distributed Computing Architecture  
Practice tasks 01–25

## Folders

- `theory/` — Tasks 01–05 and 11–15
- `calculations/` — Tasks 06–10 and 16–17
- `analysis/` — Tasks 18–20 and 24
- `benchmarks/` — Tasks 21–23 and plotting code
- `plots/` — generated graphs

## Setup

Use Python 3.10 or newer.

```bash
python -m pip install -r requirements.txt
```

## Task 21: Simulator

```bash
python benchmarks/simulator.py --alpha 0.04 --max-p 65536
```

This creates `benchmarks/simulator_results.csv` and `plots/simulator_comparison.png`.

## Tasks 22–24: Real benchmark

```bash
python benchmarks/weak_scale_bench/benchmark.py --elements 2000000 --runs 5
python benchmarks/fit_gustafson.py
python benchmarks/plot_results.py
```

The first command takes time because it runs five repetitions at each process level. It saves the raw data to `benchmarks/results.csv`. The next commands calculate the mean, standard deviation, fitted serial fraction, and comparison plot.

Do not edit the measured CSV data. Results depend on the computer and background processes.

## Task 25: Summary

Amdahl's law is useful when the problem size stays fixed. Gustafson's law is useful when the problem can grow with the number of processors. In the ideal weak-scaling model, efficiency approaches 1 - alpha. Real programs also have startup, communication, synchronization, and memory costs.

The theoretical tasks explain these limits. The calculation tasks show the formulas with numbers. The benchmark scripts let me compare the formulas with actual timings.
