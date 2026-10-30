import numpy as np
import time
import json
from pathlib import Path
from numba import njit


BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / "results" / "salted_params.json", "r") as file:
    params = json.load(file)

N = params["N"]
M = N // 2
seed = params["seed"]

rng = np.random.default_rng(seed)

A = rng.random((M, M))
B = rng.random((M, M))


@njit
def naive_ijk(A, B):
    M = A.shape[0]
    C = np.zeros((M, M))

    for i in range(M):
        for j in range(M):
            for k in range(M):
                C[i, j] += A[i, k] * B[k, j]

    return C


@njit
def interchanged_ikj(A, B):
    M = A.shape[0]
    C = np.zeros((M, M))

    for i in range(M):
        for k in range(M):
            value = A[i, k]

            for j in range(M):
                C[i, j] += value * B[k, j]

    return C


print("Compiling functions...")

naive_ijk(A, B)
interchanged_ikj(A, B)

print("Compilation completed!")

naive_times = []
interchanged_times = []

for run in range(3):
    start = time.perf_counter()

    C1 = naive_ijk(A, B)

    end = time.perf_counter()
    naive_times.append(end - start)

    start = time.perf_counter()

    C2 = interchanged_ikj(A, B)

    end = time.perf_counter()
    interchanged_times.append(end - start)

    print("Run", run + 1, "completed")

correct = np.allclose(C1, C2, rtol=1e-5, atol=1e-5)

naive_median = float(np.median(naive_times))
interchanged_median = float(np.median(interchanged_times))

speedup = naive_median / interchanged_median

results = {
    "N": N,
    "M": M,
    "naive_ijk_median_seconds": naive_median,
    "interchanged_ikj_median_seconds": interchanged_median,
    "speedup": speedup,
    "results_match": bool(correct),
    "naive_times": naive_times,
    "interchanged_times": interchanged_times
}

output_file = BASE_DIR / "results" / "loop_interchange.json"

with open(output_file, "w") as file:
    json.dump(results, file, indent=4)

print("\nLoop interchange benchmark completed!")
print(json.dumps(results, indent=4))
print("Results saved to:", output_file)