# Task 15: Energy

Let each active processor use P_idle + P_active watts and let the wall-clock time be T.

For one processor:

\[E_1=(P_{idle}+P_{active})T\]

For P identical processors running for the same time:

\[E_P=P(P_{idle}+P_{active})T\]

So E_P / E_1 = P in this simplified model. The P-processor run also completes a larger workload under weak scaling. Energy per unit of useful work can remain similar even when total energy increases. Network and cooling power would add extra energy in a real cluster.
