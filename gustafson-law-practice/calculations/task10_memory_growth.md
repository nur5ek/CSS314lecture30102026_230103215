# Task 10: Memory and a 3D Grid

Let each grid cell need b bytes and let N be the side length of a cubic grid. The memory needed for one grid is bN^3. If each node has 32 GiB, the maximum local side length is:

N_local = floor((32 * 2^30 / b)^(1/3)).

With 64 nodes, total memory is 2048 GiB. With 512 nodes, total memory is 16384 GiB. If the full grid is distributed evenly, the maximum global side length is:

N_global(P) = floor((P * 32 * 2^30 / b)^(1/3)).

For an example using one 8-byte value per cell, N_global(64) = 6501 and N_global(512) = 13003. The global side length doubles when the node count increases eight times. Extra arrays, halo cells, and program memory reduce the real maximum.

The question does not give bytes per cell, so the numeric example uses an explicit assumtion.
