from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from multiprocessing import Manager
from multiprocessing.managers import ListProxy
from queue import Queue
from typing import Optional

from loguru import logger

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


class ModelClickTo:
    def __init__(self):
        self.visited: list[str] = Manager().list()

    @staticmethod
    def make_visit(
        queue: Queue[Node], visited: list[str], end: str, is_result: ListProxy, unique: bool
    ) -> Optional[list[str]]:
        cur_node = queue.get()
        if unique:
            neighbors = get_links(cur_node.url) - set(visited)
        else:
            neighbors = get_links(cur_node.url)

        for link in neighbors:
            if is_result[-1]:
                return None
            if link == end:
                is_result.append(True)
                return get_path(Node(link, cur_node))
            visited.append(link)
            queue.put(Node(link, cur_node))
        return None

    def find_way(self, start_url: str, end_url: str, n_jobs: int, unique: bool) -> Optional[list[str]]:
        with Manager() as manager:
            founded: Queue[Node] = manager.Queue()
            founded.put(Node(start_url, None))
            is_result: ListProxy = manager.list()
            is_result.append(False)

            for depth in range(10):
                logger.info(f"Work on depth {depth}")
                with ProcessPoolExecutor(max_workers=n_jobs) as executor:
                    futures = [
                        executor.submit(ModelClickTo.make_visit, founded, self.visited, end_url, is_result, unique)
                        for _ in range(founded.qsize())
                    ]

                    for res in as_completed(futures):
                        result = res.result()
                        if result:
                            return result
            logger.info(f"No path {start_url} -> {end_url} was not found at a depth of 10")
        return None
