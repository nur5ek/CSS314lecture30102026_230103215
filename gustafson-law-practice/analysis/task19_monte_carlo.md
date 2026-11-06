# Task 19: Monte Carlo

Monte Carlo paths can usually run independently. That makes it a good weak-scaling example. Small serial parts still exist: generating unique random seeds, starting workers, collecting results, and saving output.

A tree reduction of one result per worker has about log2(P) stages when the network allows concurrent communication. If each stage takes c time, a simple overhead model is C(P) = c log2(P).

The modified scaled speedup can be estimated as [P - alpha(P - 1)] / [1 + c log2(P)]. More workers still help, but the reduction and startup costs stop performance from being perfectly linear.
