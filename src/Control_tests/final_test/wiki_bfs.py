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
    def __init__(self) -> None:
        self.not_visit: ListProxy = Manager().list()

    @staticmethod
    def make_visit(
        queue: Queue[Node], visited: ListProxy, end: str, is_result: ListProxy, not_visit: Optional[ListProxy]
    ) -> Optional[list[str]]:
        cur_node = queue.get()
        neighbors = get_links(cur_node.url) - set(visited)

        for link in neighbors:
            if (not_visit and link not in not_visit) or not not_visit:
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
            visited: ListProxy = manager.list()
            founded.put(Node(start_url, None))
            is_result: ListProxy = manager.list()
            is_result.append(False)

            for depth in range(10):
                logger.info(f"Work on depth {depth}")
                with ProcessPoolExecutor(max_workers=n_jobs) as executor:
                    if unique:
                        futures = [
                            executor.submit(
                                ModelClickTo.make_visit, founded, visited, end_url, is_result, self.not_visit
                            )
                            for _ in range(founded.qsize())
                        ]
                    else:
                        futures = [
                            executor.submit(ModelClickTo.make_visit, founded, visited, end_url, is_result, None)
                            for _ in range(founded.qsize())
                        ]

                    for res in as_completed(futures):
                        result = res.result()
                        if result:
                            self.not_visit.extend(result[1:-1])
                            return result
            logger.info(f"No path {start_url} -> {end_url} was not found at a depth of 10")
        return None
