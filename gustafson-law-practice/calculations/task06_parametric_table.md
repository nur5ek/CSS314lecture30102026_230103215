# Task 06: Scaled Speedup

Alpha = 0.04. I used S(P) = P - 0.04(P - 1) and E(P) = S(P) / P.

| P | S(P) | E(P) |
|---:|---:|---:|
| 16 | 15.40 | 0.962500 |
| 64 | 61.48 | 0.960625 |
| 256 | 245.80 | 0.960156 |
| 1024 | 983.08 | 0.960039 |
| 4096 | 3932.20 | 0.960010 |
| 16384 | 15728.68 | 0.960002 |

Efficiency gets closer to 0.96 as P grows. It does not go to zero in this ideal model.
