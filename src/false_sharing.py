
import multiprocessing as mp
import ctypes
import time
import statistics
import csv
from pathlib import Path

K = 5_000_000
PROCESS_COUNTS = [1, 2, 4, 8]
REPEATS = 3

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"


def worker(
    shared_array,
    worker_id,
    iterations,
    variant,
    ready_count,
    ready_lock,
    start_event,
    done_count,
    done_lock,
    write_lock
):
    # Tell the main process that this worker is ready.
    with ready_lock:
        ready_count.value += 1

    # Wait until all workers are ready.
    start_event.wait()

    if variant == "unpadded":
        for _ in range(iterations):
            shared_array[worker_id] += 1

    elif variant == "padded":
        index = worker_id * 8

        for _ in range(iterations):
            shared_array[index] += 1

    else:
        local_count = 0

        for _ in range(iterations):
            local_count += 1

        # One synchronized write after local counting.
        with write_lock:
            shared_array[worker_id] = local_count

    # Tell the main process that work is finished.
    with done_lock:
        done_count.value += 1


def run_test(variant, process_count, context):
    times = []

    for repeat in range(REPEATS):

        if variant == "unpadded":
            shared_array = context.Array(
                ctypes.c_int64, 8, lock=False
            )

        elif variant == "padded":
            shared_array = context.Array(
                ctypes.c_int64, process_count * 8, lock=False
            )

        else:
            shared_array = context.Array(
                ctypes.c_int64, process_count, lock=False
            )

        ready_count = context.Value("i", 0)
        done_count = context.Value("i", 0)

        ready_lock = context.Lock()
        done_lock = context.Lock()
        write_lock = context.Lock()
        start_event = context.Event()

        processes = []

        for worker_id in range(process_count):
            process = context.Process(
                target=worker,
                args=(
                    shared_array,
                    worker_id,
                    K,
                    variant,
                    ready_count,
                    ready_lock,
                    start_event,
                    done_count,
                    done_lock,
                    write_lock
                )
            )

            processes.append(process)
            process.start()

        # Wait until every worker is ready.
        while ready_count.value < process_count:
            time.sleep(0.001)

        # Start timing immediately before releasing workers.
        start_time = time.perf_counter()
        start_event.set()

        # Wait until every worker finishes its loop.
        while done_count.value < process_count:
            time.sleep(0.001)

        end_time = time.perf_counter()

        for process in processes:
            process.join()

            if process.exitcode != 0:
                raise RuntimeError(
                    "A worker process finished with an error."
                )

        elapsed = end_time - start_time
        times.append(elapsed)

        # Verify the result.
        if variant == "padded":
            total = sum(
                shared_array[worker_id * 8]
                for worker_id in range(process_count)
            )
        else:
            total = sum(
                shared_array[worker_id]
                for worker_id in range(process_count)
            )

        expected_total = process_count * K

        if total != expected_total:
            raise RuntimeError(
                f"Incorrect result: expected {expected_total}, "
                f"got {total}"
            )

        print(
            f"{variant}, P={process_count}, "
            f"repeat={repeat + 1}, time={elapsed:.4f} seconds"
        )

    return statistics.median(times)


def main():
    RESULTS_DIR.mkdir(exist_ok=True)

    context = mp.get_context("spawn")

    variants = ["unpadded", "padded", "privatized"]
    all_results = {}

    for variant in variants:
        all_results[variant] = {}

        print(f"\nTesting {variant}...")

        for process_count in PROCESS_COUNTS:
            median_time = run_test(
                variant, process_count, context
            )

            all_results[variant][process_count] = median_time

            print(
                f"Median: {variant}, P={process_count}: "
                f"{median_time:.4f} seconds"
            )

    # Save measured runtimes.
    results_path = RESULTS_DIR / "false_sharing_results.tsv"

    with open(results_path, "w", newline="") as file:
        writer = csv.writer(file, delimiter="\t")

        writer.writerow([
            "variant",
            "processes",
            "K",
            "median_time_seconds"
        ])

        for variant in variants:
            for process_count in PROCESS_COUNTS:
                writer.writerow([
                    variant,
                    process_count,
                    K,
                    all_results[variant][process_count]
                ])

    # Calculate Karp-Flatt metric.
    karp_flatt_path = (
        RESULTS_DIR / "false_sharing_karp_flatt.tsv"
    )

    with open(karp_flatt_path, "w", newline="") as file:
        writer = csv.writer(file, delimiter="\t")

        writer.writerow([
            "variant",
            "processes",
            "T1_seconds",
            "TP_seconds",
            "karp_flatt_e"
        ])

        for variant in ["unpadded", "padded"]:
            t1 = all_results[variant][1]

            for process_count in [2, 4, 8]:
                tp = all_results[variant][process_count]

                e = (
                    (process_count * tp / t1) - 1
                ) / (process_count - 1)

                writer.writerow([
                    variant,
                    process_count,
                    t1,
                    tp,
                    e
                ])

                print(
                    f"Karp-Flatt {variant}, P={process_count}: "
                    f"{e:.6f}"
                )

    print("\nMilestone 2 benchmarks completed!")
    print("Results saved in the results folder.")


if __name__ == "__main__":
    main()
