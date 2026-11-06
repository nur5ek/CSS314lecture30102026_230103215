# Task 05:
The task sheet describes the 1988 Gustafson, Montry, and Benner experiments on a 1,024-processor nCUBE system and reports scaled speedups above 1,000. The important point is that the researchers increased the problem size when they used more processors.

If the parallel-system serial fraction is 0.004, Gustafson's formula predicts:
S(1024) = 1024 - 0.004(1023) = 1019.908.

Amdahl's fixed-size formula with s = 0.004 predicts about 201.09 on 1,024 processors and an upper limit of 250. These are different workload assumptions. The expanded problem makes high scaled speedup possible. The sheet does not provide raw historical timing data, so this is a model calculation, not a reproduction of the original measurements.
