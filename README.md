01-N
\*\*Student ID:\*\* 230103215



\## Project Overview



This project studies memory locality, false sharing, parallel scaling, and performance optimization using Python.



\## Milestones



\- \*\*M0 — Host Profiling:\*\* Collected CPU, cache, operating system, and Python environment information. Generated student-specific parameters.

\- \*\*M1 — Memory Locality:\*\* Compared different memory access strides and measured the performance improvement from loop interchange.

\- \*\*M2 — False Sharing:\*\* Compared unpadded, padded, and privatized counters using multiprocessing. Calculated Karp-Flatt metrics.

\- \*\*M3 — Scaling and Roofline:\*\* Evaluated strong and weak scaling using a 2D stencil kernel and performed a Roofline analysis.



\## Key Results



\- CPU: Intel Core i7-12650H

\- Physical cores: 10

\- Logical threads: 16

\- Matrix dimension: 1536

\- Loop interchange speedup: 13.43x

\- Stride 8 latency: 4.30x higher than stride 1

\- Arithmetic intensity: 0.1042 FLOPs/byte

\- Roofline classification: Memory-Bandwidth Bound



\## Verification



All four milestones passed the automated verification script.



The verification receipt is available at:



`results/verification\_receipt.sig`



\## Technologies



\- Python 3.12

\- NumPy

\- Numba

\- Multiprocessing

\- JSON and TSV

\- Git and GitHub

