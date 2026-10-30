import time
from multiprocessing import Pool


def collatz_steps(n):
    steps = 0
    while n > 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps


def run_granularity(workers, total_items=1_000_000, chunk_size=1):
    numbers = range(1, total_items + 1)
    t0 = time.perf_counter()
    with Pool(processes=workers) as pool:
        results = pool.map(collatz_steps, numbers, chunksize=chunk_size)
    return time.perf_counter() - t0, sum(results)


if __name__ == '__main__':
    print('=== Experiment A: Granularity ===')
    for p in [1, 2, 4, 8]:
        elapsed, _ = run_granularity(workers=p, chunk_size=1)
        print(f'P={p:2d} | Time={elapsed:6.3f}s')