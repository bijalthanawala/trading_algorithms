import sys
import argparse
import logging
import pprint
from typing import List

DEFAULT_CSV_FILENAME="test.csv"
ALGORITHMS_LIST = {
        1: "Algorithm x",
        2: "Algorithm y",
        3: "Algorithm z",
        }

def setup_argument_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Trading Algorithm")
    parser.add_argument("--verbose", "-v", action="count", default=0)
    parser.add_argument("--file", "-f", default=DEFAULT_CSV_FILENAME, help=f"Name of the input CSV file (Default={DEFAULT_CSV_FILENAME})")
    parser.add_argument("--algorithm", "-a", type=int, default=1, choices= ALGORITHMS_LIST.keys(), help=f"Specify the algorithm number {pprint.pformat(ALGORITHMS_LIST)} (Default=1)")
    args = parser.parse_args(sys.argv[1:])
    return args

def setup_logger(args: argparse.Namespace):
    level_to_set = logging.WARNING
    if args.verbose >= 2:
        level_to_set = logging.DEBUG
    elif args.verbose == 1:
        level_to_set = logging.INFO
    logging.basicConfig(format="%(message)s", level=level_to_set)

def usage(args) -> None:
    print(f"Usage: {args[0]} <name of csv file>")

def main(args: List[str]) -> bool:
    args = setup_argument_parser()
    setup_logger(args)
    pprint.pprint(args)

    return True


if __name__ == "__main__":
    print(main(sys.argv))
