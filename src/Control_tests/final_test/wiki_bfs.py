from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from queue import Queue
from typing import Optional

from src.Control_tests.final_test.get_wiki_links import get_links


@dataclass
class Node:
    url: str
    parent: Optional["Node"]


def get_path(end_node: Node) -> list[str]:
    out = []
    curr = end_node
    while curr.parent:
        out.append(curr.url)
        curr = curr.parent

    out.append(curr.url)
    return out[::-1]


class Model:
    def __init__(self, start_url: str, end_url: str, depth: int, count_thread: int):
        self.start = start_url
        self.end = end_url
        self.depth = depth
        self.threads = count_thread
        self.min_len = float("inf")

    def find_path(self, list_links: list[str]) -> Optional[list[str]]:
        main_q: Queue[Node] = Queue()
        dist: int = 0
        for link in list_links:
            main_q.put(Node(link, Node(self.start, None)))

        while not main_q.empty():
            curr: Node = main_q.get()
            len_curr_path = len(get_path(curr))
            if dist < len_curr_path - 1:
                dist = len_curr_path
            if len_curr_path - 1 == dist:
                break

            for nbr in get_links(curr.url):
                if nbr == self.end:
                    return get_path(Node(nbr, curr))
                main_q.put(Node(nbr, curr))
        return None

    def main(self) -> None:
        if self.start == self.end:
            print(f"The way: {' -> '.join(self.end)}")

        links = get_links(self.start)
        size = len(links) // self.threads
        sub_links = [links[i : i + size] for i in range(0, len(links), size)]
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            result_list = [executor.submit(self.find_path, links) for links in sub_links]
            min_result = [""] * self.depth
            for path in as_completed(result_list):
                result = path.result()
                if result is not None:
                    if len(result) <= len(min_result):
                        min_result = result

        if result == [""] * self.depth:
            print(f"There is no path with such the {self.depth} length")
        else:
            print(f"The shortest way: {[result]}")
