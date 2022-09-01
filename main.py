from dataclasses import dataclass
import sys
import csv
import argparse
import logging
import pprint
from typing import List

DEFAULT_CSV_FILENAME = "data_10.csv"
ALGORITHMS_LIST = {
    1: "Algorithm x",
    2: "Algorithm y",
    3: "Algorithm z",
}

# todo: Move this class to a different file later
@dataclass
class Result:
    isSuccess: bool
    info: str


# todo: Start this method here initially and move this to a different file/module later
def read_csv_file(csv_filename: str) -> Result:
    try:
        with open(
            csv_filename, newline="", encoding="ascii", errors="ignore"
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row)
    except Exception as ex:
        return Result(False, str(ex))

        print()
    return Result(True, "")


def parse_arguments(unparsed_args: List[str]) -> argparse.Namespace:
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
    parsed_args = parse_arguments(sys_argv[1:])
    setup_logger(parsed_args)
    result = read_csv_file(parsed_args.file)

    if not result.isSuccess:
        print(f"Error encountered: {result.info}")
        print("Please fix the above error and rerun")

    return result.isSuccess


if __name__ == "__main__":
    main(sys.argv)
