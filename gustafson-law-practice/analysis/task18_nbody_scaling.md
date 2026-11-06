# Task 18: N-Body

Direct all-pairs computation takes O(N^2) operations. With ideal parallelism and a fixed time target, N(P)^2 / P stays constant, so N(P) grows approximately as sqrt(P).

Barnes-Hut takes O(N log N). Its fixed-time target is N(P) log N(P) proportional to P, so N grows approximately like P / log(P).

Both algorithms have setup and communication steps. Direct all-pairs may need particle exchange. Barnes-Hut needs tree construction and remote tree data. These steps can increase the serial or communication fraction as P grows. The exact change cannot be calculated without an overhead model.
