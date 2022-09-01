import sys
import argparse
import logging
import pprint
from typing import List

DEFAULT_CSV_FILENAME = "test.csv"
ALGORITHMS_LIST = {
    1: "Algorithm x",
    2: "Algorithm y",
    3: "Algorithm z",
}


def setup_argument_parser(unparsed_args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Trading Algorithm", formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--file",
        "-f",
        default=DEFAULT_CSV_FILENAME,
        help=f"Name of the input CSV file (Default={DEFAULT_CSV_FILENAME})",
    )
    parser.add_argument(
        "--algorithm",
        "-a",
        type=int,
        default=1,
        choices=ALGORITHMS_LIST.keys(),
        help=f"Specify one of the algorithm numbers (Default=1)\n{pprint.pformat(ALGORITHMS_LIST)}",
    )
    parser.add_argument("--verbose", "-v", action="count", default=0)
    parsed_args = parser.parse_args(unparsed_args)
    return parsed_args


def setup_logger(parsed_args: argparse.Namespace):
    level_to_set = logging.WARNING
    if parsed_args.verbose >= 2:
        level_to_set = logging.DEBUG
    elif parsed_args.verbose == 1:
        level_to_set = logging.INFO
    logging.basicConfig(format="%(message)s", level=level_to_set)


def main(sys_argv: List[str]) -> bool:
    parsed_args = setup_argument_parser(sys_argv[1:])
    setup_logger(parsed_args)
    pprint.pprint(parsed_args)

    return True


if __name__ == "__main__":
    main(sys.argv)
