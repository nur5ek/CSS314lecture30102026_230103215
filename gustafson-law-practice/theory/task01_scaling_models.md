# Task 01

Amdahl's law assumes the total work stays the same when processors are added. Each processor gets a smaller part of the work. As P grows, the serial part limits the speedup. This is strong scaling. Gustafson's law assumes that the problem grows with P. Each processor can keep about the same amount of useful work, while the total running time stays roughly constant. This is weak scaling.

For Amdahl, W(P) = W(1). For ideal Gustafson scaling W(P) is proportional to P. Fixed size means the work is fixed. Fixed-time means the time budget is fixed while the work increses.
