# Task 08: 
P = 128 and the given fraction is 0.08.

Amdahl: 1 / (0.08 + 0.92 / 128) = 11.470.
Gustafson: 128 - 0.08(127) = 117.84.
Difference = 117.84 - 11.470 = 106.370.

Using Amdahl as the percentage reference, the difference is about 927.42%. The two models are not predictions for the same experiment: Amdahl keeps the work fixed, while Gustafson allows the work to grow.
