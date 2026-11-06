# Task 13:

## Parallel BFS on a graph

As a graph grows, the frontier can become unbalanced. Some workers have many neighbors to visit while others wait. Messages and synchronization can grow faster than useful work. The runtime may increase even when vertices per processor stay constant.

## Parallel sorting

A distributed sort often needs data exchange between workers. Adding more processors increases communication partners and synchronization costs. Keeping the same number of elements per worker does not guarantee constant time because the global sorting and merging steps still grow.
In both cases, weak scaling fails when communication or waiting increases with processor count.
