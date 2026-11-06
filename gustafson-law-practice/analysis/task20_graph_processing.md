# Task 20: Graph Processing

BFS and PageRank are harder to scale than dense matrix operations. Graph data is irregular, so some workers receive more edges than others. Memory accesses are less predictable and can miss the cache often.

BFS frontiers can change greatly between levels, causing imbalance and repeated synchronization. PageRank needs repeated communication of values along graph edges. Power-law graphs also have a few very high-degree vertices that create hot spots.

Dense matrix operations have regular blocks and predictable computation. That usually makes it easier to divide the work evenly and use memory efficiently. Graph processing can still scale, but it needs good partitioning and communication strategies.
