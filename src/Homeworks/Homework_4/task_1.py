import time
from argparse import ArgumentParser
from random import randint
from typing import Callable

import matplotlib.pyplot as plt
from sort import MergeSort


def check_time(func: Callable, num_tries: int, *args: list[int], **kwargs: int) -> float:
    avg_time: list[float] = []
    for _ in range(num_tries):
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        avg_time.append(end - start)
    return sum(avg_time) / num_tries


def show_plot_figure(
    non_thread_time: list[float], multi_time: list[float], threads: list[int], size: int, path: str, multiprocess: bool
) -> None:
    plt.plot(threads, non_thread_time, label="Base sort")
    if multiprocess:
        label = "Multiprocess sort"
        xlabel = "Process number"
    else:
        label = "Multithread sort"
        xlabel = "Threads number"

    plt.plot(threads, multi_time, label=label)
    plt.title(f"Merge sort: size={size}")
    plt.xlabel(xlabel)
    plt.ylabel("time")
    plt.legend()
    plt.grid(True)

    plt.savefig(path)


def main(size: int, num_treads: int, path: str, multiprocess: bool) -> None:
    sort = MergeSort(multiprocess)
    non_sorted_list = [randint(0, 10**4) for _ in range(size)]
    nonthread_time = check_time(sort.merge_sort, 3, non_sorted_list)

    treads = []
    time_treads = []
    for num_treads in range(3, num_treads):
        thread_time = check_time(sort.merge_sort_multithread, 3, non_sorted_list, n_jobs=num_treads)
        time_treads.append(thread_time)
        treads.append(num_treads)

    show_plot_figure([nonthread_time] * len(time_treads), time_treads, treads, size, path, multiprocess)


if __name__ == "__main__":
    argparser = ArgumentParser(description="Multithread and multiprocess merge sort")
    argparser.add_argument("size", type=int, help="The size of the array to sort")
    argparser.add_argument("num_threads", type=int, help="Number of threads and processes")
    argparser.add_argument("output_path", type=str)
    argparser.add_argument("--multiprocess", action="store_true", help="use processes instead of threads")
    args = argparser.parse_args()
    main(args.size, args.num_threads, args.output_path, args.multiprocess)
