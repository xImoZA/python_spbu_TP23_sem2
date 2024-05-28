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

    def multithread_merge_sort(self, sub_list: list[int]) -> list[int]:
        pool = ThreadPoolExecutor if not self.multiprocess else ProcessPoolExecutor

        list_len = len(sub_list)
        if list_len <= 1:
            return sub_list

        with pool(max_workers=2) as executor1:
            sublist1 = executor1.submit(self.merge_sort, sub_list[: list_len // 2])
            sublist2 = executor1.submit(self.merge_sort, sub_list[list_len // 2 :])
            return self.merge_lists((sublist1.result(), sublist2.result()))

    def merge_sort_multithread(self, user_list: list[int], n_jobs: int) -> list[int]:
        pool = ThreadPoolExecutor if not self.multiprocess else ProcessPoolExecutor

        if n_jobs > len(user_list):
            size = 1
        else:
            size = len(user_list) // n_jobs
        list_slices = [user_list[i : i + size] for i in range(0, len(user_list), size)]

        with pool(max_workers=n_jobs // 3) as executor:
            results = list(executor.map(self.multithread_merge_sort, list_slices))
            while len(results) > 1:
                results.append([])
                results = list(executor.map(self.merge_lists, zip(*[iter(results)] * 2)))
        return results[0] if len(results) == 1 else results
