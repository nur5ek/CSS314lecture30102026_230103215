# Task 16: Matrix Multiplication

Dense matrix multiplication takes O(N^3) operations. If total compute work grows in proportion to P, then N(P)^3 = P * N(1)^3.

Therefore N(P) = N(1) * P^(1/3).

| P | N(P) / N(1) | Memory factor N(P)^2 / N(1)^2 |
|---:|---:|---:|
| 1 | 1.000 | 1.000 |
| 8 | 2.000 | 4.000 |
| 64 | 4.000 | 16.000 |
| 512 | 8.000 | 64.000 |
| 4096 | 16.000 | 256.000 |

This assumes ideal compute scaling. Matrix communication can prevent fixed runtime in practice.
