# Task 14:
Efficiency is useful work divided by useful work plus parallel overhead. If the serial fraction is alpha, ideal Gustafson efficiency approaches 1 - alpha.

For a program with serial work A and perfectly parallel work W, the parallel runtime is A + W/P. Its speedup is (A + W)/(A + W/P). To keep efficiency at least E0, the condition is:
\[W\geq\frac{E_0}{1-E_0}(P-1)A\]

If A stays constant, W must grow at least as O(P). This is a linear isoefficiency function. If communication overhead H(P,W) grows, the general condition becomes W = K P H(P,W), where K depends on the target efficiency. Then more than linear growth may be needed.