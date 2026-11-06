# Task 04: 
Gustafson efficiency is:
\[E_G(P)=\frac{P-\alpha(P-1)}{P}=1-\alpha+\frac{\alpha}{P}\]

When P approaches infinity:
\[\lim_{P\to\infty} E_G(P)=1-\alpha\]

For Amdahl, using a fixed serial fraction s:
\[S_A(P)=\frac{1}{s+(1-s)/P}\]

\[E_A(P)=\frac{1}{Ps+(1-s)}\]

For s greater than zero, the Amdahl efficiency limit is 0. If s = 0, it is 1. Gustafson efficiency stays near 1 - alpha only if alpha remains constant as the workload grows.
