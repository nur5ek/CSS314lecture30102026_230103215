import multiprocessing as mp
from multiprocessing import shared_memory
import numpy as np
import csv
import json
import math
import statistics
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"

with open(RESULTS_DIR / "salted_params.json", "r") as file:
    params = json.load(file)

N = params["N"]
SEED = params["seed"]

PROCESS_COUNTS = [1, 2, 4, 8, 10]
REPEATS = 3

PEAK_MEMORY_BANDWIDTH_GB_S = 76.8

INPUT_ARRAY = None
OUTPUT_ARRAY = None
INPUT_SHM = None
OUTPUT_SHM = None


def initialize_worker(input_name, output_name, shape):
    global INPUT_ARRAY, OUTPUT_ARRAY
    global INPUT_SHM, OUTPUT_SHM

    INPUT_SHM = shared_memory.SharedMemory(name=input_name)
    OUTPUT_SHM = shared_memory.SharedMemory(name=output_name)

    INPUT_ARRAY = np.ndarray(
        shape, dtype=np.float64, buffer=INPUT_SHM.buf
    )

    OUTPUT_ARRAY = np.ndarray(
        shape, dtype=np.float64, buffer=OUTPUT_SHM.buf
    )


def stencil_worker(chunk):
    start_row, end_row = chunk

    OUTPUT_ARRAY[start_row:end_row, 1:-1] = (
        INPUT_ARRAY[start_row - 1:end_row - 1, 1:-1]
        + INPUT_ARRAY[start_row + 1:end_row + 1, 1:-1]
        + INPUT_ARRAY[start_row:end_row, :-2]
        + INPUT_ARRAY[start_row:end_row, 2:]
        + INPUT_ARRAY[start_row:end_row, 1:-1]
    ) * 0.2


def make_chunks(n, process_count):
    total_rows = n - 2
    base_rows = total_rows // process_count
    extra_rows = total_rows % process_count

    chunks = []
    current_row = 1

    for i in range(process_count):
        rows = base_rows

        if i < extra_rows:
            rows += 1

        next_row = current_row + rows
        chunks.append((current_row, next_row))
        current_row = next_row

    return chunks


def run_case(n, process_count):
    rng = np.random.default_rng(SEED)

    input_data = rng.random((n, n), dtype=np.float64)
    output_data = np.zeros((n, n), dtype=np.float64)

    reference = np.zeros((n, n), dtype=np.float64)

    reference[1:-1, 1:-1] = (
        input_data[:-2, 1:-1]
        + input_data[2:, 1:-1]
        + input_data[1:-1, :-2]
        + input_data[1:-1, 2:]
        + input_data[1:-1, 1:-1]
    ) * 0.2

    input_shm = shared_memory.SharedMemory(
        create=True, size=input_data.nbytes
    )

    output_shm = shared_memory.SharedMemory(
        create=True, size=output_data.nbytes
    )

    shared_input = np.ndarray(
        input_data.shape, dtype=np.float64, buffer=input_shm.buf
    )

    shared_output = np.ndarray(
        output_data.shape, dtype=np.float64, buffer=output_shm.buf
    )

    shared_input[:] = input_data
    shared_output[:] = output_data

    chunks = make_chunks(n, process_count)
    times = []

    try:
        with mp.Pool(
            processes=process_count,
            initializer=initialize_worker,
            initargs=(
                input_shm.name,
                output_shm.name,
                input_data.shape
            )
        ) as pool:

            pool.map(stencil_worker, chunks)

            for repeat in range(REPEATS):
                start = time.perf_counter()

                pool.map(stencil_worker, chunks)

                end = time.perf_counter()
                elapsed = end - start
                times.append(elapsed)

                print(
                    f"N={n}, P={process_count}, "
                    f"run={repeat + 1}, time={elapsed:.6f} s"
                )

        result = np.ndarray(
            output_data.shape,
            dtype=np.float64,
            buffer=output_shm.buf
        )

        if not np.allclose(
            result, reference, rtol=1e-12, atol=1e-12
        ):
            raise RuntimeError(
                "Parallel stencil does not match reference!"
            )

        checksum = float(np.sum(result, dtype=np.float64))
        reference_checksum = float(
            np.sum(reference, dtype=np.float64)
        )

        return (
            statistics.median(times),
            checksum,
            reference_checksum
        )

    finally:
        input_shm.close()
        input_shm.unlink()

        output_shm.close()
        output_shm.unlink()


def main():
    RESULTS_DIR.mkdir(exist_ok=True)

    rows = []

    print("\n========== STRONG SCALING ==========")

    strong_times = {}
    strong_checksum = None
    strong_reference_checksum = None

    for p in PROCESS_COUNTS:
        elapsed, checksum, reference_checksum = run_case(N, p)

        strong_times[p] = elapsed

        if p == 1:
            strong_checksum = checksum
            strong_reference_checksum = reference_checksum

        speedup = strong_times[1] / elapsed
        efficiency = speedup / p * 100

        serial_fraction = None

        if p > 1:
            serial_fraction = (
                (1 / speedup) - (1 / p)
            ) / (1 - (1 / p))

        rows.append([
            "strong",
            p,
            N,
            (N - 2) ** 2,
            elapsed,
            speedup,
            efficiency,
            serial_fraction,
            ""
        ])

        print(
            f"Strong P={p}: time={elapsed:.6f} s, "
            f"speedup={speedup:.3f}, "
            f"efficiency={efficiency:.2f}%"
        )

    measured_points = []

    for p in PROCESS_COUNTS[1:]:
        measured_speedup = strong_times[1] / strong_times[p]
        measured_points.append((p, measured_speedup))

    best_s = 0.0
    best_error = float("inf")

    for candidate_s in np.linspace(0, 1, 10001):
        error = 0.0

        for p, measured_speedup in measured_points:
            predicted = 1 / (
                candidate_s + (1 - candidate_s) / p
            )

            error += (predicted - measured_speedup) ** 2

        if error < best_error:
            best_error = error
            best_s = float(candidate_s)

    maximum_speedup = 1 / best_s if best_s > 0 else None

    print("\n========== WEAK SCALING ==========")

    weak_times = {}
    weak_work = {}

    for p in PROCESS_COUNTS:
        weak_n = math.ceil(N * math.sqrt(p))

        elapsed, checksum, reference_checksum = run_case(
            weak_n, p
        )

        weak_times[p] = elapsed
        weak_work[p] = (weak_n - 2) ** 2

    weak_baseline_time = weak_times[1]
    weak_baseline_work = weak_work[1]

    for p in PROCESS_COUNTS:
        scaled_speedup = (
            p * weak_baseline_work * weak_baseline_time
        ) / (weak_work[p] * weak_times[p])

        rows.append([
            "weak",
            p,
            math.ceil(N * math.sqrt(p)),
            weak_work[p],
            weak_times[p],
            "",
            "",
            "",
            scaled_speedup
        ])

        print(
            f"Weak P={p}: N={math.ceil(N * math.sqrt(p))}, "
            f"time={weak_times[p]:.6f} s, "
            f"scaled speedup={scaled_speedup:.3f}"
        )

    print("\n========== ROOFLINE ANALYSIS ==========")

    flops_per_cell = 5
    bytes_per_cell = 6 * 8

    arithmetic_intensity = (
        flops_per_cell / bytes_per_cell
    )

    bandwidth_roof = (
        arithmetic_intensity * PEAK_MEMORY_BANDWIDTH_GB_S
    )

    roofline = {
        "kernel": "5-point 2D stencil",
        "base_dimension": N,
        "floating_point_operations_per_cell": flops_per_cell,
        "bytes_per_cell": bytes_per_cell,
        "arithmetic_intensity_flops_per_byte": arithmetic_intensity,
        "peak_memory_bandwidth_gb_s_assumed": PEAK_MEMORY_BANDWIDTH_GB_S,
        "estimated_bandwidth_roof_gflops": bandwidth_roof,
        "classification": "Memory-Bandwidth Bound",
        "amdahl_fitted_serial_fraction": best_s,
        "amdahl_maximum_speedup": maximum_speedup,
        "strong_scaling_times": strong_times,
        "weak_scaling_times": weak_times,
        "strong_checksum": strong_checksum,
        "reference_checksum": strong_reference_checksum
    }

    metrics_path = RESULTS_DIR / "scaling_metrics.tsv"

    with open(metrics_path, "w", newline="") as file:
        writer = csv.writer(file, delimiter="\t")

        writer.writerow([
            "study",
            "processes",
            "dimension",
            "work_cells",
            "runtime_seconds",
            "speedup",
            "efficiency_percent",
            "amdahl_serial_fraction",
            "scaled_speedup"
        ])

        writer.writerows(rows)

    roofline_path = RESULTS_DIR / "roofline_summary.json"

    with open(roofline_path, "w") as file:
        json.dump(roofline, file, indent=4)

    print("\n========== MILESTONE 3 COMPLETED ==========")
    print("Amdahl serial fraction:", best_s)
    print("Maximum theoretical speedup:", maximum_speedup)
    print("Arithmetic intensity:", arithmetic_intensity)
    print("Results saved in results folder.")


if __name__ == "__main__":
    main()
