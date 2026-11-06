# Task 17: 3D Stencil

A cubic domain with side N has O(N^3) cell updates. Its surface has O(N^2) cells. The surface-to-volume ratio is O(1/N).

If the global volume grows with P, then N_global grows as P^(1/3). The global surface-to-volume ratio improves as P^(-1/3).

However, for a domain split across P processors with constant local cube size, each processor has about the same amount of boundary data and compute work. The local communication-to-compute ratio stays approximately constant, not smaller. Network congestion and synchronization can still make runtime increase.
