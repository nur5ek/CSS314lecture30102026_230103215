# Task 03:
The two laws measure the serial fraction in different situations. Amdahl measures the serial part of a fixed workload on one processor. Gustafson measures the serial time as a fraction of the runtime on the parallel system with a larger workload. For example, a small serial step can remain the same while the parallel part grows with the number of processors. Its fraction of the total single-processor work becomes smaller even if its absolute time does not change.

There is no contradiction. The laws use different workloads and different reference times. Gustafson does not prove that serial work disappears. If serial work or communication grows with P, the scaled speedup can still become poor
