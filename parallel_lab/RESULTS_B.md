# Parallel Computing Performance Lab (Variant B) - Scalability Diagnostics

## Multi-Core Performance & Diagnostic Matrix

| Configuration | $T_1$ (s) | $T_2$ (s) | $T_4$ (s) | $T_8$ (s) | $S_8$ | $e(2)$ | $e(8)$ | Verdict |
| **A: Micro ($k=1$)** | 38.443 | 32.673 | 43.157 | 50.272 | 0.76x | High | High | Master dispatch serialization |
| **B: Queue Choke** | 2.327 | 5.170 | 5.536 | 5.606 | 0.42x | 3.398 | 2.583 | IPC lock contention explosion |
| **C: Buffered Batch** | 0.588 | 0.353 | 0.307 | 0.256 | 2.30x | 0.200 | 0.355 | Amortized synchronization |


## Empirical Conclusions & Diagnostics

1. **Experiment A (The Granularity Trap):** Executing micro-tasks (`chunksize=1`) causes master process dispatch and serialization overheads to dominate execution time. Scaling to 8 cores actually increases execution time from 38.44s to 50.27s ($S_8 = 0.76x$).
2. **Experiment B (IPC Queue Choke-Point):** Frequent unbuffered calls to `Queue.put()` create severe OS pipe lock contention and context-switching overheads. This results in negative scaling ($S_8 = 0.42x$) and a surging Karp-Flatt metric ($e(8) = 2.583$).
3. **Experiment C (Local Buffer Aggregation):** Pre-aggregating data into local buffers of 10,000 items amortizes IPC overhead. This allowed the system to process 25x more data (10,000,000 items vs 400,000 items) in just 0.256 seconds while restoring positive speedup ($S_8 = 2.30x$).
