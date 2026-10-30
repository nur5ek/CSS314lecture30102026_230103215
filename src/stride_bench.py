import numpy as np
import time
import json
import csv
from pathlib import Path
from numba import njit


BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / "results" / "salted_params.json", "r") as file:
    params = json.load(file)

data = np.ones(params["buffer_elements"], dtype=np.float64)

strides = [1, 2, 4, 8, 16, 32, 64, 128]


@njit
def calculate_sum(data, stride):
    total = 0.0

    for i in range(0, len(data), stride):
        total += data[i]

    return total


results = []

for stride in strides:
    total_elements = len(data[::stride])

    for _ in range(5):
        total = calculate_sum(data, stride)

    times = []

    for _ in range(5):
        start = time.perf_counter_ns()
        total = calculate_sum(data, stride)
        end = time.perf_counter_ns()

        times.append(end - start)

    median_time = float(np.median(times))
    latency = median_time / total_elements

    results.append({
        "stride": stride,
        "elements_touched": total_elements,
        "median_time_ns": median_time,
        "latency_ns_per_element": latency
    })

output_file = BASE_DIR / "results" / "stride_results.tsv"

with open(output_file, "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "stride",
            "elements_touched",
            "median_time_ns",
            "latency_ns_per_element"
        ],
        delimiter="\t"
    )

    writer.writeheader()
    writer.writerows(results)

print("Stride benchmark completed!")

for result in results:
    print(result)

print("Results saved to:", output_file)