# Task 02

Let the runtime on P processors be s+p = 1. Here s is the time spent in serial work and p is the time spent in parallel work. The same scaled workload on one processor takes s + Pp, because the parallel portion has to be done by one processor.

Therefore:

\[S(P)=\frac{s+Pp}{s+p}=s+Pp\]

Since p = 1 - s:
\[S(P)=s+P(1-s)=P-s(P-1)\]

Writing the serial fraction as alpha gives:
\[S(P)=P-\alpha(P-1)\]

This assumes the parallel work is divided evenly and ignores extra communication costs.
