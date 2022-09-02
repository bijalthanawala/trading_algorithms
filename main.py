import sys
import argparse
import logging
import pprint
from typing import List

from result import Result
from trading_algorithms import TradingAlgorithms

DEFAULT_CSV_FILENAME = "data_10.csv"


def parse_arguments(unparsed_args: List[str]) -> argparse.Namespace:
    algorithm_choices = TradingAlgorithms.ALGORITHMS_CHOICES()
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
        choices=algorithm_choices.keys(),
        help=f"Specify one of the algorithm numbers (Default=1)\n{pprint.pformat(algorithm_choices)}",
    )
    parser.add_argument("--verbose", "-v", action="count", default=0)
    parsed_args = parser.parse_args(unparsed_args)
    return parsed_args


def setup_logger(verbosity: int) -> None:
    level_to_set = logging.WARNING
    if verbosity >= 2:
        level_to_set = logging.DEBUG
    elif verbosity == 1:
        level_to_set = logging.INFO
    logging.basicConfig(format="%(message)s", level=level_to_set)


def main(sys_argv: List[str]) -> bool:
    parsed_args = parse_arguments(sys_argv[1:])
    setup_logger(parsed_args.verbose)

    trading_algorithms = TradingAlgorithms(parsed_args.file)
    result = trading_algorithms.init_result

    # TODO: It would be better if TradingAlgorithms constructor raised exception!
    if not result.isSuccess:
        print(f"Error encountered: {result.message}")
        print("Please fix the above error and rerun")
        return result.isSuccess

    trading_algorithms.run(parsed_args.algorithm)

    return True


if __name__ == "__main__":
    main(sys.argv)
