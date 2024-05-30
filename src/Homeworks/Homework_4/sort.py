import math
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed


class MergeSort:
    def __init__(self, multiprocess: bool):
        self.multiprocess = multiprocess

    @staticmethod
    def merge_lists(t: tuple[list[int], list[int]]) -> list[int]:
        left, right = t
        result = []
        while left and right:
            if left[0] >= right[0]:
                result.append(right[0])
                del right[0]
            else:
                result.append(left[0])
                del left[0]
        if left:
            result.extend(left)
            return result

        result.extend(right)
        return result

    def merge_sort(self, user_list: list[int]) -> list[int]:
        list_len = len(user_list)
        if list_len <= 1:
            return user_list

        right, left = self.merge_sort(user_list[: list_len // 2]), self.merge_sort(user_list[list_len // 2 :])
        return MergeSort.merge_lists((right, left))

    def merge_sort_multithread1(self, user_list: list[int], n_jobs: int) -> list[int]:
        pool = ThreadPoolExecutor if not self.multiprocess else ProcessPoolExecutor

        if n_jobs > len(user_list):
            size = 1
        else:
            size = len(user_list) // n_jobs
        list_slices = [user_list[i : i + size] for i in range(0, len(user_list), size)]

        with pool(max_workers=n_jobs) as executor:
            results = list(executor.map(self.merge_sort, list_slices))
            while len(results) > 1:
                results.append([])
                results = list(executor.map(self.merge_lists, zip(*[iter(results)] * 2)))
        return results[0] if len(results) == 1 else results

    def merge_sort_multithread2(self, data: tuple[list[int], int]) -> list[int]:
        user_list, n_jobs = data[0], data[1]
        pool = ThreadPoolExecutor if not self.multiprocess else ProcessPoolExecutor

        if n_jobs == 1:
            return self.merge_sort(user_list)

        if int(math.log(n_jobs)) == math.log(n_jobs):
            list_slices = [
                (user_list[: len(user_list) // 2], 2 ** int(math.log(n_jobs)) // 2),
                (user_list[len(user_list) // 2 :], 2 ** int(math.log(n_jobs)) // 2),
            ]
        else:
            list_slices = [
                (user_list[: len(user_list) // 2], 2 ** int(math.log(n_jobs))),
                (user_list[len(user_list) // 2 :], n_jobs - 2 ** int(math.log(n_jobs))),
            ]

        with pool(max_workers=n_jobs) as executor:
            results = list(executor.map(self.merge_sort_multithread2, list_slices))
            while len(results) > 1:
                results.append([])
                results = list(executor.map(self.merge_lists, zip(*[iter(results)] * 2)))
        return results[0] if len(results) == 1 else results

    def merge_sort2(
        self, user_list: list[int], count: int, n_jobs: int, exe: ThreadPoolExecutor | ProcessPoolExecutor
    ) -> tuple | list[int]:
        if count < n_jobs:
            list1, list2 = user_list[: len(user_list) // 2], user_list[len(user_list) // 2 :]
            ft1 = exe.submit(self.merge_sort2, list1, count + 2, n_jobs, exe)
            ft2 = exe.submit(self.merge_sort2, list2, count + 2, n_jobs, exe)
            return ft1, ft2
        return self.merge_sort(user_list)

    def merge_sort_multithread3(self, user_list: list[int], n_jobs: int) -> list[int]:
        pool = ThreadPoolExecutor if not self.multiprocess else ProcessPoolExecutor
        list_slices = [user_list[: len(user_list) // 2], user_list[len(user_list) // 2 :]]

        with pool(max_workers=n_jobs) as executor:
            futures = [executor.submit(self.merge_sort2, sub_list, 2, n_jobs, executor) for sub_list in list_slices]
            results = []
            while len(futures) > 0:
                for res in as_completed(futures):
                    res1 = res.result()
                    if isinstance(res1, tuple):
                        futures.append(res1[0])
                        futures.append(res1[1])
                    else:
                        results.append(res1)
                    del futures[0]

            while len(results) > 1:
                results.append([])
                results = list(executor.map(self.merge_lists, zip(*[iter(results)] * 2)))
        return results[0] if len(results) == 1 else results
