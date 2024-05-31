import time
from argparse import ArgumentParser

from loguru import logger

from src.Control_tests.final_test.wiki_bfs import ModelClickTo


def main(urls: list[str], n_jobs: int, unique: bool) -> None:
    model = ModelClickTo()
    path = [urls[0]]
    logger.info("Welcome to Wiki Grand Tour!")

    if len(urls) == 1:
        print("The resulting path:")
        print(urls[0])
    else:
        logger.info(f"Will look for the way {' -> '.join(urls)}")

        for i in range(0, len(urls) - 1):
            logger.info(f"Looking for a way {urls[i]} -> {urls[i + 1]}")
            sub_path = model.find_way(urls[i], urls[i + 1], n_jobs, unique)

            if sub_path:
                path.extend(sub_path[1:])
                logger.info(f"Find way!")

        if len(path) > 1:
            time.sleep(1)
            print("The resulting path:")
            print(" -> ".join(path))
        else:
            print("There was no such way")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("n_jobs", type=int, help="Count of threads")
    parser.add_argument("urls", type=str, nargs="+", help="Links through which to find a way")
    parser.add_argument("--unique", action="store_true", help="Search the path only through unique links")
    args = parser.parse_args()

    main(args.urls, args.n_jobs, args.unique)
