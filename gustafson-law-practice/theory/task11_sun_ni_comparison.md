# Task 11:
Amdahl keeps the workload fixed. Gustafson grows the workload to use a roughly fixed time. Sun-Ni looks at how the workload can grow when more memory is available.

Let W(P) be the problem size supported by P processors. A simple memory-bounded model is S_M(P) = T_1(W(P)) / T_P(W(P)). The workload is chosen by memory capacity instead of only by a fixed time target.

Gustafson can overestimate performance if communication, memory access, or serial work grows with P. It can underestimate useful growth when extra memory allows a much larger problem with better computational intensity. The actual result depends on the algorithm and hardware.
