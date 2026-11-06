# Task 12:
The basic formula is S(P) = P - alpha(P - 1). It assumes a fixed parallel-system serial fraction.  Suppose the useful work takes 1 normalized time unit on P processors, and extra communication takes C(P). The serial equivalent of the useful work is alpha + P(1 - alpha).

A simple modified scaled-speedup model is:
\[S_C(P)=\frac{P-\alpha(P-1)}{1+C(P)}\]

For example, C(P) = c log2(P) or C(P) = c sqrt(P), with c greater than zero. When P increases, communication makes the denominator larger and reduces speedup. This model assumes the added communication has no equivalent useful work in the serial references. Also 
