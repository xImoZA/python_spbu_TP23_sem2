from argparse import ArgumentParser

from src.Control_tests.final_test.wiki_bfs import Model


def main(start_url: str, depth: int, threads: int) -> None:
    Model(start_url, "http://en.wikipedia.org/wiki/Adolf_Hitler", depth, threads).main()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("start_url", type=str, help="City name")
    parser.add_argument("depth", type=int, help="Find depth")
    parser.add_argument("count_threads", type=int, help="Count of threads")
    args = parser.parse_args()

    main(args.start_url, args.depth, args.count_threads)
