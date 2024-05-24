import hypothesis.strategies as st
from hypothesis import given, settings

from src.Homeworks.Homework_4.sort import MergeSort


class TestMergeSort:
    sort = MergeSort()

    @given(st.lists(st.integers()), st.lists(st.integers()))
    def test_merge_lists(self, left_arr: list[int], right_arr: list[int]) -> None:
        left_arr.sort()
        right_arr.sort()
        expected = left_arr + right_arr
        expected.sort()
        assert MergeSort.merge_lists(left_arr, right_arr) == expected

    @given(st.lists(st.integers()))
    def test_merge_sort(self, test_arr: list[int]) -> None:
        assert self.sort.merge_sort(test_arr) == sorted(test_arr)

    @settings(deadline=None)
    @given(st.lists(st.integers()), st.integers(1, 100))
    def test_merge_sort_multithread(self, test_arr: list[int], n_jobs: int) -> None:
        assert self.sort.merge_sort_multithread(test_arr, n_jobs) == sorted(test_arr)

    @settings(deadline=None)
    @given(st.lists(st.integers()), st.integers(1, 100))
    def test_merge_sort_multiprocess(self, test_arr: list[int], n_jobs: int) -> None:
        assert self.sort.merge_sort_multithread(test_arr, n_jobs, multiprocess=True) == sorted(test_arr)
