from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed


class MergeSort:
    @staticmethod
    def merge_lists(left: list[int], right: list[int]) -> list[int]:
        result = []
        while left and right:
            if left[0] >= right[0]:
                result.append(right[0])
                right.pop(0)
            else:
                result.append(left[0])
                left.pop(0)
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
        return MergeSort.merge_lists(right, left)

    def merge_sort_multithread(self, user_list: list[int], n_jobs: int, multiprocess: bool = False) -> list[int]:
        pool = ThreadPoolExecutor if not multiprocess else ProcessPoolExecutor

        if n_jobs > len(user_list):
            size = 1
        else:
            size = len(user_list) // n_jobs
        list_slices = [user_list[i : i + size] for i in range(0, len(user_list), size)]

        out_list: list[int] = []
        with pool(max_workers=n_jobs) as executor:
            sub_arr = [executor.submit(self.merge_sort, sub_list) for sub_list in list_slices]
            for arr in as_completed(sub_arr):
                out_list = MergeSort.merge_lists(out_list, arr.result())

        return out_list
