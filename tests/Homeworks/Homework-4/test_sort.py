import hypothesis.strategies as st
from hypothesis import given, settings

from src.Homeworks.Homework_4.sort import MergeSort


class TestMergeSort:
    @given(st.lists(st.integers()), st.lists(st.integers()))
    def test_merge_lists(self, left_arr: list[int], right_arr: list[int]) -> None:
        left_arr.sort()
        right_arr.sort()
        expected = left_arr + right_arr
        expected.sort()
        assert MergeSort.merge_lists((left_arr, right_arr)) == expected

    @given(st.lists(st.integers()))
    def test_merge_sort(self, test_arr: list[int]) -> None:
        sort = MergeSort(False)
        assert sort.merge_sort(test_arr) == sorted(test_arr)

    @settings(deadline=None)
    @given(st.lists(st.integers()), st.integers(3, 10))
    def test_merge_sort_multithread(self, test_arr: list[int], n_jobs: int) -> None:
        sort_multithread = MergeSort(False)

        assert sort_multithread.merge_sort_multithread1(test_arr, n_jobs) == sorted(test_arr)
        assert sort_multithread.merge_sort_multithread2((test_arr, n_jobs)) == sorted(test_arr)
        assert sort_multithread.merge_sort_multithread3(test_arr, n_jobs) == sorted(test_arr)

    @settings(deadline=None)
    @given(st.lists(st.integers()), st.integers(3, 10))
    def test_merge_sort_multiprocess(self, test_arr: list[int], n_jobs: int) -> None:
        sort_multiprocess = MergeSort(True)

        assert sort_multiprocess.merge_sort_multithread1(test_arr, n_jobs) == sorted(test_arr)
        assert sort_multiprocess.merge_sort_multithread2((test_arr, n_jobs)) == sorted(test_arr)
